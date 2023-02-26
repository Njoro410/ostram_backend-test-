from django.contrib.auth import authenticate
from django.conf import settings
from django.middleware import csrf
from rest_framework import exceptions as rest_exceptions, response, decorators as rest_decorators, permissions as rest_permissions
from rest_framework_simplejwt import tokens, views as jwt_views, serializers as jwt_serializers, exceptions as jwt_exceptions
from . import serializers, models
# Create your views here.

def get_user_tokens(user):
    refresh = tokens.RefreshToken.for_user(user)
    return {
        "refresh_token": str(refresh),
        "access_token": str(refresh.access_token)
    }
    

    

def loginView(request):
    serializer = serializers.loginSerializer(data=request.data)
    serializer.is_valid(raise_exceptions=True)
    
    email = serializer.validated_data['email']
    password = serializer.validated_data['password']
    
    user = authenticate(email=email, password=password)
    
    if user is not None:
        pass
    raise rest_exceptions.AuthenticationFailed("Email or Password is incorrect")
    