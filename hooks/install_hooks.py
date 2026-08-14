#!/usr/bin/env python3
"""Merge the claude-adhd-mode hooks into a settings.json, leaving the rest alone.

Idempotent: re-running updates the paths in place instead of stacking duplicates.
Follows symlinks, so a shared settings.json stays shared. Backs up to .bak first.
"""
import json
import os
import shutil
import sys

MARKER = "now_hook.py"

EVENTS = [
    ("UserPromptSubmit", None, "inject", "Recalling where we left off"),
    ("PostToolUse", "Edit|Write|NotebookEdit", "mark", None),
    ("Stop", None, "check", None),
]


def entry(command, status):
    hook = {"type": "command", "command": command}
    if status:
        hook["statusMessage"] = status
    return hook


def main():
    settings_path = sys.argv[1]
    repo = os.environ.get("REPO") or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    script = os.path.join(repo, "hooks", "now_hook.py")

    settings = {}
    if os.path.exists(settings_path):
        shutil.copyfile(settings_path, settings_path + ".bak")
        try:
            with open(settings_path, encoding="utf-8") as fh:
                settings = json.load(fh) or {}
        except ValueError:
            print("SKIPPED  %s is not valid JSON; not touching it." % settings_path, file=sys.stderr)
            return 1

    hooks = settings.setdefault("hooks", {})
    for event, matcher, mode, status in EVENTS:
        command = "python3 %s %s" % (json.dumps(script), mode)
        groups = hooks.setdefault(event, [])
        # Drop any group we installed before, then add the current one.
        groups[:] = [
            g for g in groups
            if not any(MARKER in (h or {}).get("command", "") for h in g.get("hooks", []))
        ]
        group = {"hooks": [entry(command, status)]}
        if matcher:
            group["matcher"] = matcher
        groups.append(group)

    with open(settings_path, "w", encoding="utf-8") as fh:
        json.dump(settings, fh, indent=2)
        fh.write("\n")
    print("hooks    wired into %s" % settings_path)
    return 0


if __name__ == "__main__":
    sys.exit(main())
