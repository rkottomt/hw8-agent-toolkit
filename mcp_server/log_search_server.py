# Requires Python 3.10+ and mcp<2 (pinned in requirements.txt).
# mcp 2.x renamed FastMCP to MCPServer, so this file does not run on 2.x.

"""MCP server over stdio with one tool for searching prompt logs.

Stdout carries the JSON-RPC stream, so all logging goes to stderr.
"""

import logging
import os
import sys
from pathlib import Path

from mcp.server.fastmcp import FastMCP

logging.basicConfig(
    stream=sys.stderr,
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
)
logger = logging.getLogger("log_search_server")

CONTEXT_LINES = 2
SEARCHED_SUFFIXES = {".md", ".txt"}

mcp = FastMCP("log-search")


def _log_files(logs_dir: Path) -> list[Path]:
    return sorted(
        path
        for path in logs_dir.rglob("*")
        if path.is_file() and path.suffix.lower() in SEARCHED_SUFFIXES
    )


def _format_match(path: Path, lines: list[str], index: int) -> str:
    start = max(0, index - CONTEXT_LINES)
    end = min(len(lines), index + CONTEXT_LINES + 1)
    block = [f"{path}:{index + 1}"]
    for i in range(start, end):
        marker = ">" if i == index else " "
        block.append(f"{marker} {i + 1:>5} | {lines[i]}")
    return "\n".join(block)


@mcp.tool()
def search_logs(query: str, max_results: int = 5) -> str:
    """Search my past prompt logs for a word or phrase.

    This looks through every .md and .txt file under LOGS_DIR (./logs unless
    the LOGS_DIR environment variable says otherwise), including subfolders.
    The match ignores case and treats the query as literal text, so characters
    like ( or * are not regex.

    You get back up to max_results matches, in filename order. Each one shows
    the filename, the line number, and the matching line marked with > between
    2 lines of context on each side. The first line says how many matches
    there were in total, so you can tell if the list was cut off.

    Call this when you need something I said or decided in an earlier
    assignment: a standing instruction, my GitHub username, how I set up a past
    project, or the exact wording of an old prompt. Check here before asking me
    to repeat myself. It only covers the logs, so it won't help with the current
    code or anything from this session.
    """
    if not query.strip():
        return "Error: query is empty."
    if max_results < 1:
        return "Error: max_results must be at least 1."

    logs_dir = Path(os.environ.get("LOGS_DIR", "./logs"))
    if not logs_dir.is_dir():
        logger.warning("Logs directory not found: %s", logs_dir)
        return f"Error: logs directory not found: {logs_dir}"

    needle = query.casefold()
    total = 0
    results: list[str] = []
    files = _log_files(logs_dir)

    for path in files:
        try:
            lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
        except OSError as exc:
            logger.warning("Could not read %s: %s", path, exc)
            continue
        for index, line in enumerate(lines):
            if needle in line.casefold():
                total += 1
                if len(results) < max_results:
                    results.append(_format_match(path, lines, index))

    logger.info("Query %r: %d matches in %d files", query, total, len(files))
    if total == 0:
        return f"No matches for {query!r} in {len(files)} files under {logs_dir}."

    header = f"Showing {len(results)} of {total} matches for {query!r}."
    return "\n\n".join([header, *results])


if __name__ == "__main__":
    logger.info("Starting log-search server over stdio")
    mcp.run(transport="stdio")
