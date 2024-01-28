from config import OPENAI_API_KEY
import logging
from openai import OpenAI

logger = logging.getLogger(__name__)

openai_client = OpenAI(OPENAI_API_KEY)


def generate_images(prompt, model, n):
    try:
        logger.info("generate_images (prompt, model, n): ", prompt, model, n)
        return openai_client.images.generate(
            model=model, prompt=prompt, n=n, user="happyfluffymonstersbot"
        ).data
    except Exception as e:
        logging.error("Exception occured: ", e)
        return []


def generate_chat_completions(messages, model, temperature):
    try:
        logging.info(
            "generate_chat_completions (messages, model, temperature): ",
            messages,
            model,
            temperature,
        )
        return (
            openai_client.chat.completions.create(
                model=model, messages=messages, temperature=temperature
            )
            .choices[0]
            .message.content
        )
    except Exception as e:
        logging.error("Exception occured: ", e)
        return "error occurred"
