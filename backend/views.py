from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User, Conversation
from .services import get_user, createToken
from .serializers import UserSerializer, RegisterSerializer, TokenSerializer, ConversationSerializer, GoogleAuthSerializer
from django.http import JsonResponse
from django.shortcuts import redirect
from django.conf import settings
from .gpt import Gpt3
from rest_framework.permissions import AllowAny


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
        request.data['conclusion'] = Gpt3().make_conclusion(request.data['prompt'], request.data['refraim'])
        serializer = ConversationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, safe=False)
        else:
            return JsonResponse(serializer.errors)
        
class ConversationShow(APIView):
    def get(self, request, id):
        data = Conversation.objects.filter(id=id)
        serializer = ConversationSerializer(data, many=True)
        return JsonResponse(serializer.data, safe=False)
    
    def put(self, request, id):
        data = Conversation.objects.get(id=id)
        if 'conclusion' in request.data and request.data['conclusion'] == 'resubmit':
            request.data['refraim'] = Gpt3().make_accurate(request.data['prompt'], request.data['refraim'])
            request.data['conclusion'] = Gpt3().make_conclusion(request.data['prompt'], request.data['refraim'])
        if 'is_favorite' in request.data:
         data.is_favorite = request.data['is_favorite']  # Update is_favorite field of conversation instance
         data.save()

        serializer = ConversationSerializer(data, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, safe=False)
        else:
            return JsonResponse(serializer.errors)
        
    def delete(self, request, id):
        data = Conversation.objects.get(id=id)
        data.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

        
class Favorites(APIView):
    def get(self, request, id):
        data = Conversation.objects.filter(is_favorite=True)
        serializer = ConversationSerializer(data, many=True)
        return JsonResponse(serializer.data, safe=False)
        
class GoogleLoginView(APIView):
    def get(self, request):
        serializer = GoogleAuthSerializer(data=request.GET)
        serializer.is_valid(raise_exception=True)
        user_data = get_user(serializer.validated_data)

        if User.objects.filter(email = user_data['email']).exists():
            token = createToken(email=user_data['email'])
            response = redirect(f'{settings.BASE_APP_URL}/pre-prompt')
            response.set_cookie('access_token', token, max_age=60 * 24 * 60 * 60)
            return response

        # Needs logic if user doesn't have existing refraim account
    
class TokenView(TokenObtainPairView):
    serializer_class = TokenSerializer

class RegisterView(APIView):
    def post(self,request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': {
                    'username': user.username,
                    'email': user.email,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                }, 
            }, status=status.HTTP_201_CREATED)  # Here we specify the status code)
        else:
            return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)