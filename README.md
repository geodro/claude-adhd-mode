# claude-adhd-mode

A working style for [Claude Code](https://claude.com/claude-code), tuned for ADHD brains.

Long sessions with an AI agent have a specific failure mode if you have ADHD: you get bored waiting, the agent answers with walls of text you stop reading, and then it hands you five open-ended decisions at once — right at the moment your attention is already gone.

This repo is a small set of rules that fixes that. It makes the agent:

- answer in **3 lines by default**, conclusion first;
- ask **one question at a time**, always with its own recommendation first, framed as yes/no;
- **decide everything reversible on its own**, and only ask about things that are hard to undo;
- tell you up front how long something will take, so you can **walk away** instead of watching it work;
- keep a **`NOW.md`** state file per project, so coming back after a break takes five seconds instead of five minutes;
- end every step with a single **`NEXT:`** line to grab onto.

Nothing here is ADHD-specific in a way that hurts anyone else — it's mostly just a less exhausting agent. But the defaults are chosen for the brain that runs out of executive function before it runs out of interest.

> **Not to be confused with** [UditAkhourii/adhd](https://github.com/UditAkhourii/adhd), which uses "ADHD" as an acronym for a parallel-divergent-ideation reasoning strategy. This repo is about the actual condition: making the agent usable when your attention is the bottleneck.

## Install

```sh
git clone https://github.com/<you>/claude-adhd-mode.git
cd claude-adhd-mode
./install.sh
```

The installer is non-destructive:

- symlinks `skills/focus` into `~/.claude/skills/focus`;
- appends one `@import` line to `~/.claude/CLAUDE.md` (creating it if missing) — your existing content is untouched;
- creates `~/.claude/state/` for the `NOW.md` files.

Because everything is symlinked, `git pull` updates your setup with no reinstall.

Running more than one Claude config directory? Point the installer at each one:

```sh
CLAUDE_CONFIG_DIR=~/.claude-work ./install.sh
```

Restart Claude Code, or start a new session, and it's live in every project.

## What's in here

| File | What it does |
|---|---|
| `CLAUDE.md` | The always-on rules. ~30 lines, loaded into context in every session, every project. |
| `skills/focus/SKILL.md` | The full protocol with examples — chunking, decision framing, the `NOW.md` format, the re-entry ritual. Loaded on demand, or with `/focus`. |
| `install.sh` | Symlinks the above into `~/.claude/`. |

Two files, because they do different jobs. `CLAUDE.md` is always in context, so it has to stay short. The skill holds the detail and only loads when it's relevant — when you say *"where were we"*, when you come back after a break, or when a task is about to turn into a pile of decisions.

## Control words

Say these at any point:

| You say | It does |
|---|---|
| `too much` | Compresses to 2 lines immediately, no apology. |
| `details` | Gives you the long version — only when you ask. |
| `where were we` | Reads `NOW.md`, answers in 3 lines. |
| `you do it` | Stops asking anything until the task is done or it hits something irreversible. |

## Making it yours

Edit `CLAUDE.md`. It's 30 lines of plain English — no config format, no schema. If a rule doesn't fit how you work, delete it. If the agent does something that drains you, write the rule that stops it.

Some knobs worth considering:

- **Autonomy.** The default is "decide everything reversible, announce it in one line". If you want more control, change that line to require confirmation at milestones.
- **Reply length.** 3 lines is the default. Some people want 1, some want 5.
- **State file.** If you'd rather have `NOW.md` inside the project repo (so it's shared with teammates or committed), change the path in the skill and add it to `.gitignore` if you don't want it tracked.

## Uninstall

```sh
rm ~/.claude/skills/focus
```

and delete the `@.../claude-adhd-mode/CLAUDE.md` line from `~/.claude/CLAUDE.md`.

## License

MIT.
