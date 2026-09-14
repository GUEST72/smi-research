# How We're Handling Research Papers This Year

Team — this is the system we're using so that when one of us reads a paper, what matters gets captured in a way everyone else can actually find and trust, without turning every paper into a second writing assignment.

## Priority levels

Every paper gets one of three levels — not based on how good the paper is, but on how much it affects what we're building right now.

- **P0 — Core.** Directly shapes a decision we're making now. Read deeply, pull out real evidence, make a call.
- **P1 — Relevant.** Tied to a specific piece of the system, but doesn't define it. One or two solid findings is enough.
- **P2 — Background.** Worth knowing, not urgent. One paragraph, one useful point, move on.

Levels aren't fixed. When we move into a new phase, some P2 papers become P0 — when that happens, treat it as a fresh P0 read, not a relabel.

## What reading a paper actually produces

Not a summary. Not a rewrite of the abstract. Every paper produces an **Evidence Card**:

```
Paper: <title>
Authors: <authors>
Year: <year>
Link: <link>
Slug: <slug>
Priority: P0 / P1 / P2
Status: unread / assigned / in-review / done / superseded

What we take from it:
-

Evidence:
Claim: "..."
Where: [page / section / table / figure]
Why it matters to us:
-
(one block per claim that actually changes something — don't pad, don't cut a real one to fit)

What we'd reuse directly:
What we would NOT copy as-is:

Decision: KEEP / ADAPT / REJECT / DEFER
Why:

Outcome (filled in later, once we've actually tried it):
What happened when we built it:
Did the decision hold up?
```

P0 gets the full card. P1 gets just "Evidence" + "Decision." P2 is one claim, one location, one line on why it might matter later.

## The one rule that matters most

**No claim goes in without saying exactly where it came from.** "This works better with context" is useless six months from now. "Table 3 shows a 6-point gain with context included" is something we can check and build on.

And don't assume a result transfers to us. A paper's numbers came from its own data and setup. If the dataset or task is genuinely different from ours, say so in the card instead of quietly borrowing the number.

## How the GitHub repo is structured

```
research/
├── README.md
├── SYSTEM.md              ← this document
├── papers.csv             ← every paper we know about: slug, title, authors, year, link, priority, status, decision
├── search-log.md          ← searches that came up empty
├── candidates.md          ← papers worth reading later, not yet assigned
├── evidence/
│   └── <slug>.md          ← one FINAL file per paper — only finished, reviewed cards live here
├── templates/
│   ├── p0-card.md
│   ├── p1-card.md
│   └── p2-note.md
└── scripts/
    └── build_index.py     ← reads evidence/*.md, fills in papers.csv's status/decision columns
```

One person creates the repo and adds the rest of us as collaborators — that's a five-minute, one-time job for whoever gets to it first.

Every paper gets a **slug**: first author's last name + year, lowercase, hyphenated — `shriberg-2004`, `zelasko-2021`. If two would collide, add a short word — `zelasko-2021-context`. The slug is used everywhere: the filename, the branch name, the row in `papers.csv`. Nothing else needs its own naming scheme.

`evidence/` only ever holds finished work. There's no `drafts/` folder sitting on `main` — drafts live on personal branches and never get merged in as separate files, so `evidence/` never fills up with half-finished or duplicate copies.

## Adding a paper to the list

Before anyone reads it, a paper gets one row in `papers.csv` — slug, title, authors, year, link, priority, status: `unread`. Small, low-risk edit, straight to `main`, no branch needed. (If two people happen to add a row at the same time and git flags a conflict, it's just two new lines — keep both, that's not a real conflict.) This is also the entry point for a paper someone stumbles on while reading something else — a row here if we already know its priority, or a line in `candidates.md` if we're not sure yet.

## Reading and submitting one paper

This is the flow for P1, P2, and any P0 paper assigned to a single person.

1. Branch off `main`: `paper/<slug>` — e.g. `paper/zelasko-2021`.
2. Copy the right template (`templates/p0-card.md`, `p1-card.md`, or `p2-note.md`) into `evidence/<slug>.md` on that branch.
3. Read, fill it in, commit as you go — the commit history doesn't need to be tidy, this isn't what matters later.
4. Push the branch.
5. **P0 / P1 / P2:** open a pull request. Someone else reviews it against the checks in "Keeping each other honest," then merges.
7. Once it's on `main`, `papers.csv` picks up the new status and decision (see "One-time setup" below for making this automatic).
8. Delete the branch.

## When two people are assigned the same paper

Two readers means two branches, kept apart on purpose so neither can see or overwrite the other's notes until both are actually done.

1. Each creates their own branch: `paper/<slug>-<initials>` — e.g. `paper/zelasko-2021-ma` and `paper/zelasko-2021-yb`.
2. Each fills in their own copy at `evidence/<slug>-<initials>.md` — a different filename, so there's no way to collide, no merge conflict possible, and no temptation to peek at a file that isn't finished yet.
3. Both push their branch. Neither opens a PR into `main` — these are working drafts, not the deliverable.
4. Once both are done, the two readers sit down together, branch off `main` one more time — `paper/<slug>-merge` — and write the single real file, `evidence/<slug>.md`, by combining the two drafts:
   - Claims both drafts agree on go in as-is.
   - Claims that differ get five minutes of discussion, and the merged file records which reading won and why, not just the winning claim on its own.
5. Push `paper/<slug>-merge`, open one PR, both readers listed on it. This is the PR that actually gets reviewed and merged.
6. The two original draft branches never get merged into `main` — once the merge PR lands, delete both. They did their job and don't need to stick around.

## Fixing or updating something later

A card isn't frozen once it's merged. If a later paper or an actual experiment changes what we think, that's a normal edit: branch off `main`, update `evidence/<slug>.md`, small PR, merge — with one line added at the top noting what changed and why, instead of quietly overwriting the old claim, so we can see our own understanding shift over the year, not just its current state.

Priority and status changes work the same way but skip the ceremony — one field in one file is small enough to commit straight to `main`.

## How much time this should take

P0: a few hours, card included. P1: an hour or two. P2: under an hour. If a card turns into an essay, that's a sign the process broke, not a sign of thoroughness.

## Keeping each other honest

P0 decisions get a second pair of eyes before they're final — not to grade the writing, just to check the claim is really in the source, the conclusion isn't a stretch, and we're not treating a different dataset's result as our own.

P2 notes don't need any of that. Write it, done.

## What we're not doing

- Rewriting papers section by section
- Collecting every number a paper has "just in case"
- Copying an architecture because it worked somewhere else
- Writing a claim and forgetting where it came from
- Deciding once and never checking whether it actually held up

## The three questions

Every card, every decision, should answer: **What are we claiming? Where's the evidence? What did we decide to do about it?**

That's the system.
