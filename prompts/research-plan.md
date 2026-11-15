---
description: Draft or update plan.md — the numbered research strategy. Forks a fresh-context planner sub-agent. HITL after return.
args: "[optional feedback or scope hints]"
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

Draft or update `plan.md` for the problem in `./problem.md`, using `survey.md` and `research_log.md` as inputs. The substantive work happens inside the `planner` sub-agent (fresh context).

## Steps

1. **Dispatch the `planner` sub-agent**, passing any user feedback or scope hints inline. See AGENTS.md §3 (Dispatch syntax) for the exact tool invocation. The planner reads `./problem.md`, `./survey.md` (if it exists), and `./research_log.md`; follows its role definition in `.pi/agents/planner.md`; and writes `./plan.md`. If `plan.md` already exists, the planner marks completed steps, drops or revises as warranted. The structured `## Summary` / `## Result` / `## Flags` goes at the top of `plan.md`.

2. **Run the integration loop** when the planner returns:
   - Read the `## Summary` / `## Result` / `## Flags` from `plan.md`.
   - Disposition every flag in `notes/flags.md`. Suggested Conventions/Sanity Checks from the planner go to the appropriate `research_log.md` sections.
   - Commit as `research-plan: <one-line summary>`.
   - **Present the plan to the user for approval.** This is the post-plan HITL gate — do not start dispatching `/derive` or `/compute` until the user confirms.

## Notes

- Targeted edits to `plan.md` (marking a step done, dropping an obsolete step, retitling) are handled by you directly without re-invoking this skill. Re-invoke only for strategy-level changes.
