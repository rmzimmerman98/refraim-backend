import openai
from dotenv import load_dotenv
import os
load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY') 

class Gpt3:
    def __init__(self):
        self.openai = self.connect()
    def connect(self):
        openai.organization = os.getenv('OPENAI_API_ORGA')
        openai.api_key = os.getenv('OPENAI_API_KEY')
        return openai
    def make_refraim(self, content):
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