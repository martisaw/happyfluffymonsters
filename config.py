from dotenv import load_dotenv
import os
import logging
import json

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

logger = logging.getLogger(__name__)

# General
current_file_path = os.path.abspath(__file__)
current_directory_path = os.path.dirname(current_file_path)

IMAGE_FOLDER_PATH = os.path.abspath(current_directory_path + "/img")

if not os.path.exists(IMAGE_FOLDER_PATH):
    os.makedirs(IMAGE_FOLDER_PATH)

env_mode = os.getenv("ENV_MODE", "dev")
ENV_IS_DEV = True

if env_mode == "prod":
    load_dotenv(os.path.abspath(current_directory_path + "/hfm.env.prod"))
    logger.info("********** PROD MODE **********")
    ENV_IS_DEV = False
else:
    load_dotenv(os.path.abspath(current_directory_path + "/hfm.env.dev"))
    logger.info("********** DEV MODE **********")

# OpenAI Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ACTIVITY_TEMPERATURE = float(os.getenv("OPENAI_ACTIVITY_TEMPERATURE"))
PROMPT_TEMPERATURE = float(os.getenv("OPENAI_PROMPT_TEMPERATURE"))
GPT_MODEL = os.getenv("OPENAI_GPT_MODEL")
DALLE_MODEL = os.getenv("OPENAI_DALLE_MODEL")
DALLE_N = int(os.getenv("OPENAI_DALLE_N"))

if DALLE_MODEL == "dall-e-3":
    DALLE_N = 1  # API Limitations

# TelegramBot Configuration
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
SPECIAL_USERS = json.loads(
    os.getenv("TELEGRAM_ALLOWED_USERS")
)  # Only allows predefined users
MONSTER_MONDAY_CHAT_ID = os.getenv("TELEGRAM_REMINDER_CHAT_ID")
