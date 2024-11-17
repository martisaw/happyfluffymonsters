from config import OPENAI_API_KEY
import logging
from openai import OpenAI

logger = logging.getLogger(__name__)

openai_client = OpenAI(api_key=OPENAI_API_KEY)


def generate_images(prompt, model, n):
    try:
        logger.info("generate_images (%s, %s, %s): ", prompt, model, n)
        return openai_client.images.generate(
            model=model, prompt=prompt, n=n, user="happyfluffymonstersbot"
        ).data
    except Exception as e:
        logging.error("Exception occured: %s", e)
        return []


def _message_to_dict(ChatCompletionsMessage):
    return {
        "role": ChatCompletionsMessage.role,
        "content": ChatCompletionsMessage.content,
    }


def generate_text(messages, model, temperature) -> dict:
    try:
        logging.info(
            "generate_text (%s, %s, %s): ",
            messages,
            model,
            temperature,
        )
        message = (
            openai_client.chat.completions.create(
                model=model, messages=messages, temperature=temperature
            )
            .choices[0]
            .message
        )
        return _message_to_dict(message)
    except Exception as e:
        logging.error("Exception occured: %s", e)
        return "error occurred"


def generate_text_with_limited_history(messages, model, temperature, count) -> dict:
    if len(messages >= count):
        messages = messages[-count:]
    return generate_text(messages, model, temperature)
