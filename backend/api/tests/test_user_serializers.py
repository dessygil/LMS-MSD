import pytest
from user.serializers import CreateUserSerializer, MainUserSerializer
from user.models import User


@pytest.fixture
def valid_user_data():
    return {
        "name": "Test User",
        "email": "test@example.com",
    }


@pytest.fixture
def invalid_user_data():
    return {
        "name": "",
        "email": "invalid-email",
    }


@pytest.mark.django_db
def test_create_user_serializer_valid_data(valid_user_data):
    serializer = CreateUserSerializer(data=valid_user_data)
    assert serializer.is_valid()


@pytest.mark.django_db
def test_create_user_serializer_invalid_data(invalid_user_data):
    serializer = CreateUserSerializer(data=invalid_user_data)
    assert serializer.is_valid() is False
    assert "name" in serializer.errors
    assert "email" in serializer.errors


@pytest.mark.django_db
def test_create_user_serializer_save(valid_user_data):
    serializer = CreateUserSerializer(data=valid_user_data)
    assert serializer.is_valid()
    user = serializer.save()
    assert User.objects.filter(email=valid_user_data["email"]).exists()
    assert user.name == valid_user_data["name"]


@pytest.mark.django_db
def test_main_user_serializer_to_representation(valid_user_data):
    user = User.objects.create(**valid_user_data)
    serializer = MainUserSerializer(instance=user)
    expected_data = {"email": user.email}
    assert serializer.data == expected_data
