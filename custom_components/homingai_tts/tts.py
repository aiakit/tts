"""Support for HomingAI TTS."""
from __future__ import annotations

import asyncio
import base64
import json
import logging
from typing import Any

import aiohttp
from homeassistant.components.tts import (
    Provider,
    TtsAudioType,
    TextToSpeechEntity,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

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


class XTTSProvider(TextToSpeechEntity, Provider):
    """The HomingAI TTS speech API provider."""

    def __init__(self, hass: HomeAssistant, config_entry: ConfigEntry) -> None:
        """Initialize HomingAI TTS speech component."""
        self.hass = hass
        self._attr_name = "HomingAI TTS"
        self._attr_unique_id = f"{config_entry.entry_id}"
        self._language = "zh"
        self.access_token = config_entry.data.get('access_token', '')

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
        """Load TTS """
        try:
            headers = {"Authorization": f"Bearer {self.access_token}"}

            async with aiohttp.ClientSession() as session:
                async with session.post(
                        "https://api.homingai.com/ha/home/tts",
                        headers=headers,
                        json={"text": message},
                        timeout=10
                ) as response:
                    if response.status != 200:
                        _LOGGER.error("HTTP error %d: %s", response.status, await response.text())
                        return None, None

                    data = await response.read()
                    jsdata = json.loads(data)
                    if jsdata['code'] != 200:
                        _LOGGER.error("API error: %s", jsdata['msg'])
                        return None, None

                    # Decode audio data
                    audio_data = base64.b64decode(jsdata['body'])
                    _LOGGER.debug("Audio data length: %d bytes", len(audio_data))

                    # Return MP3 format directly to avoid conversion issues
                    return ("mp3", audio_data)

        except asyncio.TimeoutError:
            _LOGGER.error("Timeout requesting TTS")
            return None, None
        except aiohttp.ClientError as err:
            _LOGGER.error("Error requesting TTS: %s", str(err))
            return None, None
        except Exception as err:
            _LOGGER.error("Unexpected error requesting TTS: %s", str(err))
            return None, None
