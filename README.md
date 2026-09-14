# Research

How we read, evaluate, and reuse papers for the project. Full rules: [`SYSTEM.md`](./SYSTEM.md). Why these particular papers, right now: [`reading-list-phase1.md`](./reading-list-phase1.md).

## Layout

```
papers.csv           every paper we know about — status, priority, decision (generated + hand-added rows)
search-log.md         searches that came up empty
candidates.md          papers worth reading later, not yet assigned
evidence/<slug>.md      one finished card per paper — the actual output of reading it
templates/               copy one of these to start a new card
scripts/build_index.py   regenerates papers.csv from evidence/*.md
```

## Quick start

1. Pick a paper from `papers.csv` with `status: unread`.
2. Branch off `main`: `paper/<slug>`.
3. Copy the matching template from `templates/` into `evidence/<slug>.md`.
4. Fill it in, push, open a PR (P0) or push straight to `main` (P1/P2).
5. See `SYSTEM.md` for the two-reader flow, priority levels, and everything else.
