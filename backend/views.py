from django.shortcuts import render
from rest_framework.views import APIView
from .models import User
from .serializers import UserSerializer
from django.http import JsonResponse

class Users(APIView):
    def get(self, requests):
        data = User.objects.all() 
        serializer = UserSerializer(data, many=True)
        return JsonResponse(serializer.data, safe=False)