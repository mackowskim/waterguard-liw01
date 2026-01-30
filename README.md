# Water Guardian LIW-01 Integration

Author: M4hSzyna (@mackowskim)

## Features

- Automatic detection of LIW-01 devices via MQTT
- Creates all required input helpers for Water Guardian blueprint
- Creates sensors:
  - `sensor.waterguard_liw01_total_value` – total water usage (m³ or L)
  - `sensor.waterguard_liw01_total_cost` – total cost in PLN
- Creates `utility_meter.waterguard_liw01_hourly_consumption` automatically
- Input helpers for streaks and EMA (English names)

## Installation via HACS

1. Add repository: `https://github.com/mackowskim/hacs-liw01`  
2. Install `Water Guardian LIW-01`  
3. Restart Home Assistant  

## Usage with Blueprint

- `water_hour_meter` → `utility_meter.waterguard_liw01_hourly_consumption`
- `notify_device`, `notify_device_secondary`, `media_players` → any HA entities
