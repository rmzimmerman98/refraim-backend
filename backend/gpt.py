import openai
from dotenv import load_dotenv
import os
load_dotenv()

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
             "content" : "I'm feeling misunderstood in my friendship with Bob. He always cancels on me when we make plans. Maybe I should just let go of him as a friend."},
            {"role": "assistant", 
             "content" : "I understand that you're feeling misunderstood in your friendship with Bob, and it seems like you're experiencing a cognitive distortion called 'all-or-nothing thinking.' By believing that Bob always cancels on you when you make plans, you're perceiving the situation in extreme terms without considering any exceptions or other factors that could be contributing to his cancellations. It might be helpful to have an open conversation with Bob about your feelings to gain a better understanding of what's going on and explore possible solutions together."},
            {
            'role': 'user',
            'content': f'Content is : {content}'
            },
            {
            'role': 'user',
            'content': f'Take the {content} and relate with the emotions and feelings that the user might have. In a compassionate tone, summarize the negative thoughts and explain it to to the user in a human way in one-two sentences while also concluding with a one or two sentence positive reframe. Provide this information in a human way.'
            }
            
        ]
        response = self.openai.ChatCompletion.create(
            model='gpt-3.5-turbo',
            messages=messages,
            temperature=0.3,
        )
        return response.choices[0]['message']['content']