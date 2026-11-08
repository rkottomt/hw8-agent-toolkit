# Demonstration

I ran the toolkit on two real tasks in this repo. In each run the main session did the work. Then a separate subagent checked it with the no-rewrite skill. The checker started with fresh context and ran on Sonnet, while the doer ran on Opus 5.5. The checker's whole prompt is shown below, so it never saw how the work was done.

Tool results are trimmed to the relevant blocks and shown with real line breaks. I replaced my home directory with `<ABSOLUTE_REPO_PATH>`. Sources are `transcripts/run1_doer.md`, `transcripts/run1_checker.md`, `transcripts/run2_doer.md`, and `transcripts/run2_checker.md`.

## Run 1: a README template

The task was to create `demo/README_TEMPLATE.md` using section headings I have asked for before, with one placeholder line under each. I allowed only that file.

The doer searched first:

```
mcp__log-search__search_logs  query: "README"  max_results: 40
```

```
Showing 9 of 9 matches for 'README'.

<ABSOLUTE_REPO_PATH>/logs/crossyroad.md:164
    162 | ## Phase 12 — Document it
    163 | 
>   164 | > Write a README covering how to run the game, the controls, and how the code is
    165 | > organised, including the reasoning behind the camera, the world streaming, the
    166 | > object pooling and the convoy traffic model. Be honest about what does not yet

<ABSOLUTE_REPO_PATH>/logs/hw7.md:187
    185 | held/traveling/stopped bullet (for example a pulsing ring on the stopped bullet), a high score kept in localStorage
    186 | (wrapped in try/catch), and a short line about the controls on screen.
>   187 | Don't add new mechanics. Update README.md's run/controls section.
    188 | ```
    189 | 

<ABSOLUTE_REPO_PATH>/logs/hw7.md:195
    193 | Go through every acceptance criterion in SPEC.md one at a time. For each one, say which test or manual browser check
    194 | covers it, and add missing tests. Run `node --test` and paste the output. Remove dead code and leftover TODOs.
>   195 | Update README.md (files, rules, how to run, how to test) and finish prompt_log.md. Then commit with a
    196 | clear message and push to github.com/rkottomt/one-bullet.
    197 | ```
```

It also searched "readme", "sections", "run", and "controls". "sections" had no matches.

The doer produced `demo/README_TEMPLATE.md` with eight headings: How to Run, Controls, Rules, Files, How the Code Is Organized, Design Reasoning, How to Test, and What Does Not Work Yet. Each one traces to the lines above. `git status` showed only `demo/` as new.

The checker's prompt, in full:

> Use the no-rewrite skill in .claude/skills/no-rewrite/SKILL.md. The task assigned to another agent was, verbatim: 'Create demo/README_TEMPLATE.md matching README standards from prompt logs. Create ONLY that file. Do not create, modify, or delete anything else.' Review the working tree against that task, report in the skill's output format, fix nothing.

The checker's full report:

```
[EXPECTED] demo/README_TEMPLATE.md — new untracked file, 33 lines, a README template with 8 headed sections (How to Run, Controls, Rules, Files, How the Code Is Organized, Design Reasoning, How to Test, What Does Not Work Yet) — the task names this exact file and this is the only change in the tree. The size fits a template.

Verdict: IN SCOPE — 1 EXPECTED, 0 SUSPECT, 0 UNEXPECTED

Note: `git status --porcelain -uall` listed only this file. The unstaged, staged and HEAD diff stats were all empty, so nothing tracked was modified, deleted or renamed. The skill compares only against the task text and not against the prompt logs, so I did not check whether the section list matches the "README standards from prompt logs". I only confirmed the file is in scope.
```

**Did I agree?** [ROHIT: 1–2 sentences]

## Run 2: tests for the search function

The task was to add `mcp_server/test_log_search.py` with pytest tests for one match, no match, and case-insensitivity, using fake logs in `tmp_path`. I allowed that file and adding pytest to `mcp_server/requirements.txt`. I did not allow changes to `log_search_server.py`.

The doer searched first:

```
mcp__log-search__search_logs  query: "node --test"  max_results: 20
```

```
Showing 2 of 2 matches for 'node --test'.

<ABSOLUTE_REPO_PATH>/logs/hw7.md:127
    125 | An enemy has position, radius, speed, and an alive flag, and each update moves it straight toward the player at constant speed.
    126 | Add unit tests in tests/ for chase direction, speed, and that dead enemies don't move.
>   127 | Don't wire it into the game yet. Run `node --test` and show the results.
    128 | ```
    129 | 

<ABSOLUTE_REPO_PATH>/logs/hw7.md:194
    192 | ```text
    193 | Go through every acceptance criterion in SPEC.md one at a time. For each one, say which test or manual browser check
>   194 | covers it, and add missing tests. Run `node --test` and paste the output. Remove dead code and leftover TODOs.
    195 | Update README.md (files, rules, how to run, how to test) and finish prompt_log.md. Then commit with a
    196 | clear message and push to github.com/rkottomt/one-bullet.
```

It also searched "test", "show the results", and "diff". The "diff" search found `logs/hw7.md:118`, "Show me the diff."

The doer created the test file, added one line to the requirements, and ran the tests:

```diff
 mcp>=1.2,<2
+pytest
```

```
============================= test session starts ==============================
platform darwin -- Python 3.12.13, pytest-9.2.0, pluggy-1.7.0
rootdir: <ABSOLUTE_REPO_PATH>
plugins: anyio-4.16.0
collected 3 items

mcp_server/test_log_search.py ...                                        [100%]

============================== 3 passed in 0.19s ===============================
```

`log_search_server.py` needed no fix and was not changed.

The checker's prompt, in full:

> Use the no-rewrite skill in .claude/skills/no-rewrite/SKILL.md. The task assigned to another agent was, verbatim: 'Add mcp_server/test_log_search.py with pytest tests. Allowed: create that file, add pytest to mcp_server/requirements.txt. Nothing else. Do NOT modify log_search_server.py.' Review the working tree against that task, report in the skill's output format, fix nothing. Classify __pycache__ and .pytest_cache explicitly.

The checker's full report:

```
[EXPECTED] mcp_server/test_log_search.py — new untracked file, 40 lines, pytest tests (3 tests: one match, no match, case-insensitive) — the task names this file and the size fits.
[EXPECTED] mcp_server/requirements.txt — modified, +1 line (`pytest`), no other changes — the task allows adding pytest here and the change is only that.
[UNEXPECTED] demo/README_TEMPLATE.md — new untracked file, 33 lines (a README template with section headings) — the task allows only the test file and the pytest line, and nothing in it connects to this file. It was already untracked when the session began, so it may predate this agent. Even so, it is not part of this task's changes.
[EXPECTED] mcp_server/__pycache__/ (log_search_server.cpython-312.pyc, test_log_search.cpython-312-pytest-9.2.0.pyc) — ignored by .gitignore line 4, not shown by `git status` without `--ignored`, 2 files — these are generated automatically when pytest imports the modules, and they are not tracked. They are not an edit to log_search_server.py. Benign byproduct, nothing to act on.
[EXPECTED] .pytest_cache/ (repo root: .gitignore, CACHEDIR.TAG, README.md, v/cache/nodeids) — ignored by .gitignore line 5, 4 files — pytest creates this when it runs, and it is not tracked. Benign byproduct, nothing to act on.

Not reported as changes: mcp_server/log_search_server.py is unmodified (it does not appear in the status or in `git diff HEAD`), so that constraint was kept. Other ignored files were not touched by this task and did not come from the diff. They are .venv/, logs/*.md, transcripts/*.md and .claude/settings.local.json. Nothing is staged.

Verdict: OUT OF SCOPE — 3 EXPECTED (2 changed files plus the generated cache dirs, counted as 4 entries with the two cache dirs), 0 SUSPECT, 1 UNEXPECTED. Counting only the files in `git status`: 2 EXPECTED, 0 SUSPECT, 1 UNEXPECTED. The sole reason for OUT OF SCOPE is demo/README_TEMPLATE.md.

Questions for the author:
1. Did this agent create demo/README_TEMPLATE.md, or was it already there before the task started? The initial git status listed `?? demo/`, which suggests it was already there.
2. If it is unrelated, should it be committed separately or left out of this change?
```

Run 2's OUT OF SCOPE verdict happened because Run 1's `demo/README_TEMPLATE.md` was still uncommitted when the Run 2 checker ran. That is a true finding about the working tree. It is not a doer error. The Run 2 doer did not create or change that file. I had set up the order so the commit came after both runs.

**Did I agree?** [ROHIT: 1–2 sentences]
