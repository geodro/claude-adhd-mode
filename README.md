# claude-adhd-mode

> A working style for [Claude Code](https://claude.com/claude-code), tuned for
> ADHD. Short answers, one question at a time, and an agent that finishes the
> job instead of handing it back to you.

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Claude Code](https://img.shields.io/badge/for-Claude%20Code-d97757)](https://claude.com/claude-code)

I wrote this because long sessions with an agent kept wearing me out. Answers I stopped reading halfway through, five decisions at once right when my attention was gone, "done" on work nobody had checked, and waits I couldn't walk away from.
No plugin, no config format. Run `./install.sh` once and every Claude Code session, in every project, picks up the rules.

## Who it's for

Anyone whose attention runs out before the work does. Your attention is what gets used up in a session, so every rule here is there to save it. Nothing in it gets in the way if you don't have ADHD, you just get an agent that's easier to work with.

## Features

### Answers short enough to read

- ✂️ **Three lines by default.** The conclusion first, no preamble, no list of options it isn't going to take. Say `details` for the long version.
- 🎯 **One question at a time.** It gives its own pick first and asks yes or no, so you can answer without thinking it through.
- 🗣️ **It answers in the language you wrote in.**

### It decides what can be undone, and asks about the rest

- 🧭 **Reversible choices are its job.** Names, structure, libraries, approach. It picks one, tells you in a line and carries on. If you say "I don't know" or say nothing, it decides instead of asking again.
- 🛑 **Irreversible ones wait for you.** Deletions, deploys, money, real data, anything public. Git as well: it never commits, pushes or opens a PR by itself.
- 🚦 **Control words.** `too much`, `details`, `where were we` and `you do it` change how it behaves right away.

### Proof instead of "should work"

- ✅ **Nothing is called green without evidence.** It runs the checks itself and quotes what they printed, and it won't ask you to read the logs.
- 📊 **A confidence score when a job is done.** One line saying how sure it is, what that rests on and what it didn't verify.
- ⚡ **Your message goes first.** If you write while it's working, it answers before its next step.

### A pace you can walk away from

- ⏱️ **It tells you how long up front**, so you know when it's safe to go make a coffee.
- 👉 **Every step ends with a `NEXT:` line**, one concrete thing to pick up when you get back.
- 🧪 **Features come in phases you can test.** It builds one, checks it in a real browser the way you would, tells you what to click, and waits for your go before the next.
- 📝 **Optional `NOW.md`.** Opt-in hooks keep a 12 line state file per project, so tomorrow's session starts where today's stopped.

### Code you can follow after a break

- 🧹 **YAGNI and KISS.** No abstractions for needs that don't exist yet, no clever code you have to work out again later.
- 🔁 **Reuse before writing**, and at least one small test wherever logic branches, parses, or handles money or security.
- 💬 **Comments say why, not what.** Functions fit on one screen, and it doesn't tidy up unrelated code halfway through a task.

> **Not to be confused with** [UditAkhourii/adhd](https://github.com/UditAkhourii/adhd), which uses "ADHD" as an acronym for a reasoning strategy. This repo is about the actual condition.

## Install

```sh
git clone https://github.com/geodro/claude-adhd-mode.git
cd claude-adhd-mode
./install.sh
```

The installer doesn't overwrite anything. It:

- symlinks `skills/adhd` into `~/.claude/skills/adhd`;
- appends one `@import` line to `~/.claude/CLAUDE.md`, creating the file if needed and leaving what's already there alone;
- creates `~/.claude/state/` for the `NOW.md` files.

Everything is symlinked, so a `git pull` updates you without reinstalling.

If you use more than one Claude config directory, run it once for each:

```sh
CLAUDE_CONFIG_DIR=~/.claude-work ./install.sh
```

Start a new Claude Code session and it's active in every project.

## What's in here

| File | What it does |
|---|---|
| `CLAUDE.md` | The always-on rules, about 50 lines, loaded into every session in every project. |
| `skills/adhd/SKILL.md` | The full protocol with examples: chunking, decision framing, the `NOW.md` format, the re-entry ritual. Loaded when needed, or with `/adhd`. |
| `hooks/now_hook.py` | Three hooks that keep `NOW.md` up to date. Python 3, no dependencies. |
| `install.sh` | Symlinks the above into `~/.claude/` and wires up the hooks. |

There are two files because they do different jobs. `CLAUDE.md` is always in context, so it has to stay short. The skill holds the detail and only loads when it's useful: when you say *"where were we"*, when you come back after a break, or when a task is about to turn into a pile of decisions.

## The NOW.md file (optional)

Off by default. Turn it on with `./install.sh --hooks` and off with `./install.sh --remove-hooks`.

Each project gets `~/.claude/state/<project>/NOW.md` (under your `CLAUDE_CONFIG_DIR` if you set one) with what's happening now, the next action, what's blocked and a short list of what's done. It lives outside your repo, so it never shows up in `git status`. It's read into context on your first message of a session, and the agent can't finish a turn while there's work it hasn't written down.

It's there for one thing: the conversation doesn't carry over between sessions. Open the project tomorrow and the agent knows nothing about today unless this file exists. If your work often spans several days, that's the difference between picking up and explaining everything again.

If you usually finish in one sitting, or you'd rather keep track yourself, leave it off.

## Control words

Say these at any point:

| You say | It does |
|---|---|
| `too much` | Cuts the answer to 2 lines, no apology. |
| `details` | Gives you the long version, only when you ask. |
| `where were we` | Reads `NOW.md` and answers in 3 lines. |
| `you do it` | Stops asking anything until the task is done or it reaches something irreversible. |

## Making it yours

Edit `CLAUDE.md`. It's plain English, no config format or schema. Delete any rule that doesn't fit how you work, and when the agent does something that drains you, add a rule against it.

A few things worth adjusting:

- **Autonomy.** By default it decides everything reversible and tells you in one line. If you want more control, change that line so it asks at milestones.
- **Reply length.** 3 lines is the default. Some people want 1, some want 5.
- **State file.** If you'd rather keep `NOW.md` in the project repo, to share it or commit it, change the path in the skill, and add it to `.gitignore` if it shouldn't be tracked.

## Uninstall

```sh
rm ~/.claude/skills/adhd
```

Then delete the `@.../claude-adhd-mode/CLAUDE.md` line from `~/.claude/CLAUDE.md`.

## License

MIT.
