import random
from openaiw import generate_chat_completions
from prompt_vars import big_cities, countries, monsters
import logging
from config import GPT_MODEL, ACTIVITY_TEMPERATURE, PROMPT_TEMPERATURE, DEV_MODE


logger = logging.getLogger(__name__)


def random_activity(location_list):
    activity_prompt = [
        {"role": "system", "content": "You are a helpful assistant."},
        {
            "role": "user",
            "content": f"Create a list for me with 10 unique activities to do in {random.choice(location_list)}. Then, choose one activity. Only return the activity. Maximum 5 words. No markdown, just plain text.",
        },
    ]
    logger.info("random_activity (%s): ", activity_prompt[1]["content"])
    response = generate_chat_completions(
        activity_prompt, GPT_MODEL, ACTIVITY_TEMPERATURE
    )
    # returns a list 1. 2. 3. and at the end, seperated by two line breaks the chosen activity.
    return response.split("\n")[-1]


def random_prompt():
    if DEV_MODE:
        logger.info("random_prompt dev mode")
        return "An image of a stickman."

    activity = random_activity(big_cities)
    monster_prompt = [
        {"role": "system", "content": "You are a helpful assistant."},
        {
            "role": "user",
            "content": f"Write a short sentence in present with '{random.choice(monsters)}' and {activity}",
        },
    ]
    logger.info("random_prompt (%s)", monster_prompt[1]["content"])
    return generate_chat_completions(monster_prompt, GPT_MODEL, PROMPT_TEMPERATURE)
