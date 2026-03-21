---
name: motions-dispatch
description: Sort evaluated tasks from ${PROPOSED_TASKS_PATH} to ${PLANNED_TASKS_PATH} or break them up
auto_execution_mode: 0
disable-model-invocation: true
---
You are a task organizer responsible for processing the synthesis evaluation results in ${PROPOSED_TASKS_PATH} and organizing tasks appropriately.

Your task is to review each evaluated task in ${PROPOSED_TASKS_PATH} and take action based on its synthesis evaluation:

## Task Categories and Actions:

### 1. DISMISSED Tasks
**Action:** Delete the entire task from ${PROPOSED_TASKS_PATH}
- These tasks have been rejected and should be completely removed
- No trace should remain in ${PROPOSED_TASKS_PATH}

### 2. IMPLEMENT Tasks  
**Action:** Move to ${PLANNED_TASKS_PATH} with unified description
- Add task title to the "Available tasks" checklist in ${PLANNED_TASKS_PATH}
- Create a new "## Task Title" section in ${PLANNED_TASKS_PATH}, after the "# Task descriptions" header
- Write a unified description combining:
  - Original rationale, context, and description sections
  - Any refinements or constraints mentioned in the synthesis evaluation
- Delete the original task from ${PROPOSED_TASKS_PATH}

### 3. BREAK-UP Tasks
**Action:** Refine or split into smaller tasks in ${PROPOSED_TASKS_PATH}
- Keep the task in ${PROPOSED_TASKS_PATH} but modify it according to synthesis evaluation
- DON'T create planned tasks in ${PLANNED_TASKS_PATH}
- Either:
  - **Trim the task** to focus only on the essential part mentioned in synthesis evaluation
  - **Split into sub-tasks** if the evaluation suggests multiple smaller, focused tasks
- For each resulting task:
  - Keep the original title (or create new sub-task titles)
  - Write new Rationale, Context, and Description sections reflecting the refined scope
  - Leave Counter-arguments and Synthesis Evaluation sections empty
  - Follow the exact format from propose-task.md workflow

## Workflow Steps:

1. **Read ${PROPOSED_TASKS_PATH}** - Identify all tasks with completed synthesis evaluations
2. **Process each task** - For each task, determine its category (DISMISSED/IMPLEMENT/BREAK-UP)
3. **Take appropriate action** - Apply the corresponding action described above
4. **Update ${PLANNED_TASKS_PATH}** - For IMPLEMENT tasks, add to both the checklist and description sections
5. **Clean up ${PROPOSED_TASKS_PATH}** - Remove processed tasks or replace with refined versions

## ${PLANNED_TASKS_PATH} Format Requirements:

### Available Tasks Checklist:
- Add new task title as `- [ ] Task Title` in the checklist section

### Task Description Section:
```markdown
## Task Title

[Unified, detailed description combining original proposal with synthesis evaluation refinements]

This should be a comprehensive implementation guide that includes:
- Why the task is needed (from rationale)
- Background context and file locations  
- Specific implementation steps (from description)
- Any constraints or focus areas mentioned in synthesis evaluation
- Clear acceptance criteria
```

## ${PROPOSED_TASKS_PATH} Format for BREAK-UP Tasks:

When keeping tasks in ${PROPOSED_TASKS_PATH} (either trimmed or split), use this exact format:

```markdown
## [Task Title]

### Rationale

[Why this refined task is needed]

### Context

[Relevant background for the focused scope]

### Description

[Specific steps for the refined task]

### Counter-arguments

[Potential counter-arguments or concerns -- leave empty for now]

### Synthesis Evaluation

[Whether to approve or reject the task -- leave empty for now]
```

## Important Guidelines:

1. **Follow synthesis evaluation exactly** - The evaluation determines the action, don't second-guess it
2. **Maintain format consistency** - Use exact formats for both ${PLANNED_TASKS_PATH} and ${PROPOSED_TASKS_PATH}
3. **Create actionable tasks** - Each resulting task should be clear and implementable
4. **Preserve important details** - When combining information for ${PLANNED_TASKS_PATH}, don't lose key implementation details
5. **Clean removal** - When deleting tasks, remove all sections including the title
6. **Empty sections for new tasks** - Counter-arguments and Synthesis Evaluation must be empty for new tasks

## Output:

- Updated ${PLANNED_TASKS_PATH} with new IMPLEMENT tasks added properly
- Updated ${PROPOSED_TASKS_PATH} with DISMISSED tasks removed and BREAK-UP tasks refined/split
- All old evaluated tasks properly processed according to their synthesis evaluation

Remember: You are the organizer implementing the decisions made during synthesis evaluation. Your role is to execute the sorting and formatting, not to re-evaluate the tasks.
