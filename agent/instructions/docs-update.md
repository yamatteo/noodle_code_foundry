---
name: docs-update
description: Update project documentation based on recent code changes
auto_execution_mode: 0
disable-model-invocation: true
---

Review and update project documentation based on recent code changes. Follow these steps exactly:

## Step 1: Determine docs path

Use `$ARGUMENTS` as the docs folder path if provided (e.g., `/docs-update my-docs/`). Otherwise default to `${DOCS_PATH}`.

## Step 1: Validate `${DOCS_PATH}/index.md`

- Check that `${DOCS_PATH}/index.md` exists. If it does not exist, **stop immediately** and tell the user: "Cannot find `${DOCS_PATH}/index.md`. Please create it or pass the correct docs path as an argument."
- Read the file and verify it has a YAML frontmatter block (delimited by `---`) containing a `last_updated` field. If the frontmatter is missing, malformed, or `last_updated` is absent, **stop immediately** and tell the user what is wrong with the format.

## Step 2: Extract `last_updated` value

- Extract the `last_updated` value. Accepted formats:
  - `YYYY-MM-DD hh:mm:ss` — use as-is for git and comparisons.
  - `YYYY-MM-DD` — treat as `YYYY-MM-DD 00:00:00`.

## Step 3: Check current git status

Run `git status` and `git diff` to note any unstaged or staged changes not yet committed.

## Step 4: List commits since `last_updated`

Run:
```
git log --since="{last_updated}" --oneline
```

If there are no commits and no uncommitted changes, inform the user that docs appear to be up to date and stop.

For each commit found, inspect it with `git show <hash> --stat` and read the full diff for files that seem relevant to the documentation.

Also check uncommitted changes (from Step 3) that may need to be reflected in docs.

## Step 5: Read `${DOCS_PATH}/index.md`

Read the index file to get the full list of documentation files and their descriptions, so you know which docs might be affected by the changes.

## Step 6: Read potentially affected doc files

Based on the commits and changes identified, read each doc file that may need updating. Focus on files whose described content relates to the changed source files or topics.

## Step 7: Decide and apply updates

For each doc file you read:
- If its content is still accurate, leave it unchanged.
- If its content needs updating (incorrect details, missing new features, stale references):
  - Apply the necessary content changes.
  - Update its `last_updated` frontmatter field to the current date and time in `YYYY-MM-DD hh:mm:ss` format.
  - If substantially rewritten, also update its `abstract` frontmatter field.

Finally, update `${DOCS_PATH}/index.md`'s `last_updated` frontmatter field to the current date and time in `YYYY-MM-DD hh:mm:ss` format.

Report to the user: which files were updated and a brief summary of what changed in each.