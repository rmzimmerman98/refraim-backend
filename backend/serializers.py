from .models import User
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password

class UserSerializer(serializers.ModelSerializer):
    class Meta():
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email']

class RegisterSerializer(serializers.ModelSerializer):
    class Meta():
        model = User
        fields = ['username','password', 'email']
    
    def validate(self, attributes):
        if User.objects.filter(email = attributes['email']).exists():
            raise serializers.ValidationError({ "email" : "Email already exists"})
        else:
            return attributes
    
    def create(self, data):
        user = User.objects.create(username=data["username"], email=data["email"])
        user.set_password(data["password"])
        user.save()
        return user 