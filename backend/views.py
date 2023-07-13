from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import User, Conversation
from .serializers import UserSerializer, RegisterSerializer, TokenSerializer, ConversationSerializer, GoogleAuthSerializer
from django.http import JsonResponse
from .gpt import Gpt3

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
        request.data['refraim'] = Gpt3().make_refraim(request.data['prompt'])
        serializer = ConversationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, safe=False)
        else:
            return JsonResponse(serializer.errors)
        
class GoogleLoginView(APIView):
    def get(self, request):
        serializer = GoogleAuthSerializer(data=request.GET)
        serializer.is_valid(raise_exception=True)
        print(serializer.validated_data)
        return JsonResponse(serializer.validated_data, safe=False)
    
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