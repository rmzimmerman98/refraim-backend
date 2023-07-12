from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import User, Conversation
from .serializers import UserSerializer, RegisterSerializer, TokenSerializer, ConversationSerializer
from django.http import JsonResponse
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

gpt3 = Gpt3()

class Users(APIView):
    def get(self, requests, id):
        data = User.objects.filter(id=id) 
        serializer = UserSerializer(data, many=True)
        return JsonResponse(serializer.data, safe=False)
    
class Conversations(APIView):
    def get(self, requests, id):
        data = Conversation.objects.filter(user_id=id)
        serializer = ConversationSerializer(data, many=True)
        return JsonResponse(serializer.data, safe=False)
    
    def post(self, request, id):
        request.data['user'] = id
        request.data['refraim'] = gpt3.make_refraim(request.data['prompt'])
        serializer = ConversationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, safe=False)
        else:
            return JsonResponse(serializer.errors)
    
class TokenView(TokenObtainPairView):
    serializer_class = TokenSerializer

class RegisterView(APIView):
    def post(self,request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, safe=False)
        else:
            return JsonResponse(serializer.errors)