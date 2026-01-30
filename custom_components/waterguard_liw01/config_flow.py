"""Config flow for Water Guardian LIW-01 integration."""
from homeassistant import config_entries
import voluptuous as vol
from homeassistant.const import CONF_NAME, CONF_UNIT_OF_MEASUREMENT

DOMAIN = "waterguard_liw01"

DEFAULT_NAME = "Water Guardian LIW-01"
DEFAULT_UNIT = "m³"

class WaterGuardConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Water Guardian LIW-01."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        errors = {}

        if user_input is not None:
            # tutaj integracja sama wykryje encję LIW-01 po MQTT
            return self.async_create_entry(
                title=user_input[CONF_NAME],
                data=user_input
            )

        # formularz konfiguracji
        schema = vol.Schema(
            {
                vol.Optional(CONF_NAME, default=DEFAULT_NAME): str,
                vol.Optional(CONF_UNIT_OF_MEASUREMENT, default=DEFAULT_UNIT): str,
                vol.Optional("currency", default="PLN"): str,
            }
        )

        return self.async_show_form(
            step_id="user",
            data_schema=schema,
            errors=errors
        )
