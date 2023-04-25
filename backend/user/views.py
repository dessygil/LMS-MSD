from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ( 
    CreateAPIView
)
import os

# Our code
from .models import User
from .serializers import CreateUserSerializer

# auth0 config for views
from authlib.integrations.django_oauth2 import ResourceProtector
from . import validator

from dotenv import load_dotenv
load_dotenv()

require_auth = ResourceProtector()
validator = validator.Auth0JWTBearerTokenValidator(
    os.getenv('JWT_ISSUER'),
    os.getenv('JWT_AUDIENCE')
)
require_auth.register_token_validator(validator)

class CreateUserView(CreateAPIView):
    serializer_class = CreateUserSerializer
    
    @require_auth(None) 
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        user, created = User.objects.get_or_create(email=validated_data['email'], defaults={'name': validated_data['name']})
        status_code = status.HTTP_201_CREATED if created else status.HTTP_200_OK
        return Response(serializer.validated_data, status=status_code)
