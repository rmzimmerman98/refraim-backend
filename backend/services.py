from django.conf import settings
from django.core.exceptions import ValidationError
from urllib.parse import urlencode
from django.shortcuts import redirect
import requests
import jwt
from .models import User
from .serializers import UserSerializer

GOOGLE_ACCESS_TOKEN_OBTAIN_URL = 'https://oauth2.googleapis.com/token'
GOOGLE_USER_INFO_URL = 'https://www.googleapis.com/oauth2/v3/userinfo'

def get_access_token(code, redirect_uri):
    data = {
        'code': code,
        'client_id': settings.GOOGLE_OAUTH2_CLIENT_ID,
        'client_secret': settings.GOOGLE_OAUTH2_CLIENT_SECRET,
        'redirect_uri': redirect_uri,
        'grant_type': 'authorization_code'
    }

    response = requests.post(GOOGLE_ACCESS_TOKEN_OBTAIN_URL, data=data)
    if not response.ok:
        raise ValidationError('Could not get access token from Google')
    
    access_token = response.json()['access_token']
    return access_token

def get_google_user_info(access_token):
    response = requests.get(
        GOOGLE_USER_INFO_URL,
        params={'access_token': access_token}
    )

    if not response.ok:
        raise ValidationError('Could not get user info from Google')
    
    return response.json()

def get_user(validated_data):
    domain = settings.BASE_API_URL
    redirect_uri = f'{domain}/googlelogin/'

    code = validated_data.get('code')
    error = validated_data.get('error')

    login_url = f'{settings.BASE_APP_URL}/login' # need to get main login url

    if error or not code:
        params = urlencode({'error': error})
        return redirect(f'{login_url}?{params}')
    
    access_token = get_access_token(code=code, redirect_uri=redirect_uri)
    user_data = get_google_user_info(access_token=access_token)

    return user_data


def createToken(email):
    data = User.objects.filter(email=email)
    user = UserSerializer(data, many=True)
    user_dict = dict(user.data[0])
    token = jwt.encode(user_dict, settings.SECRET_KEY, algorithm='HS256')
    return token