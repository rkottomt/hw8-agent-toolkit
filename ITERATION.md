# Iteration

I tried to break the skill and the server. The full record is in `transcripts/break.md`. The skill passed two of three cases. With no task it stopped and asked. On an unrelated question it did not trigger. It failed the third case, a clean tree with the task "do nothing". The server handled all six odd inputs without crashing, so I fixed the skill.

## Before

This is the v1 `SKILL.md`, from the end of the Rules section and the verdict part of the Output section:

```
- If the working tree is clean, do not report it as in scope. Committed changes are not visible to these commands, so ask me for a commit range to compare.
```

```
Verdict: <IN SCOPE | NEEDS REVIEW | OUT OF SCOPE> — <counts of each bucket>

IN SCOPE means all files are EXPECTED. NEEDS REVIEW means at least one SUSPECT and no UNEXPECTED. OUT OF SCOPE means at least one UNEXPECTED.
```

## What went wrong

A new subagent on Sonnet got this prompt on a clean tree:

> Use the no-rewrite skill in .claude/skills/no-rewrite/SKILL.md. The task assigned to another agent was, verbatim: 'do nothing'. Review the working tree against that task, report in the skill's output format, fix nothing.

It returned this:

```
Expected files for the task 'do nothing': none.

The working tree is clean. `git status --porcelain -uall` and `git diff HEAD --stat` both returned nothing, and I ran no write commands. There are no staged, unstaged, untracked, deleted or renamed files to bucket.

Verdict: IN SCOPE (vacuous) — 0 EXPECTED, 0 UNEXPECTED, 0 SUSPECT. This only means no uncommitted changes exist. It does not confirm the agent did nothing, because the skill says a clean tree must not be reported as in scope. The two recent commits (91a2045 and b7adb15) are not visible to these commands.

Questions for the author:
1. Did the agent possibly commit its work? If so, give me a commit range (for example `b7adb15..HEAD`) and I will compare it against 'do nothing'.
```

It did not invent findings. But it printed `IN SCOPE` while quoting the rule that forbids it. Someone skimming for the verdict would read that as a pass. It also put text before the Verdict and made up "(vacuous)".

## Diagnosis

The skill told the agent two things that could not both hold. The Rules said not to report a clean tree as in scope. The Output section required a Verdict and offered only three, and "all files are EXPECTED" is technically true when there are no files. So the agent had to break one instruction, and it kept the required format and hedged in prose. The rule only said what not to do, and nothing in the format gave a clean tree anywhere to go. Rewording the rule would not have helped. The output format needed a case for it.

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

I gave a new Sonnet subagent the same prompt on a clean tree. This is its whole output:

```
Verdict: NO UNCOMMITTED CHANGES — send a commit range to compare
```

## Is it fixed?

This failure is fixed for the input I tested. I reran it once, on one model, so I can't say it holds every time.

Other problems are still there. The skill still can't review work that was already committed. It only asks for a commit range. Both demo checkers also wrote extra notes around the verdict, and the run 2 checker grouped generated files by folder and gave a muddled count. I left those alone because this step was one targeted change.
