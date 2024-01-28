from dotenv import load_dotenv
import os
import logging
import platform
import json

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

logger = logging.getLogger(__name__)

# Load all environment variables
load_dotenv(os.path.abspath("hfm.env"))

# General
IMAGE_FOLDER_PATH = os.path.abspath("img")

# OpenAI Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ACTIVITY_TEMPERATURE = 1.2
PROMPT_TEMPERATURE = 1.0
GPT_MODEL = "gpt-3.5-turbo-1106"
DALLE_MODEL = "dall-e-2"
DALLE_N = 4

# Telegram Bot Configuration
if platform.system() == "Windows":
    DEV_MODE = True
    BOT_TOKEN = os.getenv("DEV_TOKEN")
    logger.info("********** DEV MODE **********")
else:
    DEV_MODE = False
    BOT_TOKEN = os.getenv("TOKEN")
    logger.info("********** PROD MODE **********")
SPECIAL_USERS = json.loads(
    os.getenv("MASTER_USER_ARRAY")
)  # Only allows predefined users
MONSTER_MONDAY_CHAT_ID = os.getenv("REMINDER_CHAT_ID")
