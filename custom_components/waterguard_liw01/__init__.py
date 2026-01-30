"""Water Guardian LIW-01 integration
Author: M4hSzyna (@mackowskim)
"""

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from .helpers import setup_helpers

DOMAIN = "waterguard_liw01"

async def async_setup(hass: HomeAssistant, config: dict):
    """Setup integration via YAML (optional)."""
    await setup_helpers(hass)
    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Set up integration from a config entry (UI)."""
    await setup_helpers(hass)
    await hass.config_entries.async_forward_entry_setup(entry, "sensor")
    return True
