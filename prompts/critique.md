---
description: Strategic critique of the overall research state, in a fresh-context critic sub-agent. Identifies strategic drift, plan-viability issues, coherence problems, under-sourced claims, citation gaps.
args: "[optional focus from main agent]"
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

Run a strategic critique. The `critic` sub-agent reads `research_log.md` and `plan.md`, spot-checks artefacts as needed, and files findings in `critiques/CR-NNN.md`. Findings are proposals — you disposition each.

## Steps

1. **Determine the next `CR-NNN` number.** List `critiques/CR-*.md` and add 1; zero-pad.

2. **Collect one-line summaries of prior critiques** to pass to the new critic. For each existing `critiques/CR-MMM.md`, extract one line: the filed date and headline finding. This prevents repetition but does not leak full prior analyses.

3. **Dispatch the `critic` sub-agent**, passing the prior-critique one-liners and any focus from the user inline. See AGENTS.md §3 (Dispatch syntax) for the exact tool invocation. The critic reads `research_log.md` (esp. Established Results), `plan.md`, spot-checks artefacts as needed, follows its role definition in `.pi/agents/critic.md`, and writes `critiques/CR-NNN.md` with YAML frontmatter (`filed: YYYY-MM-DD`, `status: pending`), `## Findings`, and an empty `## Resolution`. The structured `## Summary` / `## Result` / `## Flags` goes at the top.

4. **Run the integration loop** when the critic returns:
   - Read `## Summary` / `## Result` / `## Flags` from `critiques/CR-NNN.md`.
   - **Do not act on findings unilaterally.** Disposition each finding inline in the critique file's `## Resolution` section (resolve / dismiss / defer with a reason). Update the YAML `status:` field accordingly.
   - For findings that imply a strategy-level change, re-invoke `/research-plan` after the critique commit lands.
   - Disposition any general flags in `notes/flags.md`.
   - Commit as `critique(CR-NNN): <one-line summary>`.

5. **Checks and balances.** Before acting on a major critique finding that would substantially change direction, seek a second opinion — another `/critique` or a confirming `/review` — per AGENTS.md §3.
