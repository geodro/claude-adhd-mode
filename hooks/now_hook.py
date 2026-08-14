#!/usr/bin/env python3
"""claude-adhd-mode — keeps NOW.md current without anyone having to remember.

Three modes, wired to three hook events in settings.json:

  inject  (UserPromptSubmit) once per session, feed NOW.md into context so
          picking up after a break costs the user nothing.
  mark    (PostToolUse: Edit|Write) note that real work happened.
  check   (Stop) if work happened and NOW.md has gone stale, block the stop
          once and ask the agent to update it.

Python 3 only, no dependencies.
"""
import json
import os
import sys
import time

# Don't nag if NOW.md was updated this recently (seconds).
STALE_AFTER = 600


def state_dir_for(cwd):
    cfg = os.environ.get("CLAUDE_CONFIG_DIR") or os.path.expanduser("~/.claude")
    slug = os.path.abspath(cwd).replace(os.sep, "-")
    return os.path.join(cfg, "state", slug)


def emit(obj):
    json.dump(obj, sys.stdout)
    sys.stdout.write("\n")


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else ""
    try:
        data = json.load(sys.stdin)
    except Exception:
        data = {}

    directory = state_dir_for(data.get("cwd") or os.getcwd())
    now_md = os.path.join(directory, "NOW.md")
    session = data.get("session_id") or "nosession"

    if mode == "inject":
        seen = os.path.join(directory, ".seen-" + session)
        if not os.path.exists(now_md) or os.path.exists(seen):
            return
        os.makedirs(directory, exist_ok=True)
        open(seen, "w").close()
        with open(now_md, encoding="utf-8") as fh:
            body = fh.read().strip()
        context = (
            "Session state carried over from earlier work (claude-adhd-mode). "
            "This is where you left off — resume from here instead of re-reading "
            "the transcript, and don't ask the user to remind you.\n"
            "File: %s\n\n%s" % (now_md, body)
        )
        payload = {
            "hookEventName": "UserPromptSubmit",
            "additionalContext": context,
        }
        emit({"hookSpecificOutput": payload, "additionalContext": context})
        return

    if mode == "mark":
        edited = (data.get("tool_input") or {}).get("file_path") or ""
        # Writing NOW.md itself is the thing that clears the debt, not new debt.
        if edited and os.path.abspath(edited) == os.path.abspath(now_md):
            return
        os.makedirs(directory, exist_ok=True)
        open(os.path.join(directory, ".dirty-" + session), "w").close()
        return

    if mode == "check":
        dirty = os.path.join(directory, ".dirty-" + session)
        if not os.path.exists(dirty):
            return
        if os.path.exists(now_md) and time.time() - os.path.getmtime(now_md) < STALE_AFTER:
            return
        # Clear first: ask once per batch of work, never twice in a row.
        try:
            os.remove(dirty)
        except OSError:
            return
        emit({
            "decision": "block",
            "reason": (
                "Files changed since %s was last updated. Rewrite the whole file now — "
                "don't edit it in place, sections must replace rather than accumulate. "
                "Headings Now / Next / Blocked / Done in English, body in the user's "
                "language only, 12 lines total, Done at most 3. Then close your reply "
                "with the NEXT: line. This is bookkeeping — don't re-explain it to the "
                "user." % now_md
            ),
        })
        return


if __name__ == "__main__":
    main()
