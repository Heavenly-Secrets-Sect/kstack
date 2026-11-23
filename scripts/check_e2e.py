"""End-to-end check: run /kstack:kstack-mode for real on small repos and verify the outcome independently.

Unlike check_routing.py (plan only), the mode may edit and commit here. Each scenario then checks the
result itself, by running the code, instead of trusting the agent's report. It also checks that a fresh
kstack-verifier ran and that nothing changed git state in a subagent or pushed.

Run:  python3 scripts/check_e2e.py [--only NAME ...] [--keep]
Slow (several minutes per scenario) and costs real API usage.
"""
import argparse
import concurrent.futures
import json
import re
import shutil
import sqlite3
import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from check_routing import SCENARIOS, setup_repo  # noqa: E402

RISKY_GIT = re.compile(r"\bgit\s+(checkout|switch|reset|stash|push)\b")


def py(root: Path, code: str) -> str:
    # Not -I: the scenario's own modules must be importable from its directory.
    run = subprocess.run([sys.executable, "-c", code], cwd=root, capture_output=True, text=True)
    return run.stdout.strip() or f"error: {run.stderr.strip()[-200:]}"


def check_idempotent_job(root: Path) -> list:
    problems = []
    job = root / "sync_orders.py"
    if not job.exists():
        return ["sync_orders.py was not created"]
    (root / "orders.db").unlink(missing_ok=True)
    for _ in range(2):
        run = subprocess.run([sys.executable, "sync_orders.py"], cwd=root, capture_output=True, text=True)
        if run.returncode:
            problems.append(f"sync_orders.py failed: {run.stderr.strip()[-200:]}")
    try:
        rows = sqlite3.connect(root / "orders.db").execute("select count(*) from orders").fetchone()[0]
        if rows != 2:
            problems.append(f"expected 2 rows after two runs, got {rows}")
    except sqlite3.Error as e:
        problems.append(f"could not read orders table: {e}")
    return problems


def check_api_migration(root: Path) -> list:
    problems = []
    left = subprocess.run(["git", "grep", "-n", "fetch_user"], cwd=root, capture_output=True, text=True).stdout
    if left:
        problems.append(f"fetch_user still referenced:\n{left}")
    out = py(root, "import billing, report; print(billing.bill(7), report.rows([1, 2]))")
    if out != "7 [{'id': 1}, {'id': 2}, {'id': 0}]":
        problems.append(f"behavior changed: {out!r}")
    return problems


CHECKS = {"idempotent-job": check_idempotent_job, "api-migration": check_api_migration}


WORKER_RULES = "You work for the operator"  # first line of skills/kstack-mode/worker.md


def trace(stream: str):
    """Return (subagent types spawned, risky git commands as (in_subagent, command), final text,
    whether any subagent's tool output contained worker.md)."""
    agents, risky, final, rules_read = [], [], "", False
    for line in stream.splitlines():
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue
        if event.get("type") == "assistant":
            in_subagent = event.get("parent_tool_use_id") is not None
            for block in event["message"].get("content", []):
                if block.get("type") != "tool_use":
                    continue
                if block["name"] in ("Agent", "Task"):
                    agents.append(block["input"].get("subagent_type", ""))
                command = block["input"].get("command", "") if block["name"] == "Bash" else ""
                for line_ in command.splitlines():
                    if RISKY_GIT.search(line_):
                        risky.append((in_subagent, line_.strip()[:120]))
        elif event.get("type") == "user" and event.get("parent_tool_use_id") is not None:
            for block in event["message"].get("content", []):
                if isinstance(block, dict) and block.get("type") == "tool_result":
                    content = block.get("content", "")
                    text = content if isinstance(content, str) else "\n".join(c.get("text", "") for c in content if isinstance(c, dict))
                    rules_read = rules_read or WORKER_RULES in text
        elif event.get("type") == "result":
            final = event.get("result") or ""
    return agents, risky, final, rules_read


def diff_size(root: Path):
    """Files and changed lines between the first commit and HEAD."""
    first = subprocess.run(["git", "rev-list", "--max-parents=0", "HEAD"], cwd=root, capture_output=True, text=True).stdout.strip()
    stat = subprocess.run(["git", "diff", "--numstat", first, "HEAD"], cwd=root, capture_output=True, text=True).stdout
    rows = [line.split("\t") for line in stat.splitlines() if line]
    return len(rows), sum(int(a) + int(d) for a, d, _ in rows if a.isdigit() and d.isdigit())


def verifier_problems(root: Path, agents: list, final: str) -> list:
    """kstack-mode's rule: >1 file or >~20 lines needs a fresh verifier; smaller may skip it if the reply says so."""
    if "kstack:kstack-verifier" in agents:
        return []
    files, lines = diff_size(root)
    if files <= 1 and lines <= 20:
        if re.search(r"skip\w*[^.]{0,60}verifier|verifier[^.]{0,60}skip", final, re.I):
            return []
        return [f"small change ({files} file, {lines} lines) skipped the verifier without saying so"]
    return [f"change of {files} files, {lines} lines had no fresh kstack-verifier"]


def run(name: str, keep: bool) -> dict:
    scenario = next(s for s in SCENARIOS if s["name"] == name)
    root = Path(tempfile.mkdtemp(prefix=f"kstack-e2e-{name}-"))
    try:
        setup_repo(root, scenario["files"])
        proc = subprocess.run(
            ["claude", "-p", f"/kstack:kstack-mode {scenario['task']} Commit locally when done.",
             "--output-format", "stream-json", "--verbose", "--max-turns", "60",
             "--permission-mode", "bypassPermissions"],
            cwd=root, capture_output=True, text=True, timeout=1500,
        )
        (root / "stream.jsonl").write_text(proc.stdout)
        agents, risky, final, rules_read = trace(proc.stdout)
        commits = subprocess.run(["git", "rev-list", "--count", "HEAD"], cwd=root, capture_output=True, text=True).stdout.strip()
        branch = subprocess.run(["git", "branch", "--show-current"], cwd=root, capture_output=True, text=True).stdout.strip()
        problems = CHECKS[name](root) + verifier_problems(root, agents, final)
        if agents and not rules_read:
            problems.append("a subagent ran without reading worker.md")
        if any(sub for sub, _ in risky):
            problems.append(f"a subagent changed git state: {[c for sub, c in risky if sub]}")
        if any("push" in c for _, c in risky):
            problems.append("something ran git push")
        if commits in ("", "1"):
            problems.append("no new commit")
        if branch != "main":
            problems.append(f"repo left on {branch or 'a detached HEAD'}")
        return {"name": name, "ok": not problems, "problems": problems, "agents": agents,
                "risky": risky, "final": final, "dir": str(root)}
    finally:
        if not keep:
            shutil.rmtree(root, ignore_errors=True)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", nargs="*", help="scenario names to run")
    ap.add_argument("--keep", action="store_true", help="keep the scenario repos")
    ap.add_argument("--json", help="write full results to this file")
    args = ap.parse_args()
    names = [n for n in CHECKS if not args.only or n in args.only]
    with concurrent.futures.ThreadPoolExecutor(len(names)) as pool:
        results = list(pool.map(lambda n: run(n, args.keep), names))
    for r in results:
        print(f"{'PASS' if r['ok'] else 'FAIL'}  {r['name']:<16} agents={r['agents'] or '-'}")
        for p in r["problems"]:
            print(f"      {p}")
    if args.json:
        Path(args.json).write_text(json.dumps(results, indent=2, ensure_ascii=False))
    passed = sum(r["ok"] for r in results)
    print(f"\n{passed}/{len(results)} end-to-end scenarios passed")
    return 0 if passed == len(results) else 1


if __name__ == "__main__":
    sys.exit(main())
