#!/usr/bin/env bash
# Installs claude-adhd-mode into ~/.claude. Non-destructive: symlinks the skill,
# appends one import line to your CLAUDE.md, touches nothing else.
set -euo pipefail

REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CLAUDE_DIR="${CLAUDE_CONFIG_DIR:-$HOME/.claude}"
IMPORT_LINE="@$REPO/CLAUDE.md"

mkdir -p "$CLAUDE_DIR/skills" "$CLAUDE_DIR/state"

# 1. the focus skill
SKILL_LINK="$CLAUDE_DIR/skills/focus"
if [ -L "$SKILL_LINK" ]; then
  ln -sfn "$REPO/skills/focus" "$SKILL_LINK"
  echo "updated  $SKILL_LINK -> $REPO/skills/focus"
elif [ -e "$SKILL_LINK" ]; then
  echo "SKIPPED  $SKILL_LINK already exists and is not a symlink." >&2
  echo "         Move it aside and re-run, or point it at $REPO/skills/focus yourself." >&2
else
  ln -s "$REPO/skills/focus" "$SKILL_LINK"
  echo "linked   $SKILL_LINK -> $REPO/skills/focus"
fi

# 2. the always-on rules, imported into your CLAUDE.md
USER_MD="$CLAUDE_DIR/CLAUDE.md"
if [ -e "$USER_MD" ] && grep -qF "$IMPORT_LINE" "$USER_MD"; then
  echo "ok       $USER_MD already imports the rules"
else
  [ -e "$USER_MD" ] && printf '\n' >>"$USER_MD"
  printf '%s\n' "$IMPORT_LINE" >>"$USER_MD"
  echo "added    import line to $USER_MD"
fi

echo
echo "Done. Start a new Claude Code session — the rules load in every project,"
echo "and /focus gives you the full protocol."
