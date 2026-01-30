"""Water Guardian LIW-01 sensors – dynamic MQTT detection
Author: M4hSzyna (@mackowskim)
"""

import json
from homeassistant.components.sensor import SensorEntity
from homeassistant.components.mqtt import async_subscribe
from homeassistant.core import callback, HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

async def async_setup_platform(hass: HomeAssistant, config, async_add_entities: AddEntitiesCallback, discovery_info=None):
    """Add dynamic Water Guardian LIW-01 sensors."""
    async_add_entities([
        WaterGuardLIW01ValueSensor(hass),
        WaterGuardLIW01CostSensor(hass)
    ])

class WaterGuardLIW01ValueSensor(SensorEntity):
    """Total water value (m³ or L) from LIW-01."""

    _attr_name = "Water Guardian LIW-01 Total Value"
    _attr_unit_of_measurement = "m³"
    _attr_icon = "mdi:water-pump"

    def __init__(self, hass: HomeAssistant):
        self._state = None
        self.hass = hass

        topic_pattern = "homeassistant/sensor/+/+/config"
        hass.async_create_task(self.subscribe_config(topic_pattern))

    async def subscribe_config(self, topic_pattern):
        @callback
        def config_received(msg):
            try:
                data = json.loads(msg.payload)
                if data.get("device", {}).get("name") != "ZAMEL LIW-01":
                    return
                if data.get("dev_cla") != "water":
                    return

                base = data.get("~")
                stat_t = data.get("stat_t", "")
                unit = data.get("unit_of_meas", "m³")

                stat_topic = base + stat_t.replace("~/", "/")

                # Subskrypcja stanu
                async def value_received(msg2):
                    try:
                        val = float(msg2.payload)
                        if unit.lower() in ["m³", "m3", "m^3"]:
                            val *= 1000  # m³ -> L
                            self._attr_unit_of_measurement = "L"
                        else:
                            self._attr_unit_of_measurement = unit
                        self._state = round(val, 3)
                        self.schedule_update_ha_state()
                    except Exception:
                        pass

                self.hass.async_create_task(async_subscribe(self.hass, stat_topic, value_received))
            except Exception:
                pass

        self.hass.async_create_task(async_subscribe(self.hass, topic_pattern, config_received))

    @property
    def state(self):
        return self._state

class WaterGuardLIW01CostSensor(SensorEntity):
    """Total water cost (PLN) from LIW-01."""

    _attr_name = "Water Guardian LIW-01 Total Cost"
    _attr_unit_of_measurement = "PLN"
    _attr_icon = "mdi:currency-usd"

    def __init__(self, hass: HomeAssistant):
        self._state = None
        self.hass = hass

        topic_pattern = "homeassistant/sensor/+/+/config"
        hass.async_create_task(self.subscribe_config(topic_pattern))

    async def subscribe_config(self, topic_pattern):
        @callback
        def config_received(msg):
            try:
                data = json.loads(msg.payload)
                if data.get("device", {}).get("name") != "ZAMEL LIW-01":
                    return
                if data.get("dev_cla") != "monetary":
                    return

                base = data.get("~")
                stat_t = data.get("stat_t", "")

                stat_topic = base + stat_t.replace("~/", "/")

                # Subskrypcja stanu
                async def cost_received(msg2):
                    try:
                        val = float(msg2.payload)
                        self._state = round(val, 2)
                        self.schedule_update_ha_state()
                    except Exception:
                        pass

                self.hass.async_create_task(async_subscribe(self.hass, stat_topic, cost_received))
            except Exception:
                pass

        self.hass.async_create_task(async_subscribe(self.hass, topic_pattern, config_received))

    @property
    def state(self):
        return self._state
