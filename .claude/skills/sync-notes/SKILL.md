---
name: sync-notes
description: Pull Aryan's Notion coursework notes down into the Obsidian vault at ~/MBA, without overwriting anything he wrote in Obsidian. Use when he says "sync notion", "sync my notes", "pull my notes from notion", "I've been writing in notion", or names a subject alongside Notion. This is the upstream half of the chain — publishing to the website is still sync-subject's job, and this skill hands off to it.
---

# sync-notes

Aryan writes coursework notes in **both** Notion and Obsidian, and intends to for a while.
He likes Notion's editor; the vault is where he is migrating to. This skill is the bridge
that keeps the vault current with Notion **without ever destroying Obsidian-only work**.

```
Notion  --sync-notes-->  Obsidian vault (~/MBA)  --sync-subject-->  week pages in this repo
         (this skill)         SOURCE OF TRUTH        (publishing)
```

The vault stays the single source of truth for publishing. Notion is an *input* to the
vault, not a second publishing source. **Nothing here ever writes to the repo**, and
nothing ever writes back to Notion.

---

## The four rules that outrank everything else

1. **Never overwrite a note Aryan edited in Obsidian.** Enforced in code by
   `apply_harvest.py`; see [Conflicts](#conflicts). If you find yourself about to pass
   `--force`, stop and ask him first — that flag exists for him to authorise, not for you
   to choose.
2. **One-way only.** Notion → vault. Never create, update or delete a Notion page from
   here, and never push vault edits back up.
3. **Never carry lecturer details** — no professor name, email, room or class time — into
   the vault, in any note, in any frontmatter. They were deliberately excluded at migration
   and this repo has a never-publish rule.
4. **`publish` is derived from Type, never invented.** `Pre-Live Session` → `publish: true`.
   Everything else — `Live Session`, `Assessment`, untyped — → `publish: false`. Downstream
   rulings in `sync-subject/subjects.json` (held-back notes, `Pre-Class Prep`) still apply
   at publish time and are **not** this skill's business to re-open.

---

## Files this skill owns

| Path | What |
| --- | --- |
| `reference/harvest_plan.py` | Scope resolution → `plan.json` + the fetch list |
| `reference/apply_harvest.py` | Convert + write, with the conflict guard |
| `reference/convert_core.py` | Notion markup → Obsidian markdown (canonical copy) |
| `reference/ingest.py` | Downloads a page's images before the URLs expire |

Data lives with the vault, not here:

| Path | What |
| --- | --- |
| `~/MBA/.mba-sync/raw/<notion_id>.txt` | Verbatim Notion dump, the rebuild source |
| `~/MBA/.mba-sync/notes-state.json` | Per-page `raw_sha` + `file_sha`. **The conflict guard's memory** |
| `~/MBA/.mba-sync/{courses,notebooks,notes}.tsv` | The Notion inventory |
| `~/MBA/.mba-sync/children.d/*.tsv` | Child pages found during harvest, one file per agent |

> `~/MBA` is **not** part of this repo and must never be committed to it.

---

## Setup check

Needs the Notion MCP server. If it errors, ask him to run `/mcp`.

Scripts are invoked by absolute path, because the working directory is routinely changed
to the vault mid-run:

```
python3 "${CLAUDE_PROJECT_DIR:-$PWD}/.claude/skills/sync-notes/reference/harvest_plan.py" …
```

---

## Phase 0 — Refresh the inventory *(one metered query)*

`notion-query-data-sources` is **metered on this plan.** One query per sync, no more.

| Database | Data source |
| --- | --- |
| Courses | `collection://3097b336-873c-81b6-aa7c-000b6577c6c6` |
| Notebooks | `collection://3097b336-873c-814d-b93f-000b3ee9948a` |
| Notes | `collection://3097b336-873c-816a-b24d-000b141a5afe` |

```sql
SELECT url, Name, Type, Notebook, Course, "Created Time" AS created, "Edited Time" AS edited
FROM "collection://3097b336-873c-816a-b24d-000b141a5afe"
ORDER BY "Edited Time" DESC
```

**Use these exact column names.** They are `"Created Time"` / `"Edited Time"`, not the
`date:…:start` form — that form is only for real `date` properties, and these two are
`created_time` / `last_edited_time` system properties. Getting it wrong costs a metered
query. Verified against the live schema 2026-08-19.

`url` comes back as `https://app.notion.com/<id>` — strip to the bare 32-char id. `Notebook`
and `Course` are JSON arrays of page URLs; take the first and strip it the same way.

Write the result to `~/MBA/.mba-sync/notes.tsv` as
`id <tab> name <tab> type <tab> notebook_id <tab> course_id <tab> created <tab> edited`,
with `-` for an empty notebook or course.
Refresh `courses.tsv` / `notebooks.tsv` only if a new course or week appeared — they change
about once a semester.

**Skip this phase entirely** if Aryan names a week that already exists and just wants its
content refreshed. The inventory is only needed to discover *new* notes.

---

## Phase 1 — Scope *(one question, then commit)*

```
python3 …/harvest_plan.py DMBA6008 [--week "Week 4"]
```

**Scope is course-at-a-time by default.** A whole-vault re-harvest is ~296 fetches and is
almost never what he means. If he says "sync notion" with no subject, ask which — or infer
it if the conversation has been about one subject, and say which you picked.

The plan prints `NEW` / `CHANGED` / `UNCHANGED` per note, from Notion's `Last edited time`.

> **Do not trust `--changed-only` for a real sync.** Notion does **not** bump a parent
> note's last-edited time when a *sub-page's* body is edited — and sub-pages are exactly
> where his lecture notes live. That flag is a fast triage pass, nothing more. The default
> re-fetches the whole scope and diffs on actual content, which is the honest answer.

---

## Phase 2 — Harvest *(fan out: one agent per note)*

Aryan has asked for parallelism here before. Dispatch one agent per top-level note.

Each agent must:

1. `notion-fetch` the page.
2. Write the body **verbatim** to `~/MBA/.mba-sync/raw/<notion_id>.txt`. No cleanup, no
   summarising, no fixing typos or spelling — the converter handles markup, and his
   Australian spelling and mid-sentence endings are preserved deliberately.
3. Immediately run `ingest.py` on that file. **Notion's image URLs are presigned and expire
   in ~300 seconds**, so this cannot be deferred to the end of the run.
4. Recurse into every `<page url=…>` child, to any depth, doing the same.
5. Append `childId <tab> parentId <tab> title` for each child to its **own**
   `children.d/<agent-id>.tsv` — never a shared file, or the writes race.

Attachment filenames use the **full** notion id. Truncated ids silently overwrote two
images during the migration; `publish_images.py` downstream now refuses to publish on a
collision.

---

## Phase 3 — Apply, with the conflict guard

```
python3 …/apply_harvest.py --dry-run     # always look first
python3 …/apply_harvest.py
```

Every page is classified against two independent hashes — did Notion change, and did the
vault file change since *this skill* last wrote it:

| Notion changed | Obsidian edited | Action |
| --- | --- | --- |
| no | no | `UNCHANGED` — nothing written |
| yes | no | `UPDATED` — safe overwrite |
| no | yes | `KEPT-LOCAL` — his edit stands; Notion had nothing new to say |
| **yes** | **yes** | **`CONFLICT`** — his file is left alone |

### Conflicts

On a conflict the vault file is **not touched**. Notion's version is parked beside it as
`<name>.notion-incoming.md`. Report it plainly, show him what each side says, and let him
decide — do not merge his academic prose yourself, and do not pick a winner.

`--force <notion_id>` overwrites despite local edits, backing the file up to
`<name>.local-backup.md` first. **Only on his explicit say-so.**

`--seed` adopts the vault as-is as the baseline and writes nothing. Needed once after any
out-of-band bulk change to the vault.

---

## Phase 4 — Verify

```
cd ~/MBA/.mba-sync && python3 verify.py
```

Six checks: coverage, empty notes, wikilinks, attachments, leftover Notion markup, publish
flags. **Gate 6 fails loudly if a `Live Session` or `Assessment` note is `publish: true`** —
that is the guard against publishing something he never meant to share.

Notes that are near-empty because they are *empty in Notion* are reported, not failed.
**Never generate filler for them.**

---

## Phase 5 — Hand off to publishing

Say what changed, then offer the second half of the chain:

> Pulled 4 changed notes into the vault for DMBA 6008 Week 4. Want me to publish it?

If he says yes, invoke **`sync-subject`**. It re-reads the vault, so it picks up
everything this skill just wrote with no extra plumbing. It runs its own six QA gates and
re-derives the quiz, Apply-it and study-path content for any week whose content moved.

**Do not publish automatically.** Pulling notes down and putting them on a public website
are different decisions, and the second one is his.

---

## Cost

One metered `notion-query-data-sources` call per sync. `notion-fetch` is not metered.
A one-course refresh is roughly 10–40 fetches; the whole vault is ~296.
