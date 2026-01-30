"""Sensors for Water Guardian LIW-01 with EMA calculation."""

from homeassistant.helpers.entity import Entity
from homeassistant.core import HomeAssistant
import datetime
import asyncio

async def async_setup_entry(hass: HomeAssistant, entry, async_add_entities):
    sensors = [WaterGuardianValueSensor(hass)]
    async_add_entities(sensors)

class WaterGuardianValueSensor(Entity):
    """Water consumption sensor with hourly EMA."""

    def __init__(self, hass):
        self._state = None
        self._name = "Water Guardian LIW-01 Value"
        self.hass = hass
        hass.loop.create_task(self.hourly_ema_loop())

    @property
    def name(self):
        return self._name

    @property
    def state(self):
        return self._state

    async def async_update(self):
        """Fetch latest LIW-01 value from MQTT discovery."""
        for entity in self.hass.states.async_all().values():
            if "supla" in entity.entity_id and "calculated_value" in entity.entity_id:
                self._state = float(entity.state)
                await self.hass.services.async_call(
                    "input_number",
                    "set_value",
                    {"entity_id": "input_number.waterguard_liw01_last_hour", "value": self._state}
                )

    async def hourly_ema_loop(self):
        """Update EMA in 59th minute of each hour."""
        while True:
            now = datetime.datetime.now()
            if now.minute == 59:
                await self.update_hourly_ema()
                await asyncio.sleep(61)  # avoid double calculation
            else:
                await asyncio.sleep(10)

    async def update_hourly_ema(self):
        now = datetime.datetime.now()
        current_hour = now.hour

        try:
            current_value = float(self.hass.states.get(f"input_number.waterguard_liw01_hour_{current_hour}").state)
        except:
            current_value = 0.0

        try:
            prev_ema = float(self.hass.states.get("input_number.waterguard_liw01_avg_hourly").state)
        except:
            prev_ema = 0.0

        N = 14
        k = 2 / (N + 1)
        ema = (current_value * k) + (prev_ema * (1 - k))

        await self.hass.services.async_call(
            "input_number",
            "set_value",
            {"entity_id": "input_number.waterguard_liw01_avg_hourly", "value": round(ema,1)}
        )

        await self.hass.services.async_call(
            "input_number",
            "set_value",
            {"entity_id": f"input_number.waterguard_liw01_hour_{current_hour}", "value": current_value}
        )
