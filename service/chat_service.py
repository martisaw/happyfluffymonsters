from facade.openai_client import generate_text
from service.prompt_vars import random_location, random_monster
import logging
from config import GPT_MODEL, ACTIVITY_TEMPERATURE, PROMPT_TEMPERATURE, ENV_IS_DEV


logger = logging.getLogger(__name__)


def _get_activity_for_location(location):
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {
            "role": "user",
            "content": f"Create a list for me with 10 unique activities to do in {location}. Then, choose one activity. Only return the activity. Maximum 5 words. No markdown, just plain text.",
        },
    ]
    # FIXME when underlying functions returns an error string, this will not work!
    logger.info("random_activity (%s): ", messages[1]["content"])
    response = generate_text(messages, GPT_MODEL, ACTIVITY_TEMPERATURE)["content"]
    # Return looks like this:
    # 1. Read a new book.
    # 2. Meditate for relaxation.
    # 3. Have a spa night.
    # 4. Write in a journal.
    # 5. Do a puzzle.
    # 6. Try online yoga class.
    # 7. Experiment with new recipes.
    # 8. Create a vision board.
    # 9. Watch a documentary.
    # 10. Listen to calming music.

    # Experiment with new recipes.
    return response.split("\n")[-1]


def generate_random_prompt():
    if ENV_IS_DEV:
        return "A stickman."
    else:
        location = random_location()
        activity = _get_activity_for_location(location)
        n_monster = random_monster()
        messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            {
                "role": "user",
                "content": f"Write a short sentence in present with '{n_monster}', '{activity}' and '{location}'",
            },
        ]
        logger.info("random_prompt (%s)", messages[1]["content"])
        messages.append(generate_text(messages, GPT_MODEL, PROMPT_TEMPERATURE))
        messages.append(
            {
                "role": "user",
                "content": "Add a playful item or activity to this sentence.",
            },
        )
        return generate_text(messages, GPT_MODEL, PROMPT_TEMPERATURE)["content"]
