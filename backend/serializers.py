from .models import User
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password

class UserSerializer(serializers.ModelSerializer):
    class Meta():
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email']

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])

    class Meta():
        model = User
        fields = ['username','password', 'email', 'first_name', 'last_name']
    
    def validate(self, attributes):
        if User.objects.filter(email = attributes['email']).exists():
            raise serializers.ValidationError({ "email" : "Email already exists"})
        else:
            return attributes
    
    def create(self, data):
        user = User.objects.create(username=data["username"], email=data["email"], first_name=data["first_name"], last_name=data["last_name"])
        user.set_password(data["password"])
        user.save()
        return user 