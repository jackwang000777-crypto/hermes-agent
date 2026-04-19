from unittest.mock import patch

from hermes_cli.model_switch import list_authenticated_providers


def test_list_authenticated_providers_includes_custom_providers_from_config():
    config = {
        "custom_providers": [
            {
                "name": "miaomiaocode",
                "base_url": "https://codex.miaomiaocode.com/v1",
                "api_key": "test-key",
                "models": [
                    {"id": "gpt-5-codex-mini", "name": "GPT-5 Codex Mini"},
                    {"id": "gpt-5.4", "name": "GPT 5.4"},
                ],
            }
        ]
    }

    with patch("agent.models_dev.fetch_models_dev", return_value={}), patch(
        "hermes_cli.config.load_config", return_value=config
    ):
        providers = list_authenticated_providers(current_provider="miaomiaocode")

    miaomiao = next((p for p in providers if p["slug"] == "miaomiaocode"), None)
    assert miaomiao is not None
    assert miaomiao["is_current"] is True
    assert miaomiao["models"] == ["gpt-5-codex-mini", "gpt-5.4"]
    assert miaomiao["total_models"] == 2
    assert miaomiao["source"] == "user-config"
