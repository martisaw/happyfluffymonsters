from facade.openai_client import generate_images
from openai.types.image import Image
import logging
from config import DALLE_MODEL, DALLE_N, ENV_IS_DEV
import requests
import os
from telegram import InputMediaPhoto
from config import IMAGE_FOLDER_PATH

logger = logging.getLogger(__name__)


def _add_styles(prompt):
    return prompt.replace(".", ", illustration, digital painting")


def _download_image(prompt, image_url, image_number):
    filename = prompt.replace(" ", "_").replace(".", "").lower()
    try:
        response = requests.get(image_url)
        if response.status_code == 200:
            with open(
                os.path.abspath(
                    IMAGE_FOLDER_PATH + "/" + filename + image_number + ".png"
                ),
                "wb",
            ) as img_file:
                img_file.write(response.content)
    except Exception as e:
        logging.error("Exception occured: %s", e)
        return


def generate_styled_images(prompt):
    if ENV_IS_DEV:
        return [
            Image(
                revised_prompt=prompt,
                url="https://upload.wikimedia.org/wikipedia/commons/3/35/Basic_human_drawing.png",
            ),
            Image(
                revised_prompt=prompt,
                url="https://upload.wikimedia.org/wikipedia/commons/3/35/Basic_human_drawing.png",
            ),
        ]
    else:
        styled_prompt = _add_styles(prompt)
        logger.info("images (%s): ", styled_prompt)
        return generate_images(styled_prompt, DALLE_MODEL, DALLE_N)


async def generate_image_proposal(prompt, image_list):
    count = 1
    media_list = []
    for image in image_list:
        caption = "#" + str(
            count
        )  # Ensure to differentiate between n>1 pictures for one prompt
        _download_image(prompt, image.url, caption)
        media_list.append(InputMediaPhoto(media=image.url, caption=caption))
        count = count + 1
    return media_list
