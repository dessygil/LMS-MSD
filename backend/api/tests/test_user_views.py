import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
import http.client

import os
from dotenv import load_dotenv
load_dotenv()

def get_access_token():

    conn = http.client.HTTPSConnection("")
    payload = f"grant_type=client_credentials&client_id=%24%7Baccount.{os.getenv('AUTH0_CLIENT_ID')}%7D&client_secret={os.getenv('AUTH0_SECRET')}&audience={os.getenv('AUTH0_AUDIENCE')}"
    headers = { 'content-type': "application/json" }
    conn.request("POST", "https://dev-yisv67ey5uf648sg.us.auth0.com/oauth/token", payload, headers)

    res = conn.getresponse()
    data = res.read()
    print(res, data)
    return data.decode("utf-8")

@pytest.mark.django_db
def test_create_user_view():
    client = APIClient()
    url = reverse('create-user')
    data = {
        'email': 'testuser@example.com',
        'name': 'Test User'
    }

    # Test unauthenticated request
    #response = client.post(url, data)
    #assert response.status_code == status.HTTP_401_UNAUTHORIZED

    # Test authenticated request
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {get_access_token()}')
    response = client.post(url, data)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data['email'] == data['email']
    assert response.data['name'] == data['name']
