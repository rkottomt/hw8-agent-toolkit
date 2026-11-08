# hw8-agent-toolkit

Two small tools for working with coding agents. One is a skill that checks whether an agent stayed inside its task. The other is an MCP server that lets an agent search my old prompt logs.

## no-rewrite

no-rewrite compares the files changed in a git repo against what a task asked for. It sorts every changed file into EXPECTED, SUSPECT, or UNEXPECTED and gives a verdict. It only reports. It never fixes anything.

It triggers after an agent has edited files, before a commit, or when I say "what did you touch". It needs the task description. When I gave it only "check what you touched", it stopped and asked for the task. When I asked "did the last run go okay?", it did not run. Both results are in `transcripts/break.md`.

I wanted this because I keep putting scope limits in my prompts:

> Do not change any code yet. Log this prompt in prompt_log.md. Show me the diff. (`logs/hw7.md:118`)

> Don't wire it into the game yet. Run `node --test` and show the results. (`logs/hw7.md:127`)

> Don't add new mechanics. Update README.md's run/controls section. (`logs/hw7.md:187`)

Here is the honest caveat. My logs show many "don't do X yet" instructions, but they do not record a case of an agent actually overreaching. So the logs show that I worry about this and write around it. They do not prove it happened. The skill replaces reading every diff by hand to confirm a limit held.

## search_logs

search_logs is an MCP tool that searches the `.md` and `.txt` files under `LOGS_DIR`. The match ignores case and treats the query as literal text. It returns up to `max_results` matches, each with the file, the line number, and two lines of context on each side. The first line says how many matches there were in total.

It matches substrings, so "diff" also hits "difficulty". You can see that in `transcripts/run2_doer.md`.

I wanted this because I repeat the same standing instructions in every assignment:

> rkottomt and commit everything to there as u go. do not list urself as a contributor when u commit. (`logs/hw3.md:17`)

> give me ideas that i can do for this project. after i choose a project, create a github repo, track my prompts accurately, keep the prompt log minimal and add commits to github regularly but do not add yourself as a contributor. (`logs/hw6.md:8`)

An agent can look this up now.

## Install

You need Python 3.10 or newer and `uv`. The `mcp` package is pinned below 2 because FastMCP was renamed MCPServer in mcp 2.x, and the server imports FastMCP.

Create the venv and install the requirements from the repo root:

```
uv venv --python 3.12 .venv
uv pip install --python .venv/bin/python -r mcp_server/requirements.txt
```

The skill needs no install inside this repo. It is at `.claude/skills/no-rewrite/SKILL.md`, and Claude Code picks it up from there. To use it in another project, copy the `no-rewrite` folder into that project's `.claude/skills/`.

For the server, edit `.mcp.json` in the repo root. Every value in angle brackets is machine-specific, and so is `LOGS_DIR`:

```json
{
  "mcpServers": {
    "log-search": {
      "command": "<YOUR_PYTHON_PATH>",
      "args": [
        "<ABSOLUTE_REPO_PATH>/mcp_server/log_search_server.py"
      ],
      "env": {
        "LOGS_DIR": "<ABSOLUTE_REPO_PATH>/logs"
      }
    }
  }
}
```

`<YOUR_PYTHON_PATH>` is the absolute path to `.venv/bin/python`. `<ABSOLUTE_REPO_PATH>` is where you cloned this repo. `logs/` is gitignored, so you have to put your own logs there or point `LOGS_DIR` somewhere else.

Run the tests with `.venv/bin/python -m pytest`.

Confirmed working in: Claude Code 2.1.319. The tool call and raw result are in `transcripts/mcp_registration_test.md`.

## What I borrowed

The structure of the skill is modeled on the course's spec-check example. The server follows the FastMCP quickstart.

## AI usage

Claude Code scaffolded the skill, the server, and the config, and drafted these docs from saved transcripts. I directed the design decisions and reviewed everything.

More detail is in `DEMONSTRATION.md` and `ITERATION.md`. The saved evidence for both is in `transcripts/`.
