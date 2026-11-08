"""Tests that call search_logs directly against fake log files."""

import pytest

from log_search_server import search_logs


@pytest.fixture
def logs_dir(tmp_path, monkeypatch):
    (tmp_path / "a.md").write_text(
        "first line\nDo not list yourself as a Contributor.\nlast line\n",
        encoding="utf-8",
    )
    (tmp_path / "b.txt").write_text("nothing relevant here\n", encoding="utf-8")
    monkeypatch.setenv("LOGS_DIR", str(tmp_path))
    return tmp_path


def test_one_match(logs_dir):
    result = search_logs("list yourself")

    assert result.startswith("Showing 1 of 1 matches")
    assert f"{logs_dir / 'a.md'}:2" in result
    assert ">     2 | Do not list yourself as a Contributor." in result


def test_no_match(logs_dir):
    result = search_logs("zebra")

    assert result == f"No matches for 'zebra' in 2 files under {logs_dir}."


def test_case_insensitive(logs_dir):
    lower = search_logs("contributor")
    upper = search_logs("CONTRIBUTOR")

    assert "Showing 1 of 1 matches" in lower
    assert "Showing 1 of 1 matches" in upper
    assert f"{logs_dir / 'a.md'}:2" in lower
    assert f"{logs_dir / 'a.md'}:2" in upper
