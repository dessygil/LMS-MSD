import pytest
import json
import requests
from django.urls import reverse
import os

from dotenv import load_dotenv

load_dotenv()


@pytest.fixture(scope="module")
def auth_token():

    url = "https://dev-yisv67ey5uf648sg.us.auth0.com/oauth/token"
    headers = {"content-type": "application/json"}
    data = {
        "client_id": os.getenv("AUTH0_CLIENT_ID"),
        "client_secret": os.getenv("AUTH0_SECRET"),
        "audience": os.getenv("AUTH0_AUDIENCE"),
        "grant_type": "client_credentials",
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    response_data = response.json()
    access_token = response_data.get("access_token")
    yield access_token


@pytest.mark.django_db
def test_create_user_view(auth_token, client):
    url = reverse("create_user")
    headers = {"Authorization": f"Bearer {auth_token}"}
    data = {"email": "test@example.com", "name": "Test User"}
    response = client.post(url, headers=headers, data=data)
    assert response.status_code == 201
