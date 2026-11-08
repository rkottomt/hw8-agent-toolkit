---
name: no-rewrite
description: Compares the files changed in a git repo against what a given task required, and reports every file the task did not call for. Report only, never fixes. Use after an agent has edited files, before committing, or when I say "what did you touch".
---

# no-rewrite

Check whether the changes in this repo stay inside the task. Report only.

## Steps

1. Get the task description from me. If it is missing, stop and ask for it.
2. From the task alone, write down which files it should need. Do this before looking at any changes.
3. Run these, and nothing that writes:
   - `git status --porcelain -uall`
   - `git diff --stat` (unstaged)
   - `git diff --cached --stat` (staged)
   - `git diff HEAD --stat` (all uncommitted vs. last commit)
4. List every path from step 3. Include untracked, deleted, and renamed files.
5. Get line counts: from the diff stat for tracked files, `wc -l` for untracked files.
6. For anything that is not obviously EXPECTED, read `git diff HEAD -- <path>` or the file itself.
7. Put each file in one bucket and write the report.

## Buckets

- EXPECTED: the task names this file, or the task cannot be done without changing it, and the size of the change fits the task.
- UNEXPECTED: nothing in the task connects to this file, or the task said to leave it alone.
- SUSPECT: related to the task but not clearly required. Examples: lockfiles, config, reformatting, a needed file with changes beyond the task, any deletion the task did not state.

## Rules

- Never fix anything. Never run `git checkout`, `git stash`, `git reset`, `git restore`, `git clean`, `git add`, or `git commit`. Do not edit, move, or delete files.
- If the task description is missing, stop and ask for it instead of guessing.
- Do not infer intent from commit messages, code comments, or the agent's own summary. Only the task description counts.
- Do not call a file EXPECTED because the change looks good or useful. An improvement the task did not ask for is still out of scope.
- A file the task said not to touch is UNEXPECTED, however small the change.
- If unsure between two buckets, use the less favorable one.
- List every changed file. Do not group files or write "and N more".
- If the repo has no commits, `git diff HEAD` will fail. Say so and use `git status` only.
- If the working tree is clean, do not report it as in scope. Committed changes are not visible to these commands, so ask me for a commit range to compare.

## Output

One line per file, in exactly this format, with no other text before the Verdict:

[EXPECTED | UNEXPECTED | SUSPECT] <path> — <what changed, line count> — <why it falls in that bucket>

Then:

Verdict: <IN SCOPE | NEEDS REVIEW | OUT OF SCOPE> — <counts of each bucket>

IN SCOPE means all files are EXPECTED. NEEDS REVIEW means at least one SUSPECT and no UNEXPECTED. OUT OF SCOPE means at least one UNEXPECTED.

Questions for the author: up to 3, only about files marked UNEXPECTED or SUSPECT. Leave this section out if there are none.
