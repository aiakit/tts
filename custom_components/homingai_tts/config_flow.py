"""Config flow for HomingAI TTS."""
from __future__ import annotations
import logging
from typing import Any
import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResult
import homeassistant.helpers.config_validation as cv
from .const import DOMAIN, CONF_ADDR, DEFAULT_NAME
_LOGGER = logging.getLogger(__name__)
STEP_USER_DATA_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_ADDR): str,
    }
)

class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for HomingAI TTS."""
    VERSION = 1

    @staticmethod
    def _is_valid_url(url: str) -> bool:
        """验证URL是否为http或https协议."""
        return url.lower().startswith(('http://', 'https://'))

    async def async_step_user(
            self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the initial step."""
        errors: dict[str, str] = {}
        if user_input is not None:
            url = user_input[CONF_ADDR]
            if not self._is_valid_url(url):
                _LOGGER.exception("invalid_url_protocol exception")
                errors["base"] = "invalid_url_protocol"
            else:
                try:
                    # 检查是否已经配置
                    await self.async_set_unique_id(url)
                    self._abort_if_unique_id_configured()

                    return self.async_create_entry(
                        title=DEFAULT_NAME,
                        data=user_input,
                    )
                except Exception:
                    _LOGGER.exception("Unexpected exception")
                    errors["base"] = "unknown"

        return self.async_show_form(
            step_id="user",
            data_schema=STEP_USER_DATA_SCHEMA,
            errors=errors,
        )