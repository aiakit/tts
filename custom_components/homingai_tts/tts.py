"""Support for HomingAI TTS."""
from __future__ import annotations
import logging
import asyncio
from typing import Any
import aiohttp
from homeassistant.components.tts import (
    CONF_LANG,
    Provider,
    TtsAudioType,
    TextToSpeechEntity,
    DOMAIN as TTS_DOMAIN,
)
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.components.tts import ATTR_VOICE
from .const import DOMAIN, CONF_ADDR
_LOGGER = logging.getLogger(__name__)
async def async_setup_entry(
        hass: HomeAssistant,
        config_entry: ConfigEntry,
        async_add_devices: AddEntitiesCallback,
) -> None:
    """Set up HomingAI TTS entry."""
    _LOGGER.debug("Setting up HomingAI TTS platform")
    engine = XTTSProvider(hass, config_entry)
    async_add_devices([engine])
class XTTSProvider(TextToSpeechEntity,Provider):
    """The HomingAI TTS speech API provider."""
    def __init__(self, hass: HomeAssistant, config_entry: ConfigEntry) -> None:
        """Initialize HomingAI TTS speech component."""
        self.hass = hass
        self._attr_name = "HomingAI TTS"
        self._attr_unique_id = f"{config_entry.entry_id}"
        self._addr = config_entry.data[CONF_ADDR]
        self._language = "zh"
    @property
    def supported_languages(self):
        """Return list of supported languages."""
        return SUPPORTED_LANGUAGES
    @property
    def default_language(self) -> str:
        """Return the default language."""
        return "zh"
    @property
    def supported_languages(self) -> list[str]:
        """Return list of supported languages."""
        return ["zh"]
    @property
    def supported_options(self) -> list[str]:
        """Return list of supported options."""
        return ["zh"]

    def get_tts_audio(self, message: str, language: str, options: dict[str, Any] | None = None) -> TtsAudioType:
        """Load TTS audio."""
        return self.async_get_tts_audio(message, language, options)

    async def async_get_tts_audio(
            self, message: str, language: str, options: dict[str, Any] | None = None
    ) -> TtsAudioType:
        """Load TTS from X."""
        if options is None:
            options = {}
        try:
            url = f"{self._addr}/tts"
            _LOGGER.debug("Requesting TTS from %s with message: %s", url, message)

            async with aiohttp.ClientSession() as session:
                async with session.post(
                        url,
                        json={"text": message},
                        timeout=10
                ) as response:
                    if response.status != 200:
                        _LOGGER.error(
                            "Error %d on load URL %s",
                            response.status,
                            url
                        )
                        return None, None

                    data = await response.read()
                    _LOGGER.debug("Successfully got TTS audio")
                    return "mp3", data
        except asyncio.TimeoutError:
            _LOGGER.error("Timeout requesting TTS")
            return None, None
        except aiohttp.ClientError as err:
            _LOGGER.error("Error requesting TTS: %s", str(err))
            return None, None
        except Exception as err:
            _LOGGER.error("Unexpected error requesting TTS: %s", str(err))
            return None, None