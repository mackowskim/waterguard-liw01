# Water Guardian LIW-01

Integracja Home Assistant dla licznika wody ZAMEL LIW-01, z automatycznym tworzeniem helperów dla blueprint Water Guardian.

## Funkcje

- Automatyczne wykrywanie LIW-01 po MQTT
- Tworzy 24 input_number godzinowe + EMA 14-dniową
- Tworzy utility_meter hourly
- EMA aktualizowana w **59 minucie każdej godziny**
- Kompatybilne z blueprint Water Guardian
- Obsługa zarówno jednostek m³ jak i L

## Instalacja przez HACS

1. Dodaj repo: `https://github.com/mackowskim/waterguard-liw01`
2. Wybierz wersję `v0.1.3` w HACS
3. Dodaj integrację przez UI lub YAML
