import pytest
from user.models import User

@pytest.mark.django_db
def test_create_user():
    user = User.objects.create(email='test@example.com', name='Test User')
    assert str(user.email) == 'test@example.com'
    assert str(user.name) == 'Test User'
    assert User.objects.count() == 1

def test_user_email_max_length():
    max_length = User._meta.get_field('email').max_length
    assert max_length == 255

def test_user_name_max_length():
    max_length = User._meta.get_field('name').max_length
    assert max_length == 255
