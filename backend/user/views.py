from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser 
from rest_framework import status
from rest_framework.response import Response
import os

# Our code
from .models import User
from .serializers import UserSerializer

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

#TODO change the url so we do not need this 
def api_not_found(request):
    message = {"message": "No API found with those values."}
    return JsonResponse(message, status=404)

# test endpoints
def public(request):
    """No access token required to access this route
    """
    response = "Hello from a public endpoint! You don't need to be authenticated to see this."
    return JsonResponse(dict(message=response))


@require_auth(None)
def private(request):
    """A valid access token is required to access this route
    """
    response = "Hello from a private endpoint! You need to be authenticated to see this."
    return JsonResponse(dict(message=response))

@require_auth("read:messages")
def private_scoped(request):
    """A valid access token and an appropriate scope are required to access this route
    """
    response = "Hello from a private endpoint! You need to be authenticated and have a scope of read:messages to see this."
    return JsonResponse(dict(message=response))

# user endpoints
@api_view(['POST'])
@require_auth(None)
def check_or_create_user(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        email = serializer.validated_data.get('email')
        name = serializer.validated_data.get('name')

        try:
            user = User.objects.get(email=email)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            user = User.objects.create(name=name, email=email)

        serializer = UserSerializer(user)
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
