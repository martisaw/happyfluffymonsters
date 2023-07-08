import openai
import os
from dotenv import load_dotenv
import logging

class OpenAiWrapper:
    def __init__(self, dalle_n_pictures=2, dalle_picture_size=256) -> None:
        load_dotenv('./hfm.env')
        openai.api_key = os.getenv('API_KEY')

        self.dalle_n_pictures = dalle_n_pictures
        self.dalle_picture_size = dalle_picture_size
    
    def __get_image_size_string(self, number):
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

    def __talk_to_dalle(self, input_prompt):
        try:
            return openai.Image.create(
                prompt = input_prompt,
                n = self.dalle_n_pictures,
                size = self.__get_image_size_string(self.dalle_picture_size)
            )['data']
        except openai.error.OpenAIError as e:
            logging.error(e.http_status)
            logging.error(e.error)

    def create_images(self, input_prompt):
        input_prompt_with_style = input_prompt + ', digital art.'
        return self.__talk_to_dalle(input_prompt_with_style)
