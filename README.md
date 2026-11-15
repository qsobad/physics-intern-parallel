# physics-intern-parallel

One problem per directory.

    python3 run_autoresearch.py P-3

The command detaches and returns at once. Each problem runs inside
`runs/P-<n>/`, which holds only that problem's files, so a run for P-3 never
reads or writes P-4. Start the next problem with the same command and another
id. All problems share this one repository; a run directory is not its own
repository and is not committed.

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
  `notes/`, and `autoresearch.log`. Created on launch and gitignored, so it is
  not committed. Safe to delete; the statement survives in `problems/`.

The runner refuses to start unless `problems/P-<n>.md` exists. It copies
`prompts/`, `skills/`, `AGENTS.md`, and the statement into the run directory on
every launch, overwriting what is there, so launch a pass once. To start a pass
over, delete its `runs/P-<n>/` first. Output goes to
`runs/P-<n>/autoresearch.log`.

A finished pass stays in `runs/P-<n>/`. There is no archive step and no moving
of a finished pass anywhere else: the run directory is the pass's only copy.
Do not delete a `runs/P-<n>/` whose statement is not in `problems/`, or the
pass is gone. `runs/` is gitignored, so a pass that should survive a checkout
has to be copied out of it deliberately.

## What is shared

`prompts/`, `skills/`, and `AGENTS.md` are the method. They are copied into each
run directory at launch, so a run reads its own copy and not the originals.

The virtualenv is a symlink to `/data/projects/physics-intern/.venv`, read at
import time and not a second copy. A pass that needs a package the shared
environment lacks should say so in its log rather than install into it, since
every other pass imports from it.

Nothing else crosses a pass boundary. There is no root `problem.md`, no shared
`research_log.md`, and no archive step, because there is nothing to archive:
each pass already owns its directory.
