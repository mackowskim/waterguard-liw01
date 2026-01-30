"""Water Guardian LIW-01 helpers
Author: M4hSzyna (@mackowskim)
"""

from homeassistant.core import HomeAssistant

async def setup_helpers(hass: HomeAssistant):
    """Create all input_number and input_datetime helpers needed by Water Guardian."""

    # Input datetime – last alert
    if "input_datetime.waterguard_last_alert" not in hass.states.async_entity_ids():
        await hass.services.async_call(
            "input_datetime",
            "create",
            {
                "name": "Water Guardian Last Alert",
                "has_date": True,
                "has_time": True,
                "entity_id": "input_datetime.waterguard_last_alert"
            },
            blocking=True
        )

    # Input numbers – streaks
    for name, friendly in [
        ("waterguard_leak_streak", "Leak Streak"),
        ("waterguard_zero_hour_streak", "Zero Hour Streak")
    ]:
        entity_id = f"input_number.{name}"
        if entity_id not in hass.states.async_entity_ids():
            await hass.services.async_call(
                "input_number",
                "create",
                {
                    "name": friendly,
                    "min": 0,
                    "max": 100,
                    "step": 1,
                    "mode": "box",
                    "entity_id": entity_id
                },
                blocking=True
            )

    # EMA hourly consumption – 24 input_numbers
    for h in range(24):
        entity_id = f"input_number.waterguard_hourly_consumption_{h}"
        if entity_id not in hass.states.async_entity_ids():
            await hass.services.async_call(
                "input_number",
                "create",
                {
                    "name": f"Hourly Consumption {h}:00",
                    "min": 0,
                    "max": 500,
                    "step": 1,
                    "mode": "box",
                    "entity_id": entity_id
                },
                blocking=True
            )
