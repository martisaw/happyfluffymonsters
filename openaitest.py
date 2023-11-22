import openai
import logging

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


openai.api_key = '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'


messages=[
    {'role': 'system', 'content': 'You are a helpful assistant.'},
    {'role': 'user', 'content': f'Imagine today it\'s 2018-07-31, you are in Germany and a \'happy fluffy monster\' is another term for human. What is a happy fluffy monster typically doing in this country on that date? Answer in one sentence. Do not mention the date. Do not mention Germany. Only tell what is happening. Focus on only one activity. Take this as examples: "Two happy fluffy monsters are singing in the rain" or "A cute baby monster with a red balloon" or "A happy fluffy monster is watering a monstera plant".'}
]
messages=[
    {'role': 'system', 'content': 'You are a helpful assistant.'},
    {'role': 'user', 'content': f'Imagine today it\'s 2018-07-31, you are in Germany and a \'happy fluffy monster\' is another term for human. What is a happy fluffy monster typically doing in this country on that date? Answer in one sentence. Do not mention the date. Do not mention Germany. Only tell what is happening. Focus on only one activity.'},
    {'role': 'system', 'name':'example_assistant', 'content': 'Two happy fluffy monsters are singing in the rain.'},
    {'role': 'system', 'name':'example_assistant', 'content': 'A cute baby monster with a red balloon.'},
    {'role': 'system', 'name':'example_assistant', 'content': 'A happy fluffy monster is watering a monstera plant.'},
    {'role': 'system', 'name':'example_assistant', 'content': 'A red happy fluffy monster is riding a cargo bike.'},
    {'role': 'system', 'name':'example_assistant', 'content': 'A happy fluffy monster is dancing on a rainbow.'},
    {'role': 'system', 'name':'example_assistant', 'content': 'Two happy fluffy monsters riding a tram.'}
]

messages=[
    {'role': 'system', 'content': 'You are a helpful assistant.'},
    {'role': 'user', 'content': f'Imagine today it\'s 2018-07-31, you are in Germany and a \'happy fluffy monster\' is another term for human. What is a happy fluffy monster typically doing in this country on that date? Only tell what is happening. Focus on only one activity.'},
    {'role': 'system', 'name':'example_assistant', 'content': 'Two happy fluffy monsters are singing in the rain.'},
    {'role': 'system', 'name':'example_assistant', 'content': 'A cute baby monster with a red balloon.'},
    {'role': 'system', 'name':'example_assistant', 'content': 'A happy fluffy monster is watering a monstera plant.'},
    {'role': 'system', 'name':'example_assistant', 'content': 'A red happy fluffy monster is riding a cargo bike.'},
    {'role': 'system', 'name':'example_assistant', 'content': 'A happy fluffy monster is dancing on a rainbow.'},
    {'role': 'system', 'name':'example_assistant', 'content': 'Two happy fluffy monsters riding a tram.'},
    {'role': 'system', 'content': 'Answer in one sentence. Do not mention the date. Do not mention Germany.'},
]

messages=[
    {'role': 'system', 'content': 'You are a helpful assistant.'},
    {'role': 'system', 'content': 'Answer in one sentence. Do not mention the date. Do not mention Germany.'},
    {'role': 'user', 'content': f'Imagine today it\'s 2018-07-31, you are in Spain and a \'happy fluffy monster\' is another term for human. What is a happy fluffy monster typically doing in this country on that date?'},
    {'role': 'user', 'content': 'Only tell what is happening. Focus on only one activity.'},
    {'role': 'system', 'name':'example_assistant', 'content': 'Two happy fluffy monsters are singing in the rain.'},
    {'role': 'system', 'name':'example_assistant', 'content': 'A cute baby monster with a red balloon.'},
    {'role': 'system', 'name':'example_assistant', 'content': 'A happy fluffy monster is watering a monstera plant.'},
    {'role': 'system', 'name':'example_assistant', 'content': 'A red happy fluffy monster is riding a cargo bike.'},
    {'role': 'system', 'name':'example_assistant', 'content': 'A happy fluffy monster is dancing on a rainbow.'},
    {'role': 'system', 'name':'example_assistant', 'content': 'Two happy fluffy monsters riding a tram.'}
]

def chatgpt(model, messages):
    
    return openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=1.0
    ).choices[0].message.content

print(chatgpt('gpt-3.5-turbo', messages))
# print(chatgpt('gpt-4', messages))