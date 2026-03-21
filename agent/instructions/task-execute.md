---
name: task-execute
description: Execute tasks from ${PLANNED_TASKS_PATH} in a systematic workflow
auto_execution_mode: 0
disable-model-invocation: true
---

# /task skill — Systematic ${PLANNED_TASKS_PATH} task execution workflow

Follow these steps precisely every time this skill is invoked.

## Step 1: Read config from ${PLANNED_TASKS_PATH}

Read ${PLANNED_TASKS_PATH} and extract the confirmation setting from the HTML comment on line 1:

```
<!-- task-config: confirmation=<value> -->
```

Valid values and their meanings:
- `required` (default if comment is missing): present task choice and wait for user approval before executing
- `complex_only`: auto-execute simple/routine tasks; confirm with user before executing complex ones
- `full_auto`: proceed immediately without asking for confirmation

## Step 2: Task selection

Read ${PLANNED_TASKS_PATH} and collect all uncompleted tasks (`- [ ]`). Evaluate which to do first based on:
- Urgency or time sensitivity
- Whether the task unblocks other tasks
- Recurrent vs one-time (recurrent tasks are lower priority if any one-time tasks remain)

Based on the confirmation setting:
- `required`: present your selected task and rationale, then wait for the user to approve or redirect
- `complex_only`: announce your choice; if complex, wait for confirmation; if simple, proceed
- `full_auto`: announce your choice and proceed immediately

## Step 3: Effort evaluation

Before starting execution:
- **Complex task**: check if you are in plan mode. If not, ask the user whether to switch to plan mode before proceeding.
- **Too large**: if the task scope is too broad for a single session, propose breaking it into subtasks. If the user approves, your current task becomes writing the subtask breakdown into ${PLANNED_TASKS_PATH}.

## Step 4: Execution

Carry out the selected task. During execution:
- Always use `uv run python` (never bare `python`) for any Python execution
- Use the SymPy MCP tools for any mathematical reasoning, derivation, or symbolic computation
- Use the Jupyter MCP tools (`mcp__jupyter__*`) for **any** interaction with Jupyter notebooks — never read or edit raw `.ipynb` JSON directly

## Step 5: Post-execution checklist (mandatory — do not skip)

After the task is complete, run through this checklist in order:

1. **Run tests**: `uv run python -m pytest` — check for regressions
   - If a regression is too complex to fix immediately, propose adding a new task to ${PLANNED_TASKS_PATH} instead of blocking the current one
2. **Recapitulate changes**: run `git diff` and summarise what changed
3. **Docs sync**:
   - If any file in `tests/` changed → update `docs/tests.md`
   - If any file in `docs/` changed → update `docs/index.md`
   - If changes were substantial → update `CLAUDE.md` and `README.md`

## Step 6: Update ${PLANNED_TASKS_PATH}

After completing the previous five steps, update ${PLANNED_TASKS_PATH}:
- **Completed one-time task**: 
   - mark it `[x]` in the task list and move up in the list before any
     other uncompleted task
   - add a `(DONE YYYY-MM-DD)` tag in the title of the task description
- **Completed recurrent task** (explicitly described as repeating in the
  task description): 
  - move the list item to the bottom of the task list (leave it `[ ]`)
  - add or update the task description title with `(LAST YYYY-MM-DD)`