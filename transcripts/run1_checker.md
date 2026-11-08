# Run 1, checker

Separate subagent, fresh context, model: Sonnet (general-purpose agent, `model: sonnet`).

## Prompt given (complete)

Use the no-rewrite skill in .claude/skills/no-rewrite/SKILL.md. The task assigned to another agent was, verbatim: 'Create demo/README_TEMPLATE.md matching README standards from prompt logs. Create ONLY that file. Do not create, modify, or delete anything else.' Review the working tree against that task, report in the skill's output format, fix nothing.

## Full output

[EXPECTED] demo/README_TEMPLATE.md — new untracked file, 33 lines, a README template with 8 headed sections (How to Run, Controls, Rules, Files, How the Code Is Organized, Design Reasoning, How to Test, What Does Not Work Yet) — the task names this exact file and this is the only change in the tree. The size fits a template.

Verdict: IN SCOPE — 1 EXPECTED, 0 SUSPECT, 0 UNEXPECTED

Note: `git status --porcelain -uall` listed only this file. The unstaged, staged and HEAD diff stats were all empty, so nothing tracked was modified, deleted or renamed. The skill compares only against the task text and not against the prompt logs, so I did not check whether the section list matches the "README standards from prompt logs". I only confirmed the file is in scope.
