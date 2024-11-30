from facade.openai_client import generate_text, generate_text_with_structured_output
from service.prompt_vars import random_location, random_monster
import logging
import random
from config import GPT_MODEL, ACTIVITY_TEMPERATURE, PROMPT_TEMPERATURE, ENV_IS_DEV
from structured_outputs.pydantic_classes import Activities


logger = logging.getLogger(__name__)


def _get_activity_for_location(location):
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {
            "role": "user",
            "content": f"Create a list for me with 10 unique activities to do in {location}. Only return the activity. Maximum 5 words. Plain Text.",
        },
    ]
    # FIXME refusal case not handled
    logger.info("random_activity (%s): ", messages[1]["content"])
    response = generate_text_with_structured_output(
        messages, GPT_MODEL, ACTIVITY_TEMPERATURE, Activities
    ).activities
    logger.info("RESPONSE %s", response)
    return random.choice(response)


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
