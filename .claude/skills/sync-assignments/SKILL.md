---
name: sync-assignments
description: Pull the Notion Assignments/Exams database into the Obsidian vault's tracker note. Use when Aryan says "sync assignments", "update assignments", "sync my deadlines", "what's due", "pull from notion", or asks to refresh assignment tracking. Notion is the only thing he still creates assignments in; everything else lives in Obsidian at ~/MBA.
---

# sync-assignments

Aryan creates and tracks assignments in **Notion**. Everything else — all coursework
notes — lives in the **Obsidian vault at `~/MBA`**. This skill is the one-way bridge:
Notion → vault. Run it whenever he asks.

**Notion is the source of truth. The vault note is a read-only mirror.** The note is
regenerated wholesale every run, so additions, deletions, status changes and date changes
all take care of themselves. Never edit `~/MBA/Assignments & Exams.md` by hand and never
write back to Notion from here.

---

## Rules

1. **One-way only.** Never create, update or delete a Notion row from this skill. If he
   wants a new assignment, he makes it in Notion; you re-sync afterwards.
2. **Never publish this.** The note is `publish: false`. It is personal study planning and
   contains no coursework prose. It must never reach `aryangupta1.github.io/MBA`, and it is
   not part of the website repo — it lives only in the vault.
3. **Never carry the lecturer's details across.** The `Courses` rows expose `Professor`,
   `Email`, `Location` and `Time`. None of them belong in the vault. Use only
   `Course Code`, `Name`, `Semester`, `Status`.
4. **Regenerate, don't merge.** Do not try to patch rows in the existing note.

---

## Procedure

### Step 1 — load the Notion tool

```
ToolSearch  query: "select:mcp__notion__notion-query-data-sources"
```

The MCP server is authenticated per-machine; if it errors, ask him to run `/mcp`.

### Step 2 — query the database

Data source: `collection://3097b336-873c-81f2-a506-000bcf539b96`  (**Assignments/Exams**)

```sql
SELECT Title, Type, Status, "date:Due Date:start", Course
FROM "collection://3097b336-873c-81f2-a506-000bcf539b96"
```

`Course` comes back as a JSON array of course-page URLs. Map the id to a code:

| Notion course id | Code |
| --- | --- |
| `3097b336873c80968073e1efcf72711d` | DMBA6001 |
| `3097b336873c80e0801fc3d2462d1cf9` | DMBA6002 |
| `3097b336873c80d3800df8c3f77b2a8b` | DMBA6004 |
| `3097b336873c80c0948dcc805089b071` | DMBA6008 |
| `3a17b336873c80c284a7cd6be4a60c4d` | DMBA6005 |

A row may have **no** course (general to-dos) — use `-`. A row may list **two** courses —
use the first. `Type` may be null — write `(untyped)`. A null due date — write `-`.

**A new subject will appear here eventually.** If a course id is not in the table above,
do not guess: query the Courses data source
(`collection://3097b336-873c-81b6-aa7c-000b6577c6c6`) for its `Course Code`, add a row to
`~/MBA/.mba-sync/courses.tsv`, and update this table.

### Step 3 — write the TSV

Write every row to `~/MBA/.mba-sync/assignments.tsv`, tab-separated, no header:

```
Title <TAB> Type <TAB> Status <TAB> Due (YYYY-MM-DD or -) <TAB> CourseCode (or -)
```

Take only the **date** part of the due timestamp. Use a quoted heredoc so titles
containing `$`, backticks or quotes survive intact. Titles are his words — copy verbatim,
typos included.

### Step 4 — render

```
python3 "${CLAUDE_PROJECT_DIR:-$PWD}/.claude/skills/sync-assignments/render_assignments.py"
```

Use the absolute form. A bare relative path breaks the moment the shell's working
directory has been changed to the vault, which happens often in this workflow.

It writes `~/MBA/Assignments & Exams.md`, snapshots the data to `assignments.prev.tsv`,
and prints a diff against the previous sync.

### Step 5 — verify, then report

```
python3 ~/MBA/.mba-sync/verify.py
```

Confirm the row count in the note matches the row count from Notion, then report to Aryan:

- how many rows synced, and **what changed since last time** (the script prints this)
- **what is still open**, soonest first
- anything **overdue** — the note marks these ⚠️

Lead with what is open and overdue. That is the reason he asked.

---

## Gotchas

- `notion-query-data-sources` is **metered** on this plan. One query per sync is fine;
  do not query per row.
- Status values are exactly `Not Started`, `In Progress`, `Complete`. A status group
  reshuffle in Notion changes these strings — if the "still open" list looks wrong, check
  them before assuming the script is broken.
- The note keeps a trailing section sourced from `~/MBA/.mba-sync/dashboard-callout.md`
  (a loose to-do captured from the Notion MBA dashboard page at migration). It is included
  verbatim if that file exists. It is **not** refreshed by this skill — if he wants it
  updated, re-read the dashboard page `3097b336-873c-8025-b728-d96b85cbfec0` and rewrite
  that file.
- `Exam` rows are supported by the schema but none existed at migration. They render like
  any other row; no special handling needed.
