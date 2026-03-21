---
name: commit-relevant
description: Analyze staged and unstaged changes to identify semantically meaningful commit units
auto_execution_mode: 0
disable-model-invocation: true
---

# Analyze and Propose Commit

## Objective
Analyze the current repository state (staged and unstaged changes) along with recent commits to identify semantically meaningful groups of changes that should be committed together. The goal is to create logical, atomic commits rather than committing whatever happens to be in the working directory.

## Steps

1. **Check repository status**
   - Run `git status` to see current staging state
   - Identify which files have staged changes and which have unstaged changes

2. **Analyze staged changes**
   - Run `git diff --staged` to examine staged changes
   - Look for patterns, themes, or logical groupings in the staged changes

3. **Analyze unstaged changes**
   - Run `git diff` to examine unstaged changes
   - Identify patterns and logical groupings in unstaged changes

4. **Review recent commit history**
   - Run `git log --oneline -10` to understand recent commit patterns
   - Look for commit message style and semantic grouping patterns

5. **Identify semantic groups**
   - Analyze all changes together to find common themes:
     - Feature additions
     - Bug fixes
     - Refactoring
     - Documentation updates
     - Configuration changes
     - Test improvements
   - Consider if changes form a complete, logical unit

6. **Stage relevant changes**
   - If changes span multiple semantic groups, stage only one logical group at a time
   - Use `git add` selectively to group related changes
   - Leave unrelated changes unstaged for future commits

7. **Propose commit message**
   - Based on the identified semantic group, suggest a clear, descriptive commit message
   - Follow conventional commit format if appropriate (feat:, fix:, docs:, etc.)
   - Ensure the message accurately describes the scope of changes

8. **Present analysis to user**
   - Show what changes are being proposed for commit
   - Present the suggested commit message
   - Explain the reasoning behind the grouping
   - If changes don't form a complete semantic unit, explain why and ask user to decide

## Notes
- Always prioritize semantic completeness over arbitrary grouping
- If changes are incomplete or don't form a logical unit, clearly communicate this to the user
- Consider the impact of each proposed commit on codebase coherence
- Respect existing commit message conventions in the repository
- Whenever possible, use git mcp instead of shell commands
