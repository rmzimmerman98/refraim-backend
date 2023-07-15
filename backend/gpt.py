import openai
from dotenv import load_dotenv
import os
load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY') 

class Gpt3:
    def __init__(self):
        self.openai = self.connect()
    def connect(self):
        openai.api_key = os.getenv('OPENAI_API_KEY')
        return openai
    def make_refraim(self, content):
        messages=[{
            'role': 'system',
            'content': 'I want you to help me reframe negative thoughts.'
            },
            {"role": "user", 
             "content" : "I'm not good enough"},
            {"role": "assistant", 
             "content" : "It appears that you might be experiencing the cognitive distortion known as 'all-or-nothing thinking' or 'black-and-white thinking.' \n This distortion involves seeing things in extremes, where you perceive yourself as either completely good or completely inadequate. \n Remember, it's important to challenge this distortion with more balanced thinking. \n Here are three positive reframes to consider: \n 1. I have unique strengths and qualities that make me valuable. \n 2. I am constantly growing and learning, and my worth is not defined by perfection. \n 3. I am deserving of love, acceptance, and compassion, just as I am."},
            {
            'role': 'user',
            'content': f'Content is : {content}'
            },
            {
            'role': 'user',
            'content': f'Take the {content} and identify a cognitive distortion that I might be suffering from. In a compassionate tone, state the cognitive distortion and explain it in simple terms in one sentence. Offer a one-sentence positive reframe.'
            }
            
        ]
        response = self.openai.ChatCompletion.create(
            model='gpt-3.5-turbo',
            messages=messages,
            temperature=0.3,
        )
        return response.choices[0]['message']['content']