from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import User, Conversation
from .serializers import UserSerializer, RegisterSerializer, TokenSerializer, ConversationSerializer
from django.http import JsonResponse

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