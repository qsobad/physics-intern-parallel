# physics-intern-parallel

One problem per directory.

    python3 run_autoresearch.py P-3

The command detaches and returns at once. Each problem runs inside
`runs/P-<n>/`, and that directory is its own git repository: its branch is
named `P-<n>`, its index and lock live in its own `.git`, and its commits are
pushed to `refs/heads/P-<n>` on the shared remote. A run for P-3 never reads,
writes, or commits over P-4, so the two cannot block each other on a lock.
Start the next problem with the same command and another id.

This is a copy of the physics-intern method, changed in one place: the original
keeps the live problem at the repository root and archives the previous one
before the next can start, so two problems cannot run together.

The original workspace at `/data/projects/physics-intern` is not touched. A
problem that is already running there keeps running there.

## Layout

- `problems/P-<n>.md` — the problem statement. Write it here. It is copied into
  the run directory at launch and not modified after that.
- `runs/P-<n>/` — everything that problem produces: `problem.md`, `survey.md`,
  `plan.md`, `research_log.md`, `computations/`, `derivations/`, `critiques/`,
  `notes/`, and `autoresearch.log`. Created on launch. Safe to delete; the
  statement survives in `problems/`.
- `prompts/`, `skills/`, `AGENTS.md` — the method, copied into each run
  directory so a run does not depend on files outside itself.
- `.venv` — a symlink to `/data/projects/physics-intern/.venv`. Not a second copy.

The runner refuses to start unless `problems/P-<n>.md` exists.

A second launch of a pass that already has a `runs/P-<n>/` directory resumes
that run, because the runner infers its start point from the files already
there. To start a pass over, delete its `runs/P-<n>/` first.

## What is shared

Only the virtualenv, and it is read at import time. A pass that needs a package
the shared environment lacks should say so in its log rather than install into
the shared environment, since every other pass imports from it.

Nothing else crosses a pass boundary. There is no root `problem.md`, no shared
`research_log.md`, and no archive step, because there is nothing to archive:
each pass already owns its directory.
