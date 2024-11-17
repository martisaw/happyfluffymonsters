# happyfluffymonsters

Powering @happyfluffymonsters Telegram chatbot. Read my [blog post](https://blog.sawilla.cloud/the-happy-fluffy-monsters-telegram-chatbot/).

## Conventional Commits

This projects uses Conventional Commits (or at least I try). For more information see this [Website](https://www.conventionalcommits.org/en/v1.0.0/).

## Python Virtual Environment (on Windows)

Use `python -m venv ./venv` to create a virtual environment within this folder.

Use `./venv/Scripts/activate.ps1` to activate the virtual environment.

## Requirements

`pip install -r requirements.txt`

`pip install -r requirements.txt --upgrade --upgrade-strategy eager` -> to update sub-dependencies too

## Linux Setup (My Bot runs on a RaspberryPi 4)

1. Create virtual python environment
2. Not entirely sure, but make the script executable for cron `chmod +x bot.py`
3. Use the /path/to/pip or /path/to/python to user venv
4. Add to cron `crontab -e` = `@reboot sleep 60 && path/to/venv/python path/to/bot.py >> path/to/log 2>&1` -> Sleep as a workaround of some networking issues on startup (something's not powered up yet)

## Configuration Properties

Check out the sample config file `hfm.env.dev.example`. I'll have two Bots: One for Developing (`hfm.env.dev`) and the other for Production (`hfm.env.prod`). To use the prod-environmnent, I have to set an environment variable called `ENV_MODE=prod`.

The telegram chat_id of you and the bot can be easily figured out. Check some guides for that.

In Powershell, I can to this by setting `$env:ENV_MODE = "prod"`.
