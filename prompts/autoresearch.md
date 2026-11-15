---
description: Run the research pipeline autonomously without human-in-the-loop gates. Can only be invoked by the user.
args: "[max-iterations=N] [max-derivations=N] [start-from=survey|plan|loop|finalize]"
section: PhysicsIntern Workflows
---

## 0. Tool discipline (read first)

Tool names are literal and lowercase. Use only tools visible in the current tool set.

- File I/O: `read`, `write`, `edit` (not `Read`/`Write`/`Edit`).
- Shell: `bash` (not `Bash`). Pass an explicit timeout for any long-running command.
- Search: `grep`, `find`, `ls`. Web: `web_search`, `fetch_content` (from the `pi-web-access` package).
- Sub-agent dispatch: `subagent` (from the `pi-subagents` package). Do not use `Task` — that tool does not exist here.
- To ask the user a question, write plain chat text and wait for the next user message. Do not call non-existent tools like `ask_user_question`.
- If a tool returns `Tool not found`, do not retry the same invalid call — map to the canonical visible tool, or record the capability as blocked and continue with a written artefact.

You work in **autoresearch mode**. Drive the research pipeline from the current workspace state to completion, without pausing for user approval at the three HITL gates of normal flow.

This is a deliberate, scoped deviation from the normal methodology. It is **only** safe when the user has high prior confidence that the pipeline will not need course correction (testing the methodology, simple problems with a known answer shape, methodology validation runs). The user invokes this skill having accepted the named failure modes below.

This skill runs in the **main-agent context** — it drives the loop. Each step still dispatches the relevant sub-agent in fresh context.

Common args:
- `max-iterations=N` — total sub-agent dispatch cap. Default: 30.
- `max-derivations=N` — combined `/derive` + `/compute` cap. Default: 12.
- `start-from=survey|plan|loop|finalize` — explicit resume point. Default: infer from files on disk (no `survey.md` → start at `/survey`; no `plan.md` → start at `/research-plan`; otherwise enter the dispatch loop).

## Prerequisite: problem statement

Before the loop proper, confirm `problem.md` exists and has been filled in — its `### Problem setup` and `### Main question` sections must not still hold the skeleton placeholder text. If they do, halt and tell the user to fill in `problem.md`.

## What changes vs. normal flow

Normal flow has the main agent pause for user approval at three gates:
1. After `/survey`, before `/research-plan`.
2. After `/research-plan`, before plan execution.
3. Before any strategy-level plan rewrite (re-invoking `/research-plan`).

In autoresearch mode the main agent **skips these gates** and proceeds, recording each skipped decision in `notes/auto-decisions.md` (see schema below).

Everything else stays the same: the integration loop (AGENTS.md §3) runs after every sub-agent return, sub-agents remain fresh-context, `## Flags` are dispositioned in `notes/flags.md`, commits land per integration step.


## Waiting on a sub-agent

When you wait for a dispatched sub-agent, pass the maximum the tool allows, one hour. A derivation or a computation legitimately runs longer than a few minutes. If the wait returns because the time elapsed and the child is still running, wait again for the same maximum. Do not cancel it, do not re-dispatch it, and do not write its artefact yourself. Cancel only when the child has failed or its artefact is already on disk. A cancelled child writes nothing, and the run then ends with that step missing.

## Auto-decisions log

Append one block to `notes/auto-decisions.md` at every gate the main agent skipped. Create the file if it does not exist.

```markdown
## <ISO date+time> — <gate name>

- **Decision:** <what the main agent decided>
- **Reasoning:** <why it was safe to proceed without user input>
- **Would have asked:** "<the question that would have been put to the user in HITL mode>"
- **Inputs considered:** <files / claim IDs / sources / sub-agent ## Summary lines that the decision rested on>
```

Gate names to use (use these exact strings so the audit skill can grep them):

- `Post-survey gate` — proceeding from `/survey` to `/research-plan`.
- `Framing gate` — a load-bearing disagreement was found in `survey.md`. Logged after `/research-plan` returns. The block lists every reading the plan carries and states that none was dropped. It does not record a choice between them. Dropping a reading later is a strategy-level change and is re-logged under `Pre-strategy-change gate`.
- `Post-plan gate` — proceeding from `/research-plan` into the first dispatch.
- `Pre-strategy-change gate` — re-invoking `/research-plan` for a strategy shift (after the second critique, or when revising a prior framing decision).
- `Refutation gate` — acting on a `/review` refutation after the second-opinion review agrees.
- `Pre-finalize gate` — proceeding to `/finalize`.

The log is **not** committed as a separate step. Bundle the new block into the next integration commit (the dispatch the gate authorised) alongside the integration loop's other files.


## End-of-run report

Print to the user:

- **Outcome:** completed / halted-on-trigger-N (one line)
- **Iterations used:** k / max-iterations
- **Derivations + computations used:** k / max-derivations
- **Artefacts produced:** D-NNN list, C-NNN list, CR-NNN list
- **Established Results:** count, with one-liner each
- **Working Claims still open:** count, with one-liner each and current status
- **Dead Ends added:** count
- **Auto-decisions logged:** count, with a link to `notes/auto-decisions.md`
- **Commits landed:** count (one per integration step)
- **Recommended next step for the user:**
  - If completed: read `answer.md` and audit `notes/auto-decisions.md` for any decision the user disagrees with.
  - If halted: pointer to the artefact / claim / file the user should look at first.

## Loop pseudocode (for the main agent)

```
init:
  ensure notes/auto-decisions.md exists (create with a one-line header if not).
  if problem.md still has skeleton placeholder text: halt and ask the user to fill it in.
  determine entry point from start-from arg or file inspection.
  initialise counters:
    iterations=0,
    derivations=0,
    state_changes_since_critique=0,         # any integrated sub-agent return
    substantive_changes_since_critique=0.   # ER promotions and refutations only

while not (terminated or halted):
  if entry_point == survey:
    /survey  → integrate  → log Post-survey gate decision  → entry_point = plan
  elif entry_point == plan:
    /research-plan  → integrate  → log Post-plan gate decision
                                  (and Framing gate decision if survey flagged a load-bearing disagreement)
                                  → entry_point = loop
  elif entry_point == loop:
    pick next dispatch from plan.md + research_log.md open work:
      if a derivation/computation is the next step:
        /derive or /compute  → integrate  → state_changes_since_critique++
                                            (if integration promoted a Working Claim to ER: substantive_changes_since_critique++)
        /review on that artefact  → integrate  → state_changes_since_critique++
                                                 (if verdict refuted, or integration promoted a Working Claim to ER: substantive_changes_since_critique++)
        if refuted: dispatch second /review; act per checks-and-balances.
      # Fire /critique only when there is something new to critique strategically.
      # The substantive_changes guard prevents re-litigating hygiene findings after
      # low-grade integration steps; the state_changes backstop catches stalled loops.
      if (substantive_changes_since_critique >= 1 AND state_changes_since_critique >= 2)
         OR state_changes_since_critique >= 6:
        /critique  → disposition  → reset both counters.
      if a strategy-level rewrite is warranted:
        /critique (the mandatory second)  → disposition.
        log Pre-strategy-change gate decision.
        /research-plan with feedback.
      check budgets (iterations, derivations); halt if exhausted.
      if research_log.md Established Results carry the answer: entry_point = finalize.
  elif entry_point == finalize:
    /critique (final, mandatory)  → disposition.
    log Pre-finalize gate decision.
    /finalize  → integrate.
    terminated = true.

emit end-of-run report.
```

The loop is the main agent's responsibility from start to end of this skill's invocation. Sub-agents continue to do all substantive work; the main agent dispatches, integrates, commits, and decides.
