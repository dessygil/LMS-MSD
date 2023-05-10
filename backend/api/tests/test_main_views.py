import pytest
import json
import requests
import os
from rest_framework import status
from rest_framework.test import APIClient
from django.urls import reverse
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
def test_list_samples(auth_token, client):
    user = lmsUser.objects.create(email="testuser@gmail.com", name="testuser")
    assert lmsUser.objects.all().count() == 1
    experiment = Experiment.objects.create(name="Test Experiment")
    sample_data = {
        "name": "Test Sample",
        "experiment": experiment.id,
        "user": user.id,
    }
    serializer = SampleSerializer(data=sample_data)
    serializer.is_valid(raise_exception=True)
    sample = serializer.save()

    headers = {"Authorization": f"Bearer {auth_token}"}
    url = reverse("sample-list")
    response = client.get(url, headers=headers)
    assert response.status_code == status.HTTP_200_OK


"""
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
"""


@pytest.mark.django_db
def test_destroy_sample(auth_token, client):
    experiment = Experiment.objects.create(name="Test Experiment")
    sample = Sample.objects.create(experiment=experiment, name="Test Sample")
    headers = {"Authorization": f"Bearer {auth_token}"}
    url = reverse("sample-destroy", args=[sample.id])

    response = client.delete(url, headers=headers)
    assert response.status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.django_db
def test_list_experiments():
    api_client = APIClient()

    machine = Machine.objects.create(name="Machine 1", time_takes=10)
    experiment_data = {
        "name": "Experiment 1",
        "machine_ids": [machine.id],
    }
    experiment = ExperimentSerializer(data=experiment_data)
    experiment.is_valid(raise_exception=True)
    experiment.save()

    url = reverse("experiment-list")
    response = api_client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_create_experiment():
    api_client = APIClient()

    machine = Machine.objects.create(name="Machine 1", time_takes=10)

    url = reverse("experiment-create")
    data = {"name": "New Experiment", "machine_ids": [machine.id]}
    response = api_client.post(url, data)
    assert response.status_code == 201


@pytest.mark.django_db
def test_retrieve_experiment():
    api_client = APIClient()

    machine = Machine.objects.create(name="Machine 1", time_takes=10)
    experiment_data = {
        "name": "Experiment 1",
        "machine_ids": [machine.id],
    }
    experiment = ExperimentSerializer(data=experiment_data)
    experiment.is_valid(raise_exception=True)
    experiment.save()
    experiment_id = experiment.data.get("id")

    url = reverse("experiment-retrieve", kwargs={"pk": experiment_id})
    response = api_client.get(url)

    assert response.status_code == 200


@pytest.mark.django_db
def test_update_experiment():
    api_client = APIClient()

    machine = Machine.objects.create(name="Machine 1", time_takes=10)
    machine_two = Machine.objects.create(name="Machine 2", time_takes=10)
    experiment_data = {
        "name": "Experiment 1",
        "machine_ids": [machine.id],
    }
    experiment = ExperimentSerializer(data=experiment_data)
    experiment.is_valid(raise_exception=True)
    experiment.save()
    experiment_id = experiment.data.get("id")

    url = reverse("experiment-update", kwargs={"pk": experiment_id})
    data = {"name": "Updated Experiment", "machine_ids": [machine_two.id]}
    response = api_client.put(url, data)

    assert response.status_code == 200


@pytest.mark.django_db
def test_destroy_experiment():
    api_client = APIClient()

    machine = Machine.objects.create(name="Machine 1", time_takes=10)
    experiment_data = {
        "name": "Experiment 1",
        "machine_ids": [machine.id],
    }
    experiment = ExperimentSerializer(data=experiment_data)
    experiment.is_valid(raise_exception=True)
    experiment.save()
    experiment_id = experiment.data.get("id")

    url = reverse("experiment-destroy", kwargs={"pk": experiment_id})
    response = api_client.delete(url)
    assert Experiment.objects.all().count() == 0
    assert response.status_code == 204


@pytest.mark.django_db
def test_list_machines():
    api_client = APIClient()

    machine = Machine.objects.create(name="Machine1", time_takes=10)
    url = reverse("machine-list")
    response = api_client.get(url)
    assert response.status_code == 200
    machines = Machine.objects.all()
    assert response.json() == MachineSerializer(machines, many=True).data


@pytest.mark.django_db
def test_create_machine():
    api_client = APIClient()

    data = {
        "name": "Machine1",
        "time_takes": 10,
        "manufacturer": "Test Manufacturer",
        "model_number": "Test Model Number",
    }
    url = reverse("machine-create")
    response = api_client.post(url, data)
    assert response.status_code == 201
    machine = Machine.objects.last()
    if machine is None:
        pytest.fail("No Machine objects found in the database")
    assert machine.name == data["name"]
    assert machine.time_takes == data["time_takes"]


@pytest.mark.django_db
def test_retrieve_machine():
    api_client = APIClient()

    machine = Machine.objects.create(name="Machine1", time_takes=10)
    url = reverse("machine-retrieve", kwargs={"pk": machine.id})
    response = api_client.get(url)
    assert response.status_code == 200
    assert response.json() == MachineSerializer(machine).data


@pytest.mark.django_db
def test_update_machine():
    api_client = APIClient()

    data = {
        "name": "Machine1",
        "time_takes": 10,
        "manufacturer": "Test Manufacturer",
        "model_number": "Test Model Number",
    }

    machine = Machine.objects.create(**data)

    updated_data = {
        "name": "UpdatedMachine",
        "time_takes": 15,
        "manufacturer": "Test Manufacturer",
        "model_number": "Test Model Number",
    }
    url = reverse("machine-update", kwargs={"pk": machine.id})
    response = api_client.put(url, updated_data)
    assert response.status_code == 200


@pytest.mark.django_db
def test_destroy_machine():
    api_client = APIClient()

    machine = Machine.objects.create(name="Machine1", time_takes=10)
    url = reverse("machine-destroy", kwargs={"pk": machine.id})
    response = api_client.delete(url)
    assert response.status_code == 204
    assert not Machine.objects.filter(id=machine.id).exists()
