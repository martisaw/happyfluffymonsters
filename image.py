from openaiw import generate_images
from openai.types.image import Image
import logging
from config import DALLE_MODEL, DALLE_N, DEV_MODE

logger = logging.getLogger(__name__)


def add_styles(prompt):
    return prompt.replace(".", ", illustration, digital painting")


def images(prompt):
    if DEV_MODE:
        logger.info("images dev mode")
        return [
            Image(
                revised_prompt=prompt,
                url="https://upload.wikimedia.org/wikipedia/commons/thumb/d/dd/Friendly_stickman.svg/400px-Friendly_stickman.svg.png",
            ),
            Image(
                revised_prompt=prompt,
                url="https://upload.wikimedia.org/wikipedia/commons/thumb/d/dd/Friendly_stickman.svg/400px-Friendly_stickman.svg.png",
            ),
        ]
    styled_prompt = add_styles(prompt)
    logger.info("images (%s): ", styled_prompt)
    return generate_images(styled_prompt, DALLE_MODEL, DALLE_N)
