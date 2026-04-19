from types import SimpleNamespace

import hermes_cli.status as status_mod
from hermes_cli.status import show_status


def test_show_status_includes_tavily_key(monkeypatch, capsys, tmp_path):
    monkeypatch.setenv("HERMES_HOME", str(tmp_path))
    monkeypatch.setenv("TAVILY_API_KEY", "tvly-1234567890abcdef")

    show_status(SimpleNamespace(all=False, deep=False))

    output = capsys.readouterr().out
    assert "Tavily" in output
    assert "tvly...cdef" in output


def test_show_status_uses_launchctl_print_target_on_macos(monkeypatch, capsys, tmp_path):
    monkeypatch.setenv("HERMES_HOME", str(tmp_path))
    monkeypatch.setattr(status_mod.sys, "platform", "darwin")
    monkeypatch.setattr(status_mod.os, "getuid", lambda: 501)

    calls = []

    def fake_run(cmd, **kwargs):
        calls.append(cmd)
        return SimpleNamespace(returncode=0, stdout="service running", stderr="")

    monkeypatch.setattr(status_mod.subprocess, "run", fake_run)

    show_status(SimpleNamespace(all=False, deep=False))

    output = capsys.readouterr().out
    assert any(
        cmd[:2] == ["launchctl", "print"] and cmd[2].startswith("gui/501/ai.hermes.gateway")
        for cmd in calls
    )
    assert "loaded" in output.lower()
