"""Helper creation for Water Guardian LIW-01, including EMA."""
from homeassistant.core import HomeAssistant

async def setup_helpers(hass: HomeAssistant):
    """Create input_number and utility_meter for Water Guardian LIW-01."""

    # Input numbers – główne
    input_numbers = {
        "waterguard_liw01_last_hour": {"name": "Water Guardian – last hour [L]", "min":0,"max":5000,"step":1,"unit_of_measurement":"L"},
        "waterguard_liw01_leak_streak": {"name": "Water Guardian – leak streak [h]", "min":0,"max":24,"step":1,"unit_of_measurement":"h"},
        "waterguard_liw01_zero_hour_streak": {"name": "Water Guardian – zero hour streak [h]", "min":0,"max":24,"step":1,"unit_of_measurement":"h"},
        "waterguard_liw01_avg_hourly": {"name": "Water Guardian – EMA 14d hourly", "min":0,"max":5000,"step":1,"unit_of_measurement":"L"},
    }

    # 24 input_number godzinowe
    for h in range(24):
        entity_id = f"waterguard_liw01_hour_{h}"
        input_numbers[entity_id] = {"name": f"Water Guardian – hour {h}", "min":0,"max":5000,"step":1,"unit_of_measurement":"L"}

    # Tworzenie encji jeśli nie istnieją
    for entity_id, config in input_numbers.items():
        if not hass.states.get(f"input_number.{entity_id}"):
            await hass.services.async_call("input_number", "create", config)

    # Utility meter – hourly, zlicza całkowite zużycie LIW-01
    if not hass.states.get("sensor.waterguard_liw01_hourly_meter"):
        await hass.services.async_call(
            "utility_meter",
            "create",
            {
                "name": "Water Guardian – hourly meter",
                "source": "sensor.waterguard_liw01_value",
                "cycle": "hourly",
                "tariffs": ["hourly"]
            }
        )
