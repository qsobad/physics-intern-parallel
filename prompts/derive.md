---
description: Analytical derivation for a target claim or open question, in a fresh-context sub-agent that uses only what is dispatched via a brief file. Writes derivations/D-NNN.md with the derivation, assumptions, and sanity checks.
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

Perform an analytical derivation. The `deriver` sub-agent works only from what you put in a brief file plus the workspace `problem.md`. You write the brief; you dispatch; you integrate.

## Steps

1. **Determine the next `D-NNN` number.** List `derivations/D-*.md` and add 1; zero-pad to 3 digits (`D-001`, `D-002`, …).

2. **Write the brief** at `derivations/.briefs/D-NNN-brief.md`. Include only:
   - The target claim or question, stated concretely.
   - Relevant **Established Results** from `research_log.md` the deriver may need (by ID and one-line restatement).
   - Relevant **Conventions** from `research_log.md`.
   - Specific reference file paths (`references/<id>.{md,pdf,tex}`) that bear on the target.
   - Any prior `D-NNN.md` or `C-NNN.md` whose result is a load-bearing input — by path, not by re-statement.

   **No steering, no priors.** Do not signal an expected answer or preferred direction.

3. **Dispatch the `deriver` sub-agent**, passing the brief path and the output path. See AGENTS.md §3 (Dispatch syntax) for the exact tool invocation. The deriver reads the brief, follows its role definition in `.pi/agents/deriver.md`, and writes `derivations/D-NNN.md` with the structured `## Summary` / `## Result` / `## Flags` at the top.

4. **Run the integration loop** when the deriver returns:
   - Read `## Summary` / `## Result` / `## Flags` from `derivations/D-NNN.md`.
   - Add or update a Working Claim in `research_log.md` citing `D-NNN`.
   - Disposition every flag in `notes/flags.md`.
   - Commit as `derive(D-NNN): <one-line summary>`.

5. **Next dispatch is `/review D-NNN`** unless the integration loop surfaced a reason to defer. Do not chain another `/derive` or `/compute` without intervening review.
