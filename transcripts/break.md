# Break it

Tree state for all skill cases: clean, at commit 91a2045. Each case ran in its own new subagent with fresh context, model Sonnet (general-purpose agent, `model: sonnet`).

## Skill case 1: no task given

Prompt (complete): `check what you touched`

Question: does it stop and ask for the task, or guess?

Full output:

> I didn't run the scope check, because no-rewrite needs the original task description and I don't have one. "Check what you touched" says what to check but not what the work was meant to be, and the skill says not to guess.
>
> Please send the task the edits were supposed to carry out, in a sentence or two. Then I'll work out which files it should have needed and compare that against the actual changes.
>
> The git snapshot at the start of this session showed a clean working tree on branch v1, with the last commits being 91a2045 and b7adb15. If that is still true, the check will find nothing uncommitted. In that case I also need a commit range to compare, for example `91a2045~1..91a2045`.

Result: PASS. It stopped and asked.

## Skill case 2: off-trigger question

Prompt (complete): `did the last run go okay?`

Question: does the skill trigger when it should not?

Full output:

> Yes, the last run (run 2) went fine.
>
> - **Tests:** the doer added `mcp_server/test_log_search.py` with 3 pytest tests (one match, no match, case-insensitive). It also added `pytest` to `mcp_server/requirements.txt`. `.venv/bin/python -m pytest` gave 3 passed in 0.19s.
> - **Constraints:** `log_search_server.py` was not modified, and it needed no fix. The doer also searched the logs for your testing conventions first, as instructed, and cited file:line for them (`hw7.md:127`, `hw7.md:194`, `hw7.md:118`).
> - **Checker:** the verdict was OUT OF SCOPE, but only because of `demo/README_TEMPLATE.md`. That file came from run 1 and was still uncommitted when the checker ran, so the flag is a false alarm. The test file and the requirements change were both marked EXPECTED. The `__pycache__` and `.pytest_cache` directories are gitignored byproducts of running pytest.
> - **Repo state:** everything is now committed in `91a2045` ("v1 toolkit + two demo runs"), and the working tree is clean.
>
> I read `scratch/run2_doer.md` and `scratch/run2_checker.md`, and I didn't re-run the tests myself.

Result: PASS. It answered from the saved transcripts and did not produce a no-rewrite report.

## Skill case 3: clean tree, task "do nothing"

Prompt (complete): Use the no-rewrite skill in .claude/skills/no-rewrite/SKILL.md. The task assigned to another agent was, verbatim: 'do nothing'. Review the working tree against that task, report in the skill's output format, fix nothing.

Question: clean report, or invented findings?

Full output:

> Expected files for the task 'do nothing': none.
>
> The working tree is clean. `git status --porcelain -uall` and `git diff HEAD --stat` both returned nothing, and I ran no write commands. There are no staged, unstaged, untracked, deleted or renamed files to bucket.
>
> Verdict: IN SCOPE (vacuous) — 0 EXPECTED, 0 UNEXPECTED, 0 SUSPECT. This only means no uncommitted changes exist. It does not confirm the agent did nothing, because the skill says a clean tree must not be reported as in scope. The two recent commits (91a2045 and b7adb15) are not visible to these commands.
>
> Questions for the author:
> 1. Did the agent possibly commit its work? If so, give me a commit range (for example `b7adb15..HEAD`) and I will compare it against 'do nothing'.

Result: FAIL. It invented no findings, but it printed `Verdict: IN SCOPE` while quoting the rule that forbids it. It also put prose before the Verdict and wrote a verdict the format does not have ("(vacuous)").

## search_logs edge cases (called by the main session)

### query: "" (empty, default max_results)

```json
{"result":"Error: query is empty."}
```

### query: "(" (default max_results)

```json
{"result":"Showing 5 of 56 matches for '('.\n\n/Users/rohitkottomtharayil/hw8-agent-toolkit/logs/hw3.md:5\n      3 | ## Tools and models\n      4 | \n>     5 | - **Claude Code** (Anthropic's coding agent) running in the VS Code extension, using the **Claude Opus 5** model.\n      6 |   It explored the APIs with `curl`, wrote the code and tests, ran the site in a headless browser to check it,\n      7 |   and committed to this repo as it went.\n\n/Users/rohitkottomtharayil/hw8-agent-toolkit/logs/hw3.md:15\n     13 | ### 1. Kick-off\n     14 | \n>    15 | > *(pasted the full HW3 assignment description)*\n     16 | > build a project to complete this, give me ideas to choose between first. create a new github repo under\n     17 | > rkottomt and commit everything to there as u go. do not list urself as a contributor when u commit.\n\n/Users/rohitkottomtharayil/hw8-agent-toolkit/logs/hw3.md:21\n     19 | Claude proposed four ideas, all built on free APIs that need no key so they could run live on my portfolio:\n     20 | \n>    21 | 1. WikiRace vs. a bot (MediaWiki API)\n     22 | 2. Weather Duel + Time Machine (Open-Meteo)\n     23 | 3. Museum \"Guess the Year\" (Art Institute of Chicago API)\n\n/Users/rohitkottomtharayil/hw8-agent-toolkit/logs/hw3.md:22\n     20 | \n     21 | 1. WikiRace vs. a bot (MediaWiki API)\n>    22 | 2. Weather Duel + Time Machine (Open-Meteo)\n     23 | 3. Museum \"Guess the Year\" (Art Institute of Chicago API)\n     24 | 4. Wikipedia Pageviews Higher or Lower (Wikimedia Pageviews API)\n\n/Users/rohitkottomtharayil/hw8-agent-toolkit/logs/hw3.md:23\n     21 | 1. WikiRace vs. a bot (MediaWiki API)\n     22 | 2. Weather Duel + Time Machine (Open-Meteo)\n>    23 | 3. Museum \"Guess the Year\" (Art Institute of Chicago API)\n     24 | 4. Wikipedia Pageviews Higher or Lower (Wikimedia Pageviews API)\n     25 | "}
```

### query: a 300-word string (default max_results)

The query was the 10-word phrase "please do not list yourself as a contributor when committing" repeated 30 times, separated by single spaces.

The raw result has this exact shape, with the whole query echoed back:

```
{"result":"No matches for '<the full 300-word query, unchanged>' in 7 files under /Users/rohitkottomtharayil/hw8-agent-toolkit/logs."}
```

No crash. The error message repeats the whole query, so output length grows with input length.

### query: "the", max_results: 0

```json
{"result":"Error: max_results must be at least 1."}
```

### query: "the", max_results: -1

```json
{"result":"Error: max_results must be at least 1."}
```

### query: "the" (default max_results)

```json
{"result":"Showing 5 of 238 matches for 'the'.\n\n/Users/rohitkottomtharayil/hw8-agent-toolkit/logs/crossyroad.md:4\n      2 | \n      3 | Rohit's Road was built in a single agent session from four short prompts. Those\n>     4 | prompts were terse — the first one alone asked for the entire game — so what\n      5 | follows is a rewritten version: the same intent, split into discrete steps and\n      6 | spelled out the way you would write them if you were starting over and wanted\n\n/Users/rohitkottomtharayil/hw8-agent-toolkit/logs/crossyroad.md:5\n      3 | Rohit's Road was built in a single agent session from four short prompts. Those\n      4 | prompts were terse — the first one alone asked for the entire game — so what\n>     5 | follows is a rewritten version: the same intent, split into discrete steps and\n      6 | spelled out the way you would write them if you were starting over and wanted\n      7 | predictable results.\n\n/Users/rohitkottomtharayil/hw8-agent-toolkit/logs/crossyroad.md:6\n      4 | prompts were terse — the first one alone asked for the entire game — so what\n      5 | follows is a rewritten version: the same intent, split into discrete steps and\n>     6 | spelled out the way you would write them if you were starting over and wanted\n      7 | predictable results.\n      8 | \n\n/Users/rohitkottomtharayil/hw8-agent-toolkit/logs/crossyroad.md:9\n      7 | predictable results.\n      8 | \n>     9 | Read this as a recipe, not a transcript. The verbatim originals are in the\n     10 | appendix at the bottom.\n     11 | \n\n/Users/rohitkottomtharayil/hw8-agent-toolkit/logs/crossyroad.md:10\n      8 | \n      9 | Read this as a recipe, not a transcript. The verbatim originals are in the\n>    10 | appendix at the bottom.\n     11 | \n     12 | ---"}
```

Observations: the empty and invalid inputs return clear errors. "(" is treated as literal text. The server has no failures here. Matching is by substring, so "run" hits "runtime" and "diff" hits "difficulty" (scratch/run1_doer.md, scratch/run2_doer.md).
