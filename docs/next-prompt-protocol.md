# The `next-prompt.md` protocol

`next-prompt.md` is a rolling handoff note between Claude Code sessions. Each session
reads it at the start and rewrites it at the end, so the next session begins with the
context the last one had.

## How it is injected

A `SessionStart` hook runs at the beginning of every session:

```
.claude/settings.json          hook registration
.claude/hooks/load-next-prompt.sh   reads next-prompt.md, emits it as additionalContext
```

The script resolves the repo root from **`BASH_SOURCE`**, not from `CLAUDE_PROJECT_DIR`,
reads `next-prompt.md`, wraps it in a short preamble, and returns:

```json
{ "hookSpecificOutput": {
    "hookEventName": "SessionStart",
    "additionalContext": "…preamble…\n--- BEGIN next-prompt.md ---\n…file…\n--- END next-prompt.md ---" } }
```

It exits 0 and emits nothing when the file is missing or blank, so a broken or absent
handoff never blocks a session.

### When it silently stopped firing (2026-08-05 → 2026-08-15)

The hook produced nothing for ten days while the script itself ran perfectly by hand. The
cause was in the **registration, not the script**: `settings.json` invoked it as

```
bash "$CLAUDE_PROJECT_DIR/.claude/hooks/load-next-prompt.sh"
```

and `CLAUDE_PROJECT_DIR` is only set when the harness chooses to export it. Unset, that
expands to `/.claude/hooks/load-next-prompt.sh`, and bash exits **127** before a single line
of the script runs. Reproduce the old failure with:

```sh
env -u CLAUDE_PROJECT_DIR bash -c 'bash "$CLAUDE_PROJECT_DIR/.claude/hooks/load-next-prompt.sh"'
```

Both ends are now defensive: the command falls back to `${CLAUDE_PROJECT_DIR:-$PWD}`, and
the script derives its own root from `BASH_SOURCE` regardless.

**The general lesson: a hook that fails is indistinguishable from a hook that never ran** —
the failure was in the registration, and testing the script by hand could never reveal it.
Test the *command string* from `settings.json`, not just the script it names.

A firing log was added here to close that gap and removed the same day. **Do not add one
back.** This hook runs at session start behind a 10s timeout, so anything that can block —
a file write needing approval, a network call, a prompt — risks holding up the session. The
hook must do nothing but read `next-prompt.md` and write stdout. Whether it fired is already
observable: the note either appears in context or it does not.

If the note does not appear, the hook is still not being invoked. Ask the user to open
`/hooks` once (which reloads hook config, and is where project-scope hooks are reviewed) or
restart the session; the settings watcher only picks up `.claude/` changes made while it is
already watching, and a project hook may be awaiting approval. **That is a user action — it
cannot be done from inside a session.**

## The rules

1. **Read it first.** Treat `next-prompt.md` as the session's opening agenda.
2. **It is binding** — follow it unless the user redirects.
3. **The escape hatch is `Adhoc chat, ignore next prompt`.** If that phrase appears in the
   user's message, ignore the agenda entirely, answer the question asked, and leave the
   file unchanged unless asked to update it.
4. **An explicit user request always outranks the file.** If the user asks for something
   else, do that; note anything you displaced in the file before you finish.
5. **Every session updates the file before it ends** — including sessions that finished
   everything (say so explicitly rather than leaving stale tasks).

## What to write

Keep it short enough to read in thirty seconds. It is a handoff, not a log — git already
holds the history.

```markdown
# Next prompt

**Last updated:** YYYY-MM-DD
**Left by:** <one line on what this session did>

## Current focus
<the single thing that matters next, or "nothing in flight">

## Do first
1. <concrete first action>

## Open threads
- [ ] <unfinished work, with enough context to resume cold>

## Do not
- <traps, dead ends, and things the user has ruled out>

## Notes for the next session
<anything discovered that is not obvious from the code>
```

Guidance:

- **Write for someone with no memory of this session.** Name files and paths; do not say
  "the fix we discussed".
- **Absolute dates**, never "yesterday" or "last week".
- **Carry forward or close every open thread.** If an item is done, delete it. If it was
  abandoned, move it to *Do not* with the reason.
- **Record decisions and their reasons**, not just outcomes — the reason is what stops the
  next session relitigating it.
- Do not paste large diffs, file contents, or command output.
- Do not put anything in it that belongs in `docs/` — a durable convention goes in the
  docs; only in-flight state goes here.

## Scope

`next-prompt.md` is checked into the repo and is repo-scoped, so it survives across
machines and clones. It is internal — it is excluded from search engines by `robots.txt`
and is never linked from a reader-facing page.
