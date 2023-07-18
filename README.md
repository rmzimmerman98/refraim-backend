# Refraim - [Live Site](https://refraim.netlify.app/)

A mental health app that reframes your negative thoughts. Our goal is to help users with a simple tool powered by OpenAI, to identify their negative thought-patterns and move towards healthier self-awareness and self-talk.

### Backend
This is the backend API Repository for Refraim. It utilizes Django's REST Framework to create endpoints that serves our PostgreSQL Database. 

#### Endpoints
```user/:id/``` - Passing a user ID will return that users profile data<br />
```register/``` - An endpoint to create a new user into the database<br />
```token/``` - Passing login information will create a token for the user to be authenticated<br />
```allconversations/:id/``` - Passing a user ID will return all conversations for that user<br />
```allconversations/:id/favorites/``` - Passing a user ID will return all favorited conversations for that user<br />
```conversation/:id/``` - This is a full CRUD route for conversations by passing a conversation ID<br />
```googlelogin/``` - This route recieves a Google Account's Access token, to authenticate a user with Google credentials.

### OpenAI

To create _Refraims_ for users, calls to OpenAI API with specific prompts are made. Using ```allconversations/:id/``` as a POST route and passing a new prompt will make the OpenAI call. Here is an example of the Class used to make a call to OpenAI in order for our backend to make _Refraims_. 

```Python
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
        messages=[# Messages to send to OpenAI API]
        response = self.openai.ChatCompletion.create(
            model='gpt-3.5-turbo',
            messages=messages,
            temperature=0.3,
        )
        return response.choices[0]['message']['content']
```
And here is the data that this backend will return when a prompt is given in the response.

<img width="723" alt="Screen Shot 2023-07-15 at 12 31 42 PM" src="https://github.com/rmzimmerman98/refraim-backend/assets/107363999/6dc30f8b-1351-40f4-81bc-e204d9255580">

