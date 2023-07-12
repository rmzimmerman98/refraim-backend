import openai
from dotenv import load_dotenv
import os
import asyncio
load_dotenv()

# OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
openai.api_key = os.getenv('OPENAI_API_KEY') 

# async def call_openai(messages, max_tokens, temperature):
#     response = await openai.ChatCompletion.create(
#         messages,
#         max_tokens,
#         temperature,
#         model = 'gpt-3.5-turbo-0301',
#     )
#     return response

# print(asyncio.run(call_openai('this is a test', 30, 0)))

# completion = openai.ChatCompletion.create(
#   model="gpt-3.5-turbo",
#   messages=[
#     {"role": "system", "content": "You are a helpful assistant."},
#     {"role": "user", "content": "Hello!"}
#   ]
# )


# # print(completion.choices[0].message)

# MODEL = "gpt-3.5-turbo"
# response = openai.ChatCompletion.create(
#     model=MODEL,
#     messages=[
#         {"role": "system", "content": "You are a helpful assistant."},
#         {"role": "user", "content": "Knock knock."},
#         {"role": "assistant", "content": "Who's there?"},
#         {"role": "user", "content": "Orange."},
#     ],
#     temperature=0,
# )

# print(response)

class Gpt3:
    def __init__(self):
        self.openai = self.connect()
    def connect(self):
        openai.organization = os.getenv('OPENAI_API_ORGA')
        openai.api_key = os.getenv('OPENAI_API_KEY')
        return openai
    def make_summary(self, content):
        messages=[{
            'role': 'system',
            'content': 'I want you to help me reframe negative thoughts.'
            },
            {
            'role': 'user',
            'content': f'Content is : {content}'
            },
            {
            'role': 'user',
            'content': 'Can you give me three one sentence positive reframes?'
            }
        ]
        response = self.openai.ChatCompletion.create(
            model='gpt-3.5-turbo',
            messages=messages,
            temperature=0.3,
        )
        return response.choices[0]['message']['content']
    

gpt3 = Gpt3()
summary = gpt3.make_summary("I enjoy traveling.")
print(summary)