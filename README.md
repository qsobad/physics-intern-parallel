# physics-intern-parallel

One problem per directory. `run_parallel.sh` starts them all at once, and a
run for P-3 never reads or writes P-4.

This is a copy of the physics-intern method, changed in one place: the original
keeps the live problem at the repository root and archives the previous one
before the next can start, so two problems cannot run together. Here each
problem runs inside `runs/P-<n>/`, which is a complete workspace of its own.

The original workspace at `/data/projects/physics-intern` is not touched. A
problem that is already running there keeps running there.

## Layout

- `problems/P-<n>.md` — the problem statement. Write it here. It is copied into
  the run directory at launch and not modified after that.
- `runs/P-<n>/` — everything that problem produces: `problem.md`, `survey.md`,
  `plan.md`, `research_log.md`, `computations/`, `derivations/`, `critiques/`,
  `notes/`. Created on launch. Safe to delete; the statement survives in
  `problems/`.
- `prompts/`, `skills/`, `AGENTS.md` — the method, copied into each run
  directory so a run does not depend on files outside itself.
- `.venv` — a symlink to `/data/projects/physics-intern/.venv`. Not a second copy.

## Run

```bash
# one problem
./run_one.sh P-3

# several at once
./run_parallel.sh P-3 P-4 P-5
```

`run_one.sh` refuses to start unless `problems/P-<n>.md` exists. Each pass
appends to its own `runs/P-<n>/autoresearch.log`. `run_parallel.sh` prints the
pid of each pass and returns immediately; the passes keep running.

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
