---
name: motions-evaluation
description: Evaluate proposed tasks from ${PROPOSED_TASKS_PATH} one at a time
auto_execution_mode: 0
disable-model-invocation: true
---

Evaluate proposed tasks from ${PROPOSED_TASKS_PATH} one at a time, writing
decisions back into each task's `### Synthesis Evaluation` section.

## Workflow

1. Read `${PROPOSED_TASKS_PATH}` and collect every task whose `### Synthesis
   Evaluation` section still contains the placeholder `[Whether to
   approve or reject the task -- leave empty for now]`.

2. If no unevaluated tasks remain, report that all tasks have already
   been evaluated and stop.

3. For each unevaluated task, work through it **one at a time**:

   ### a. Evaluate across five axes

   | Axis | Key question |
   |---|---|
   | Problem severity | Is the problem real & demonstrated, or merely theoretical? |
   | Proportionality | Is the solution sized to the actual problem? |
   | Cost-benefit | Effort vs. payoff, ongoing maintenance burden |
   | Risk | New bugs, breakage probability, new dependencies |
   | Strategic fit | Research-focused math lib; small expert user base |

   **Default lean**: DISMISS over-engineered proposals; REPLACE when
   there is a valid core idea buried in unnecessary complexity or when
   the task is too complex to safely deliver it in one step; IMPLEMENT
   for targeted, low-risk improvements with demonstrated need.

   ### b. Produce a recommendation with specific guidance

   Choose one of: **DISMISS** / **REPLACE** / **IMPLEMENT**

   **DISMISS** when:
   - Problem is theoretical/not demonstrated in practice
   - Solution is over-engineered for the actual issue
   - Risk outweighs potential benefit
   - Problem is flat wrong or not influential
   - Alternative approaches are much simpler/better
   
   **REPLACE** when:
   - Valid core idea buried in unnecessary complexity
   - Task too large to safely deliver in one step
   - Multiple distinct concerns mixed together
   - Some parts valuable, others should be discarded
   
   **IMPLEMENT** when:
   - Targeted, low-risk improvement with demonstrated need
   - Problem is real and solution is proportional
   - Even if not perfect, can be framed better with advice
   - Clear benefit with manageable cost/risk

   Write a 3–4 sentence rationale covering the strongest axes for your
   recommendation. Include specific guidance:

   - **DISMISS**: State why it's over-engineered, wrong, not influential, or too risky
   - **REPLACE**: Specify what part to keep and what new pieces to produce
   - **IMPLEMENT**: Provide advice on how to frame it better if imperfect

   ### c. Present recommendation and ask for user decision

   Display your recommendation and rationale clearly to the user. Then
   use the `AskUserQuestion` tool to prompt:

   > **Task: `<task heading>`** My recommendation: **DISMISS / REPLACE
   > / IMPLEMENT**
   >
   > Enter your decision — `d` or `dismiss`, `b` or `replace`, `i` or
   > `implement`, or `q` / `quit` to stop. Press Enter to accept my
   > recommendation.

   Accept the user's input (case-insensitive, prefix match). An empty
   response accepts the recommendation. `q`/`quit` stops processing and
   jumps to the summary.

   ### d. Write the decision into ${PROPOSED_TASKS_PATH}

   Use the Edit tool to replace the **exact** placeholder string:

   ```
   [Whether to approve or reject the task -- leave empty for now]
   ```

   with the decision block:

   ```
   DECISION

   Rationale / advice sentence(s). Include specific guidance:
   - DISMISS: Why over-engineered, wrong, not influential, or too risky
   - REPLACE: What part to keep and what new pieces to produce  
   - IMPLEMENT: How to frame it better (if imperfect) and any constraints
   ```

   Only replace the placeholder for the **current task** — do not touch
   other tasks.

4. After all tasks are processed (or the user chose QUIT), print a
   summary table:

   | Task | Decision |
   |---|---|
   | ... | ... |

## Notes

- Work strictly one task at a time; do not batch-evaluate.
- Never modify any section of ${PROPOSED_TASKS_PATH} other than the `### Synthesis
  Evaluation` placeholder for the current task.
- If ${PROPOSED_TASKS_PATH} does not exist, say so and stop.
