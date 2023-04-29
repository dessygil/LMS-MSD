import pytest

import json
import requests
import os
from rest_framework import status
from rest_framework.test import APIClient
from django.urls import reverse
from django.utils import timezone
from main.models import (
    Sample,
    Machine,
    Experiment,
)
from user.models import User as lmsUser
from main.serializers import (
    SampleSerializer,
    ExperimentSerializer,
    MachineSerializer,
)


from dotenv import load_dotenv
load_dotenv()

@pytest.fixture(scope='module')
def auth_token():
    
    url = 'https://dev-yisv67ey5uf648sg.us.auth0.com/oauth/token'
    headers = {'content-type': 'application/json'}
    data = {
        'client_id': os.getenv('AUTH0_CLIENT_ID'),
        'client_secret': os.getenv('AUTH0_SECRET'),
        'audience': os.getenv('AUTH0_AUDIENCE'),
        'grant_type': 'client_credentials',
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    response_data = response.json()
    access_token = response_data.get('access_token')
    yield access_token 

@pytest.mark.django_db
def test_list_samples(auth_token, client):
    user = lmsUser.objects.create(email='testuser@gmail.com', name='testuser')
    assert lmsUser.objects.all().count() == 1
    experiment = Experiment.objects.create(name='Test Experiment')
    sample_data = {
        "name": "Test Sample",
        "experiment": experiment.id,
        "user": user.id,
    }
    serializer = SampleSerializer(data=sample_data)
    serializer.is_valid(raise_exception=True)
    sample = serializer.save()
    
    headers = {'Authorization': f'Bearer {auth_token}'}
    url = reverse('sample-list')
    response = client.get(url, headers=headers)
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_create_sample(auth_token, client):
    user = lmsUser.objects.create(email='testuser@gmail.com', name='testuser')
    experiment = Experiment.objects.create(name='Test Experiment')
    headers = {'Authorization': f'Bearer {auth_token}'}

    url = reverse('sample-create')
    data = {
        'name': 'Sample 2',
        'experiment': experiment.id,
        'user': user.id
    }
    
    response = client.post(url, headers=headers, data=data)
    assert response.status_code == status.HTTP_201_CREATED

@pytest.mark.django_db
def test_retrieve_sample(auth_token, client):
    user = lmsUser.objects.create(email='testuser@gmail.com', name='testuser')
    machine = Machine.objects.create(name='Test Machine', time_takes=10)
    experiment = Experiment.objects.create(name='Test Experiment')
    sample_data = {
        "name": "Test Sample",
        "experiment": experiment.id,
        "user": user.id,
    }
    serializer = SampleSerializer(data=sample_data)
    serializer.is_valid(raise_exception=True)
    sample = serializer.save()
    
    headers = {'Authorization': f'Bearer {auth_token}'}
    url = reverse('sample-retrieve', args=[sample.id])
    response = client.get(url, headers=headers)
    assert response.status_code == status.HTTP_200_OK

@pytest.mark.django_db
def test_update_sample(auth_token, client):
    user = lmsUser.objects.create(email='testuser@gmail.com', name='testuser')
    experiment = Experiment.objects.create(name='Test Experiment')
    sample_data = {
        "name": "Test Sample",
        "experiment": experiment.id,
        "user": user.id,
    }
    serializer = SampleSerializer(data=sample_data)
    serializer.is_valid(raise_exception=True)
    sample = serializer.save()
    
    headers = {'Authorization': f'Bearer {auth_token}'}
    url = reverse('sample-update', args=[sample.id])
    data = {
        'name': 'Updated Sample',
        'experiment': experiment.id,
        'idle_time': 10,
        'created_at': timezone.now().date(),
    }
    response = client.put(url, headers=headers, data=data)
    assert response.status_code == status.HTTP_200_OK

@pytest.mark.django_db
def test_destroy_sample(auth_token, client):
    experiment = Experiment.objects.create(name='Test Experiment')
    sample = Sample.objects.create(experiment=experiment, name='Test Sample')
    headers = {'Authorization': f'Bearer {auth_token}'}
    url = reverse('sample-destroy', args=[sample.id])
    
    response = client.delete(url, headers=headers)
    assert response.status_code == status.HTTP_204_NO_CONTENT
