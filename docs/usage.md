# Usage

```
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python -m arc_esp --config config/default.yaml
```

Hotkeys:

- `F8` — toggle ESP
- `End` — panic exit

Config lives in `config/default.yaml`. Aimbot is disabled by default; enable by
setting `aimbot.enabled: true` or pressing `F8` twice.

## Disclaimer

For educational / research use only. Using this against live servers violates
the game's Terms of Service and may result in a ban. Use at your own risk.