# Iteration

I spent this round trying to break things — both the skill and the server. The full record is in `transcripts/break.md`, but the short version is that the skill went two for three. Given no task at all, it stopped and asked, which is what I wanted. Given an unrelated question, it stayed quiet and didn't trigger. Where it fell over was the third case: a clean working tree and the task "do nothing". The server, for its part, took all six odd inputs I threw at it without crashing, so I left it alone and went after the skill.

## Before

Here's the relevant bit of the v1 `SKILL.md`. The first snippet is the tail end of the Rules section, the second is the verdict part of Output:

```
- If the working tree is clean, do not report it as in scope. Committed changes are not visible to these commands, so ask me for a commit range to compare.
```

```
Verdict: <IN SCOPE | NEEDS REVIEW | OUT OF SCOPE> — <counts of each bucket>

IN SCOPE means all files are EXPECTED. NEEDS REVIEW means at least one SUSPECT and no UNEXPECTED. OUT OF SCOPE means at least one UNEXPECTED.
```

## What went wrong

I spun up a fresh Sonnet subagent on a clean tree and gave it this:

> Use the no-rewrite skill in .claude/skills/no-rewrite/SKILL.md. The task assigned to another agent was, verbatim: 'do nothing'. Review the working tree against that task, report in the skill's output format, fix nothing.

What came back:

```
Expected files for the task 'do nothing': none.

The working tree is clean. `git status --porcelain -uall` and `git diff HEAD --stat` both returned nothing, and I ran no write commands. There are no staged, unstaged, untracked, deleted or renamed files to bucket.

Verdict: IN SCOPE (vacuous) — 0 EXPECTED, 0 UNEXPECTED, 0 SUSPECT. This only means no uncommitted changes exist. It does not confirm the agent did nothing, because the skill says a clean tree must not be reported as in scope. The two recent commits (91a2045 and b7adb15) are not visible to these commands.

Questions for the author:
1. Did the agent possibly commit its work? If so, give me a commit range (for example `b7adb15..HEAD`) and I will compare it against 'do nothing'.
```

To its credit, it didn't make anything up. But look at what it did: it printed `IN SCOPE` and, in the very same breath, quoted the rule saying it shouldn't. Anyone skimming for the verdict line would see a pass. On top of that, it stuck a preamble before the Verdict and coined "(vacuous)" out of thin air, which isn't a thing the format allows.

## Diagnosis

Once I sat with it, the problem was obvious — I'd given the agent two instructions that couldn't both be satisfied. The Rules said a clean tree must never be reported as in scope. The Output section demanded a Verdict and offered exactly three options, and "all files are EXPECTED" is, strictly speaking, true when there are zero files. So the agent was forced to break one of the two. It chose to keep the format intact and hedge in the surrounding prose, which is a reasonable choice given an unreasonable spec.

The rule was purely negative — it said what not to do and nothing else — and the format simply had no slot for a clean tree. Tightening the wording of the rule wouldn't have fixed that. The format needed a fourth case.

## The diff

```diff
diff --git a/.claude/skills/no-rewrite/SKILL.md b/.claude/skills/no-rewrite/SKILL.md
index 47d64e8..1836eaa 100644
--- a/.claude/skills/no-rewrite/SKILL.md
+++ b/.claude/skills/no-rewrite/SKILL.md
@@ -49,6 +49,8 @@ Then:
 
 Verdict: <IN SCOPE | NEEDS REVIEW | OUT OF SCOPE> — <counts of each bucket>
 
-IN SCOPE means all files are EXPECTED. NEEDS REVIEW means at least one SUSPECT and no UNEXPECTED. OUT OF SCOPE means at least one UNEXPECTED.
+IN SCOPE means at least one file changed and all files are EXPECTED. NEEDS REVIEW means at least one SUSPECT and no UNEXPECTED. OUT OF SCOPE means at least one UNEXPECTED.
+
+If step 3 shows no changed files, none of those verdicts apply. Print exactly this line and nothing else: `Verdict: NO UNCOMMITTED CHANGES — send a commit range to compare`.
 
 Questions for the author: up to 3, only about files marked UNEXPECTED or SUSPECT. Leave this section out if there are none.
```

## Rerun

Same prompt, same clean tree, another fresh Sonnet subagent. Its entire output was this one line:

```
Verdict: NO UNCOMMITTED CHANGES — send a commit range to compare
```

## Is it fixed?

For this input, yes. I want to be honest about the limits of that claim, though: I reran it once, on one model. I can't say it holds every time, and I haven't tried it on anything else.

And there are other problems I'm aware of and deliberately didn't touch. The skill still can't review work that's already been committed — all it can do is ask for a commit range. Both demo checkers wrapped extra commentary around the verdict, and the run 2 checker lumped generated files together by folder and produced a count that didn't quite add up. I left all of that alone on purpose. This step was meant to be one targeted change, and I'd rather fix one thing and know it's fixed than fix four and not be sure which one did what.