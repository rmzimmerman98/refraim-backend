from .models import User, Conversation
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.password_validation import validate_password

class UserSerializer(serializers.ModelSerializer):
    class Meta():
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email']

class ConversationSerializer(serializers.ModelSerializer):
    class Meta():
        model = Conversation
        fields = "__all__"

class TokenSerializer(TokenObtainPairSerializer):
    def get_token(self, user):
        token = super().get_token(user)
        token['username'] = user.username
        return token
    
class GoogleAuthSerializer(serializers.Serializer):
    code = serializers.CharField(required=False)
    error = serializers.CharField(required=False)

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