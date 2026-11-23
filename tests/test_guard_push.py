import json
import subprocess
import sys
import unittest
from pathlib import Path

HOOK = Path(__file__).resolve().parent.parent / "hooks" / "guard_push.py"


def decision(command: str, tool: str = "Bash"):
    event = {"tool_name": tool, "tool_input": {"command": command}}
    out = subprocess.run([sys.executable, str(HOOK)], input=json.dumps(event), capture_output=True, text=True, check=True).stdout
    return json.loads(out)["hookSpecificOutput"]["permissionDecision"] if out.strip() else None


class GuardPush(unittest.TestCase):
    def test_asks_for_every_form_of_git_push(self):
        for cmd in [
            "git push",
            "git push origin main",
            "git push --force-with-lease origin feat",
            "cd repo && git push",
            "git add -A && git commit -m 'x' && git push -u origin main",
            "git -C /path/to/repo push",
            "git -c user.name=x push origin",
            "GIT_SSH_COMMAND='ssh -v' git push",
            "/usr/bin/git push",
            "(cd sub; git push)",
            "git status\ngit push",
        ]:
            with self.subTest(cmd=cmd):
                self.assertEqual(decision(cmd), "ask")

    def test_leaves_other_commands_alone(self):
        for cmd in [
            "git status",
            "git log --oneline origin/main..HEAD",
            "git commit -m 'push the button'",
            "echo 'git push'",
            "echo \"remember to git push\"",
            "grep -rn 'git push' docs",
            "git stash push -m wip",
            "npm test",
            "git pushx",
            "git commit -m 'first line\nthen git push later'",
        ]:
            with self.subTest(cmd=cmd):
                self.assertIsNone(decision(cmd))

    def test_ignores_other_tools(self):
        self.assertIsNone(decision("git push", tool="Read"))


if __name__ == "__main__":
    unittest.main()
