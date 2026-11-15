---
description: Computation for a target claim, in a fresh-context sub-agent that uses only what is dispatched via a brief file. Cadabra2 for tensor algebra, Lean 4 + mathlib for proofs, NumPy and SymPy for numerical spot-checks. Disagreement between backends is flagged.
args: <target claim>
section: PhysicsIntern Workflows
topLevelCli: true
---

## 0. Tool discipline (read first)

Tool names are literal and lowercase. Use only tools visible in the current tool set.

- File I/O: `read`, `write`, `edit` (not `Read`/`Write`/`Edit`).
- Shell: `bash` (not `Bash`). Pass an explicit timeout for any long-running command.
- Search: `grep`, `find`, `ls`. Web: `web_search`, `fetch_content` (from the `pi-web-access` package).
- Sub-agent dispatch: `subagent` (from the `pi-subagents` package). Do not use `Task` — that tool does not exist here.
- To ask the user a question, write plain chat text and wait for the next user message. Do not call non-existent tools like `ask_user_question`.
- If a tool returns `Tool not found`, do not retry the same invalid call — map to the canonical visible tool, or record the capability as blocked and continue with a written artefact.

Perform symbolic + numerical computation. The `computer` sub-agent writes a script, executes it, and captures the output; you write the brief and integrate the result.

## Steps

1. **Determine the next `C-NNN` number.** List `computations/C-*.md` and add 1; zero-pad to 3 digits.

2. **Write the brief** at `computations/.briefs/C-NNN-brief.md`. Include only:
   - The target claim or quantity to compute, stated concretely.
   - Relevant **Established Results** from `research_log.md` (by ID and one-line restatement).
   - Relevant **Conventions** from `research_log.md` (units, signatures, normalizations).
   - Specific reference file paths (`references/<id>.{md,pdf,tex}`) that bear on the target.
   - Any prior `D-NNN.md` or `C-NNN.md` whose result is a load-bearing input — by path, not by re-statement.
   - Any prior `data/<slug>.*` files the computer may reuse — by path only.

   **No steering, no priors.** Do not signal an expected answer or preferred direction.

3. **Dispatch the `computer` sub-agent**, passing the brief path and the output path. See AGENTS.md §3 (Dispatch syntax) for the exact tool invocation. The computer reads the brief, follows its role definition in `.pi/agents/computer.md`, runs both symbolic and numerical paths together when feasible (flagging disagreement), writes `computations/C-NNN.py` and `computations/C-NNN.md`, and captures stdout+stderr to `computations/C-NNN.out`.

4. **Run the integration loop** when the computer returns:
   - Read `## Summary` / `## Result` / `## Flags` from `computations/C-NNN.md`.
   - Add or update a Working Claim in `research_log.md` citing `C-NNN`.
   - Note any new `data/<slug>.*` files mentioned in `## Data outputs` in `research_log.md` Conventions or near the relevant claim.
   - Disposition every flag in `notes/flags.md`.
   - Commit as `compute(C-NNN): <one-line summary>` — include the `.py` script and the `.out` log in the commit.

5. **Next dispatch is `/review C-NNN`** unless the integration loop surfaced a reason to defer.
