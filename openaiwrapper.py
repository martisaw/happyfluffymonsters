import openai
import os
from dotenv import load_dotenv
import logging

# Load all variables from .env file
load_dotenv('./hfm.env')

# CONFIG
dalle_n_pictures = 2
dalle_picture_size = 256

# openai.organization = "personal"
openai.api_key = os.getenv('API_KEY')

def get_image_size_string(number):
    if not isinstance(number, int):
        logging.warning('input was not an integer. returning default.')
    match number:
        case 256: 
            return '256x256'
        case 512:
            return '512x512'
        case 1024:
            return '1024x1024'
        case _:
            logging.warning(f'could not match {number} to 256, 512 or 1024. returning default.')
            return '256x256'

def talk_to_dalle(input_prompt, input_n, input_size):
    try:
      return openai.Image.create(
        prompt = input_prompt,
        n = input_n,
        size = get_image_size_string(input_size)
      )['data']
    except openai.error.OpenAIError as e:
      logging.error(e.http_status)
      logging.error(e.error)

def create_images(input_prompt):
    input_prompt_with_style = input_prompt + ', digital art.'
    return talk_to_dalle(input_prompt_with_style, dalle_n_pictures, dalle_picture_size)
