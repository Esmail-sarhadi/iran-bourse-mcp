"""`config` / `install` / `call` / `tools`: the cross-agent onboarding surface."""

from __future__ import annotations

import json

import pytest

from iran_bourse_mcp import clients
from iran_bourse_mcp.cli import _parse_value, _result_text, build_parser


def test_every_client_has_a_snippet():
    for client in clients.all_clients():
        text = clients.snippet(client.id)
        assert "iran-bourse" in text or client.id == "generic"
        assert "uvx" in text


def test_unknown_client_lists_choices():
    with pytest.raises(KeyError, match="claude-code"):
        clients.get_client("nope")


def test_launch_defaults_to_github_and_supports_pypi():
    assert clients.launch()[1][:2] == ["--from", clients.GIT_SOURCE]
    assert clients.launch("pypi") == ("uvx", ["iran-bourse-mcp"])


def test_client_specific_shapes():
    assert clients.entry_for(clients.get_client("vscode"))["type"] == "stdio"
    opencode = clients.entry_for(clients.get_client("opencode"))
    assert opencode["type"] == "local" and opencode["command"][0] == "uvx" and isinstance(opencode["command"], list)
    assert "context_servers" in clients.snippet("zed")
    assert "[mcp_servers.iran-bourse]" in clients.snippet("codex")
    assert clients.snippet("claude-code").startswith("# Run once in your terminal:\nclaude mcp add iran-bourse -- uvx")


def test_deeplinks_decode_back_to_the_launch_command():
    import base64
    import urllib.parse

    cursor = clients.cursor_deeplink()
    assert cursor.startswith("cursor://anysphere.cursor-deeplink/mcp/install?name=iran-bourse&config=")
    payload = json.loads(base64.b64decode(cursor.split("config=")[1]))
    assert payload == {"command": "uvx", "args": ["--from", clients.GIT_SOURCE, "iran-bourse-mcp"]}

    vscode = clients.vscode_deeplink()
    assert vscode.startswith("vscode:mcp/install?")
    decoded = json.loads(urllib.parse.unquote(vscode.split("?", 1)[1]))
    assert decoded["name"] == "iran-bourse" and decoded["type"] == "stdio"

    goose = clients.goose_deeplink()
    assert goose.startswith("goose://extension?cmd=uvx") and goose.count("&arg=") == 3


def test_install_creates_file_and_is_idempotent(tmp_path):
    target = tmp_path / "cfg" / "mcp.json"
    message = clients.install("cursor", path=target)
    assert "Added" in message
    first = json.loads(target.read_text(encoding="utf-8"))
    assert first["mcpServers"]["iran-bourse"]["command"] == "uvx"
    assert "Updated" in clients.install("cursor", path=target)
    assert json.loads(target.read_text(encoding="utf-8")) == first


def test_install_preserves_existing_servers_and_makes_a_backup(tmp_path):
    target = tmp_path / "claude_desktop_config.json"
    target.write_text(json.dumps({"theme": "dark", "mcpServers": {"other": {"command": "x"}}}), encoding="utf-8")
    clients.install("claude-desktop", path=target)
    data = json.loads(target.read_text(encoding="utf-8"))
    assert data["theme"] == "dark" and data["mcpServers"]["other"] == {"command": "x"} and "iran-bourse" in data["mcpServers"]
    backups = list(tmp_path.glob("claude_desktop_config.json.bak-*"))
    assert len(backups) == 1
    assert json.loads(backups[0].read_text(encoding="utf-8"))["mcpServers"] == {"other": {"command": "x"}}


def test_install_refuses_to_touch_unparseable_files(tmp_path):
    target = tmp_path / "settings.json"
    original = '{ // comments are not JSON\n "mcpServers": {} }'
    target.write_text(original, encoding="utf-8")
    with pytest.raises(clients.InstallError, match="Not touching"):
        clients.install("gemini-cli", path=target)
    assert target.read_text(encoding="utf-8") == original


def test_install_refuses_wrong_shapes(tmp_path):
    target = tmp_path / "mcp.json"
    target.write_text('{"mcpServers": []}', encoding="utf-8")
    with pytest.raises(clients.InstallError):
        clients.install("cursor", path=target)
    target.write_text("[1, 2]", encoding="utf-8")
    with pytest.raises(clients.InstallError):
        clients.install("cursor", path=target)


def test_dry_run_writes_nothing(tmp_path):
    target = tmp_path / "mcp.json"
    out = clients.install("cursor", path=target, dry_run=True)
    assert "dry run" in out and not target.exists()


def test_clients_without_auto_install_explain_the_alternative():
    for client_id in ("zed", "codex", "claude-code", "generic"):
        with pytest.raises(clients.InstallError, match="config"):
            clients.install(client_id)


def test_cli_value_parsing_and_result_text():
    assert _parse_value("5") == 5 and _parse_value("true") is True and _parse_value("فولاد") == "فولاد"
    assert _parse_value('{"a": 1}') == {"a": 1}

    class Block:
        text = '{"ok": true}'

    class Result:
        content = [Block()]

    assert json.loads(_result_text(Result())) == {"ok": True}
    assert json.loads(_result_text(([Block()], {"x": 1}))) == {"ok": True}
    assert _result_text({"a": 1}) == '{"a": 1}'


def test_parser_has_all_subcommands():
    parser = build_parser()
    for argv in (["doctor"], ["tools", "--json"], ["call", "quote", "symbol=فولاد", "--compact"], ["config", "cursor"], ["install", "cursor", "--dry-run"], ["serve"]):
        assert parser.parse_args(argv).command == argv[0]
