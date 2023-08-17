import openai
import logging
import random
import datetime

logger = logging.getLogger(__name__)

class OpenAiWrapper:
    
    countries = [
        'Afghanistan', 'Albania', 'Algeria', 'Andorra', 'Angola', 'Antigua and Barbuda', 'Argentina',
        'Armenia', 'Australia', 'Austria', 'Azerbaijan', 'Bahamas', 'Bahrain', 'Bangladesh', 'Barbados',
        'Belarus', 'Belgium', 'Belize', 'Benin', 'Bhutan', 'Bolivia', 'Bosnia and Herzegovina', 'Botswana',
        'Brazil', 'Brunei', 'Bulgaria', 'Burkina Faso', 'Burundi', 'Cabo Verde', 'Cambodia', 'Cameroon',
        'Canada', 'Central African Republic', 'Chad', 'Chile', 'China', 'Colombia', 'Comoros', 'Congo',
        'Costa Rica', 'Croatia', 'Cuba', 'Cyprus', 'Czech Republic', 'Democratic Republic of the Congo',
        'Denmark', 'Djibouti', 'Dominica', 'Dominican Republic', 'East Timor', 'Ecuador', 'Egypt',
        'El Salvador', 'Equatorial Guinea', 'Eritrea', 'Estonia', 'Eswatini', 'Ethiopia', 'Fiji', 'Finland',
        'France', 'Gabon', 'Gambia', 'Georgia', 'Germany', 'Ghana', 'Greece', 'Grenada', 'Guatemala',
        'Guinea', 'Guinea-Bissau', 'Guyana', 'Haiti', 'Honduras', 'Hungary', 'Iceland', 'India',
        'Indonesia', 'Iran', 'Iraq', 'Ireland', 'Israel', 'Italy', 'Ivory Coast', 'Jamaica', 'Japan',
        'Jordan', 'Kazakhstan', 'Kenya', 'Kiribati', 'Korea, North', 'Korea, South', 'Kosovo', 'Kuwait',
        'Kyrgyzstan', 'Laos', 'Latvia', 'Lebanon', 'Lesotho', 'Liberia', 'Libya', 'Liechtenstein', 'Lithuania',
        'Luxembourg', 'Madagascar', 'Malawi', 'Malaysia', 'Maldives', 'Mali', 'Malta', 'Marshall Islands',
        'Mauritania', 'Mauritius', 'Mexico', 'Micronesia', 'Moldova', 'Monaco', 'Mongolia', 'Montenegro',
        'Morocco', 'Mozambique', 'Myanmar', 'Namibia', 'Nauru', 'Nepal', 'Netherlands', 'New Zealand',
        'Nicaragua', 'Niger', 'Nigeria', 'North Macedonia', 'Norway', 'Oman', 'Pakistan', 'Palau',
        'Palestine', 'Panama', 'Papua New Guinea', 'Paraguay', 'Peru', 'Philippines', 'Poland', 'Portugal',
        'Qatar', 'Romania', 'Russia', 'Rwanda', 'Saint Kitts and Nevis', 'Saint Lucia',
        'Saint Vincent and the Grenadines', 'Samoa', 'San Marino', 'Sao Tome and Principe', 'Saudi Arabia',
        'Senegal', 'Serbia', 'Seychelles', 'Sierra Leone', 'Singapore', 'Slovakia', 'Slovenia',
        'Solomon Islands', 'Somalia', 'South Africa', 'South Sudan', 'Spain', 'Sri Lanka', 'Sudan',
        'Suriname', 'Sweden', 'Switzerland', 'Syria', 'Taiwan', 'Tajikistan', 'Tanzania', 'Thailand',
        'Togo', 'Tonga', 'Trinidad and Tobago', 'Tunisia', 'Turkey', 'Turkmenistan', 'Tuvalu', 'Uganda',
        'Ukraine', 'United Arab Emirates', 'United Kingdom', 'United States', 'Uruguay', 'Uzbekistan',
        'Vanuatu', 'Vatican City', 'Venezuela', 'Vietnam', 'Yemen', 'Zambia', 'Zimbabwe'
    ]
    
    big_cities = [
        "Tokyo", "New York City", "London", "Paris", "Beijing",
        "Moscow", "Cairo", "Rio de Janeiro", "Sydney", "Toronto",
        "Berlin", "Rome", "Bangkok", "Dubai", "Mumbai",
        "Los Angeles", "Istanbul", "Seoul", "Mexico City", "Cape Town",
        "Jakarta", "Madrid", "Buenos Aires", "Lima", "Nairobi",
        "Amsterdam", "Stockholm", "New Delhi", "Vienna", "Athens",
        "Prague", "Budapest", "Hong Kong", "Singapore", "Kuala Lumpur",
        "Oslo", "Copenhagen", "Warsaw", "Zurich", "Helsinki",
        "Dublin", "Lisbon", "Brussels", "Riyadh", "Doha",
        "Manila", "Hanoi", "Brasília", "Ottawa", "Havana",
        "Bogotá", "Caracas", "Santiago", "Montevideo", "Ljubljana",
        "Reykjavik", "Panama City", "San Juan", "Bucharest", "Kiev",
        "Tehran", "Baghdad", "Damascus", "Kabul", "Islamabad",
        "Kathmandu", "Dhaka", "Colombo", "Nicosia", "Vilnius",
        "Tallinn", "Belgrade", "Tirana", "Tbilisi", "Yerevan",
        "Baku", "Ashgabat", "Astana", "Ulaanbaatar", "Bishkek",
        "Tashkent", "Kuala Lumpur", "Manama", "Muscat", "Abu Dhabi",
        "Doha", "Nur-Sultan", "Bogota", "Quito", "La Paz",
        "Asuncion", "Paramaribo", "Georgetown", "Bridgetown", "Nassau",
        "Kingston", "Port-au-Prince", "San Salvador", "Guatemala City", "Belmopan",
        "Tegucigalpa", "Managua", "San Jose", "Panama City", "Lima",
        "Caracas", "Buenos Aires", "Montevideo", "Santiago", "Brasilia",
        "La Paz", "Sucre", "Quito", "Paramaribo", "Georgetown",
        "Bridgetown", "Nassau", "Kingston", "Port-au-Prince", "San Salvador",
        "Guatemala City", "Belmopan", "Tegucigalpa", "Managua", "San Jose"
    ]

    def __init__(self, openai_api_key=None, dalle_n_pictures=2, dalle_picture_size=256, chatGPT_model='gpt-4') -> None:
        openai.api_key = openai_api_key

        self.dalle_n_pictures = dalle_n_pictures
        self.dalle_picture_size = dalle_picture_size

        self.chatGPT_model=chatGPT_model

        logger.info(f'Initialized OpenAiWrapper with dalle_n_pictures={self.dalle_n_pictures}, dalle_pictures_size={self.dalle_picture_size} and chatGPT_model={self.chatGPT_model}')
    
    def __get_image_size_string(self, number):
        if not isinstance(number, int):
            logger.warning('input was not an integer. returning default.')
        match number:
            case 256: 
                return '256x256'
            case 512:
                return '512x512'
            case 1024:
                return '1024x1024'
            case _:
                logger.warning(f'could not match {number} to 256, 512 or 1024. returning default.')
                return '256x256'

    def __talk_to_dalle(self, input_prompt):
        try:
            return openai.Image.create(
                prompt = input_prompt,
                n = self.dalle_n_pictures,
                size = self.__get_image_size_string(self.dalle_picture_size)
            )['data']
        except openai.error.OpenAIError as e:
            logger.error(e.http_status)
            logger.error(e.error)

    def create_images(self, input_prompt): # TODO make style a parameter TODO check that input prompt < 1000
        input_prompt = input_prompt.replace('.', '') 
        input_prompt_with_style = input_prompt + ', digital art'
        logger.info(f'Creating images for prompt: {input_prompt_with_style}')
        return self.__talk_to_dalle(input_prompt_with_style)
    
    def __talk_to_chatGPT(self, messages) -> str:
        try:
            return openai.ChatCompletion.create(
                model=self.chatGPT_model,
                messages=messages,
                temperature=1.0
            ).choices[0].message.content
        except openai.error.OpenAIError as e:
            logger.error(e.http_status)
            logger.error(e.error)
    
    def create_randomized_prompt(self):
        n_monsters = random.randint(1,3)
        n_years_ago = random.randint(3,20)
        date_n_years_ago = (datetime.datetime.now() - datetime.timedelta(days=n_years_ago*365)).strftime('%Y-%m-%d')
        city = random.choice(self.big_cities)
        monster_question = None
        if n_monsters == 1:
            monster_question = 'What is a happy fluffy monster doing in this city on that date?'
        else:
            monster_question = f'What are {n_monsters} happy fluffy monsters doing in this city on that date?'
        
        messages=[
            {'role': 'system', 'content': 'You are a helpful assistant.'},
            {'role': 'system', 'content': f'Answer in one sentence. Do not mention the date. Do not mention {city}.'},
            {'role': 'user', 'content': f'Imagine today it\'s {date_n_years_ago}, you are in {city} and a \'happy fluffy monster\' is another term for human. {monster_question}'},
            {'role': 'user', 'content': 'Only tell what is happening. Focus on only one activity.'},
            {'role': 'system', 'name':'example_assistant', 'content': 'Two happy fluffy monsters are singing in the rain.'},
            {'role': 'system', 'name':'example_assistant', 'content': 'A cute baby monster with a red balloon.'},
            {'role': 'system', 'name':'example_assistant', 'content': 'A happy fluffy monster is watering a monstera plant.'},
            {'role': 'system', 'name':'example_assistant', 'content': 'A red happy fluffy monster is riding a cargo bike.'},
            {'role': 'system', 'name':'example_assistant', 'content': 'A happy fluffy monster is dancing on a rainbow.'},
            {'role': 'system', 'name':'example_assistant', 'content': 'Two happy fluffy monsters riding a tram.'}
        ]
        return self.__talk_to_chatGPT(messages)
    
class OpenAiWrapperMock:

    def __init__(self) -> None:
       logger.info("Initialized OpenAiWrapperMock")
       pass

    def create_images(self, input_prompt) -> list:
        return [
            {'url':'https://upload.wikimedia.org/wikipedia/commons/thumb/d/d4/Simple_Stick_Figure.svg/170px-Simple_Stick_Figure.svg.png'},
            {'url':'https://upload.wikimedia.org/wikipedia/commons/thumb/d/dd/Friendly_stickman.svg/400px-Friendly_stickman.svg.png'}
        ]

    def create_randomized_prompt(self) -> str:
        return 'Dev mode sample prompt.'