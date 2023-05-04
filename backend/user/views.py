from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework import status

import os

from .models import User
from .serializers import CreateUserSerializer

# auth0 config for views
from authlib.integrations.django_oauth2 import ResourceProtector
from . import validator

from dotenv import load_dotenv

load_dotenv()

require_auth = ResourceProtector()
validator = validator.Auth0JWTBearerTokenValidator(
    os.getenv("JWT_ISSUER"), os.getenv("JWT_AUDIENCE")
)
require_auth.register_token_validator(validator)


@api_view(["POST"])
@require_auth(None)
def create_user_view(request, *args, **kwargs):
    print(request.data, "You have reached the create_user_view")
    serializer = CreateUserSerializer(data=request.data)
    try:
        serializer.is_valid(raise_exception=True)
    except ValidationError as e:
        return Response(
            {"error": "create_user_view " + str(e)}, status=status.HTTP_400_BAD_REQUEST
        )
    email = serializer.validated_data.get("email")
    name = serializer.validated_data.get("name")

    if User.objects.filter(email=email).exists():
        return Response({"Success": "User already exists"}, status=status.HTTP_200_OK)
    User.objects.create(email=email, name=name)
    return Response({"success": "User created"}, status=status.HTTP_201_CREATED)
