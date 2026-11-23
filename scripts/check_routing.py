"""Check that /kstack:kstack-mode routes each kind of task to the right playbook and principles.

Each scenario builds a tiny git repo, runs kstack-mode headless in plan-only mode (Edit and Write
are disallowed), and compares the kstack files the session read against what the scenario expects.

Run:  python3 scripts/check_routing.py [--only NAME ...] [--jobs 4] [--keep]
Needs the `claude` CLI with kstack loaded (kstack@skills-dir). Costs real API usage.
"""
import argparse
import concurrent.futures
import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILLS = ROOT / "skills"

PLAN_ONLY = (
    "\n\nThis is a routing check. Do only the first part of the mode: restate the goal, pick the "
    "playbook, read it and every principle file you would apply, and read the project code you "
    "need. Then write the plan and stop. Do not modify files."
)

SCENARIOS = [
    {
        "name": "bug-fix",
        "files": {
            "stats.py": "def average(xs):\n    return sum(xs) / len(xs)\n",
            "test_stats.py": "from stats import average\n\n\ndef test_avg():\n    assert average([1, 2, 3]) == 2\n",
        },
        "task": "average([]) crashes with ZeroDivisionError; it should return None.",
        "playbook": "bug-fix",
        "principles": ["fix-root-causes", "test-behavior-not-implementation"],
    },
    {
        "name": "investigation",
        "files": {
            "pricing.py": "TAX = 0.1\n\n\ndef total(items):\n    return round(sum(i['price'] for i in items) * (1 + TAX), 2)\n",
        },
        "task": "Why does total() round to 2 decimals and where does the tax rate come from? Just explain.",
        "playbook": "investigation",
        "principles": [],
    },
    {
        "name": "idempotent-job",
        "files": {
            "db.py": "import sqlite3\n\n\ndef conn():\n    return sqlite3.connect('orders.db')\n",
            "api.py": "def fetch_orders():\n    return [{'id': 1, 'total': 10}, {'id': 2, 'total': 5}]\n",
        },
        "task": "Add a nightly job sync_orders.py that copies orders from api.fetch_orders() into an orders table. The scheduler retries the job if it crashes.",
        "playbook": "feature",
        "principles": ["make-operations-idempotent"],
    },
    {
        "name": "domain-model",
        "files": {
            "orders.py": (
                "class Order:\n    def __init__(self):\n        self.is_paid = False\n        self.is_shipped = False\n        self.is_cancelled = False\n\n"
                "    def label(self):\n        if self.is_cancelled:\n            return 'cancelled'\n        if self.is_shipped:\n            return 'shipped'\n"
                "        if self.is_paid:\n            return 'paid'\n        return 'new'\n"
            ),
        },
        "task": "Orders can now be refunded after they are paid or shipped. Add refund support.",
        "playbook": "feature",
        "principles": ["model-the-domain"],
    },
    {
        "name": "api-migration",
        "files": {
            "users.py": "def fetch_user(uid):\n    return {'id': uid}\n\n\ndef get_user(uid: int) -> dict:\n    return {'id': uid}\n",
            "billing.py": "from users import fetch_user\n\n\ndef bill(uid):\n    return fetch_user(uid)['id']\n",
            "report.py": "from users import fetch_user, get_user\n\n\ndef rows(ids):\n    return [fetch_user(i) for i in ids] + [get_user(0)]\n",
        },
        "task": "We have two helpers doing the same thing. Replace fetch_user with get_user everywhere so only one remains.",
        "playbook": "refactoring",
        "principles": ["migrate-callers-then-delete-legacy-apis"],
    },
    {
        "name": "large-migration",
        "files": {
            "store_users.py": "import sqlite3\n\n\ndef add(name):\n    c = sqlite3.connect('app.db')\n    c.execute('insert into users(name) values (?)', (name,))\n    c.commit()\n",
            "store_orders.py": "import sqlite3\n\n\ndef add(uid, total):\n    c = sqlite3.connect('app.db')\n    c.execute('insert into orders(uid,total) values (?,?)', (uid, total))\n    c.commit()\n",
            "store_reports.py": "import sqlite3\n\n\ndef count():\n    return sqlite3.connect('app.db').execute('select count(*) from orders').fetchone()[0]\n",
        },
        "task": "Migrate the whole project from raw sqlite3 calls to SQLAlchemy ORM models with Alembic migrations. Plan it in phases.",
        "playbook": "multi-phase-plan",
        "principles": ["outcome-oriented-execution"],
    },
    {
        "name": "shared-state",
        "files": {
            "report.py": (
                "import json\n\n\ndef build_sales(out):\n    out['sales'] = 1\n\n\ndef build_users(out):\n    out['users'] = 2\n\n\n"
                "def build_stock(out):\n    out['stock'] = 3\n\n\ndef main():\n    out = json.load(open('report.json'))\n"
                "    for f in (build_sales, build_users, build_stock):\n        f(out)\n        json.dump(out, open('report.json', 'w'))\n"
            ),
        },
        "task": "Speed up report.py by running the three section builders in parallel processes. Each one currently updates report.json.",
        "playbook": "feature",
        "principles": ["separate-before-serializing-shared-state"],
    },
    {
        "name": "boundary-types",
        "files": {
            "app.py": (
                "import json\n\n\ndef load():\n    return json.load(open('config.json'))\n\n\n"
                "def connect(cfg):\n    if cfg and cfg.get('timeout') is not None:\n        return ('db', int(cfg['timeout']))\n\n\n"
                "def retry(cfg):\n    if cfg and 'retries' in cfg:\n        return int(cfg.get('retries') or 0)\n"
            ),
            "config.json": '{"timeout": "30", "retries": 3}\n',
        },
        "task": "Config handling is fragile: raw dicts are passed everywhere and every function re-checks keys. Make config loading robust and typed.",
        "playbook": "refactoring",
        "principles": ["boundary-discipline", "type-system-discipline"],
    },
]


def setup_repo(root: Path, files: dict) -> None:
    for rel, text in files.items():
        p = root / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text)
    for cmd in (["git", "init", "-q"], ["git", "add", "-A"],
                ["git", "-c", "user.name=t", "-c", "user.email=t@t", "commit", "-qm", "init"]):
        subprocess.run(cmd, cwd=root, check=True)


def heading_index() -> dict:
    """Map each principle and playbook file to its `# Title` line, which identifies it in tool output."""
    index = {}
    for path in [*SKILLS.glob("principle-*/SKILL.md"), *SKILLS.glob("kstack-mode/playbooks/*.md")]:
        title = next(l for l in path.read_text().splitlines() if l.startswith("# "))
        index[str(path.relative_to(ROOT))] = re.compile(rf"^(?:\s*\d+\t)?{re.escape(title)}\s*$", re.M)
    return index


HEADINGS = heading_index()


def tool_output_text(content) -> str:
    if isinstance(content, str):
        return content
    return "\n".join(c.get("text", "") for c in content if isinstance(c, dict))


def kstack_reads(stream: str):
    """Return (kstack files read, tools that tried to modify files, final text).

    A file counts as read when its title shows up in a tool result, so reads through Read, cat,
    loops or anything else all count.
    """
    outputs, writes, final = [], [], ""
    for line in stream.splitlines():
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue
        if event.get("type") == "assistant":
            for block in event["message"].get("content", []):
                if block.get("type") == "tool_use" and block["name"] in ("Edit", "Write", "NotebookEdit"):
                    writes.append(block["name"])
        elif event.get("type") == "user":
            for block in event["message"].get("content", []):
                if isinstance(block, dict) and block.get("type") == "tool_result":
                    outputs.append(tool_output_text(block.get("content", "")))
        elif event.get("type") == "result":
            final = event.get("result") or ""
    text = "\n".join(outputs)
    reads = [rel for rel, title in HEADINGS.items() if title.search(text)]
    return reads, writes, final


def run(scenario: dict, keep: bool) -> dict:
    root = Path(tempfile.mkdtemp(prefix=f"kstack-routing-{scenario['name']}-"))
    try:
        setup_repo(root, scenario["files"])
        proc = subprocess.run(
            ["claude", "-p", f"/kstack:kstack-mode {scenario['task']}{PLAN_ONLY}",
             "--output-format", "stream-json", "--verbose", "--max-turns", "25",
             "--disallowed-tools", "Edit", "Write", "NotebookEdit",
             "--permission-mode", "bypassPermissions"],
            cwd=root, capture_output=True, text=True, timeout=600,
        )
        (root / "stream.jsonl").write_text(proc.stdout)  # kept with --keep, for debugging
        reads, writes, final = kstack_reads(proc.stdout)
        playbook = f"skills/kstack-mode/playbooks/{scenario['playbook']}.md"
        missing = [p for p in scenario["principles"] if f"skills/principle-{p}/SKILL.md" not in reads]
        principles = sorted({r.split("/")[1].removeprefix("principle-") for r in reads if r.startswith("skills/principle-")})
        playbooks = sorted({Path(r).stem for r in reads if "/playbooks/" in r})
        ok = playbook in reads and not missing and not writes
        return {"name": scenario["name"], "ok": ok, "playbooks": playbooks, "principles": principles,
                "missing": missing, "expected_playbook": scenario["playbook"], "writes": writes,
                "final": final, "dir": str(root)}
    finally:
        if not keep:
            shutil.rmtree(root, ignore_errors=True)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", nargs="*", help="scenario names to run")
    ap.add_argument("--jobs", type=int, default=4)
    ap.add_argument("--keep", action="store_true", help="keep the scenario repos")
    ap.add_argument("--json", help="write full results to this file")
    args = ap.parse_args()
    chosen = [s for s in SCENARIOS if not args.only or s["name"] in args.only]
    with concurrent.futures.ThreadPoolExecutor(args.jobs) as pool:
        results = list(pool.map(lambda s: run(s, args.keep), chosen))
    for r in results:
        mark = "PASS" if r["ok"] else "FAIL"
        print(f"{mark}  {r['name']:<16} playbook={','.join(r['playbooks']) or '-'} (want {r['expected_playbook']})")
        print(f"      principles read: {', '.join(r['principles']) or '-'}")
        if r["missing"]:
            print(f"      missing: {', '.join(r['missing'])}")
        if r["writes"]:
            print(f"      tried to modify files: {r['writes']}")
    if args.json:
        Path(args.json).write_text(json.dumps(results, indent=2, ensure_ascii=False))
    passed = sum(r["ok"] for r in results)
    print(f"\n{passed}/{len(results)} scenarios routed as expected")
    return 0 if passed == len(results) else 1


if __name__ == "__main__":
    sys.exit(main())
