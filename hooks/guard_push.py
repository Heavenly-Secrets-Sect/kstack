"""PreToolUse (Bash): the operator decides every `git push`.

kstack's rule "never push without a yes" is otherwise only a prompt. This hook makes it a gate the
harness enforces. In modes that show permission prompts, a Bash call that runs `git push` gets
"ask". Bypass and auto mode resolve "ask" without showing it (measured), so there the push is
denied and the operator pushes with `! git push`, which runs outside the tool and the hook.
"""
import json
import shlex
import sys

CONTROL = {"&&", "||", ";", "|", "&", "(", ")", "\n"}
GIT_OPTS_WITH_VALUE = {"-C", "-c", "--git-dir", "--work-tree", "--namespace"}
NO_PROMPT_MODES = {"bypassPermissions", "auto"}  # these modes approve "ask" without asking


def commands(line: str):
    """Split a shell command line into simple commands (lists of words), respecting quotes."""
    lexer = shlex.shlex(line, posix=True, punctuation_chars="();<>|&\n")  # a newline also separates commands
    lexer.whitespace = " \t\r"
    lexer.whitespace_split = True
    current = []
    try:
        for token in lexer:
            if token in CONTROL or set(token) <= set("&|;()\n"):
                if current:
                    yield current
                current = []
            else:
                current.append(token)
    except ValueError:  # unbalanced quotes: fall back to a plain split
        current = line.split()
    if current:
        yield current


def is_git_push(words) -> bool:
    i = 0
    while i < len(words) and ("=" in words[i] and not words[i].startswith("-") or words[i] in ("sudo", "command", "env")):
        i += 1  # skip VAR=value prefixes and simple wrappers
    if i >= len(words) or words[i].rsplit("/", 1)[-1] != "git":
        return False
    i += 1
    while i < len(words) and words[i].startswith("-"):
        i += 2 if words[i] in GIT_OPTS_WITH_VALUE else 1
    return i < len(words) and words[i] == "push"


def main() -> None:
    event = json.load(sys.stdin)
    if event.get("tool_name") != "Bash":
        return
    command = event.get("tool_input", {}).get("command", "")
    if not any(is_git_push(words) for words in commands(command)):
        return
    if event.get("permission_mode") in NO_PROMPT_MODES:
        decision, reason = "deny", ("kstack: git push is blocked in this permission mode because it would not ask "
                                    "the operator. Tell the operator to push themselves with `! git push`.")
    else:
        decision, reason = "ask", "kstack: pushing needs the operator's yes (git push detected)."
    print(json.dumps({"hookSpecificOutput": {
        "hookEventName": "PreToolUse", "permissionDecision": decision, "permissionDecisionReason": reason}}))


if __name__ == "__main__":
    main()
