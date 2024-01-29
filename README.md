# happyfluffymonsters

Powering @happyfluffymonsters

## Conventional Commits

This projects uses Conventional Commits. For more information see this [Website](https://www.conventionalcommits.org/en/v1.0.0/).

## Python Virtual Environment

Use `python -m venv ./venv` to create a virtual environment within this folder.

Use `./venv/Scripts/activate.ps1` to activate the virtual environment.

## Requirements

`pip install -r requirements.txt`

`pip install -r requirements.txt --upgrade --upgrade-strategy eager` -> Für Sub-Dependencies

## OPEN AI API

https://platform.openai.com/docs/api-reference

https://github.com/openai/openai-cookbook/blob/main/examples/How_to_format_inputs_to_ChatGPT_models.ipynb

## Linux Setup

1. Create virtual python environment
2. Not entirely sure, but make the script executable for cron `chmod +x bot.py`
3. Add to cron `crontab -e` = `@reboot sleep 15 && python bot.py` -> Sleep as a workaround of some networking issues on startup (something's not powered up yet)
