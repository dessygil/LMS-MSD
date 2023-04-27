import pytest
from django.utils import timezone
from rest_framework.exceptions import ValidationError
from main.models import Experiment, Sample, Machine, MachineExperimentConnector, UserSampleConnector
from user.models import User
from main.serializers import (
    ExperimentSerializer,
    SampleSerializer,
    MachineSerializer,
    MachineExperimentConnectorSerializer,
    UserSampleConnectorSerializer,
)

@pytest.fixture
def user():
    return User.objects.create(email="test@example.com", name="testname")

@pytest.fixture
def experiment():
    return Experiment.objects.create(name="Test Experiment")

@pytest.fixture
def machine():
    return Machine.objects.create(name="Test Machine", time_takes=120)

@pytest.fixture
def sample(experiment, user):
    return Sample.objects.create(name="Test Sample", experiment=experiment)

@pytest.mark.django_db
def test_experiment_serializer_create(user, machine):
    experiment_data = {
        "name": "Test Experiment",
        "machine_ids": [machine.id],
    }
    serializer = ExperimentSerializer(data=experiment_data)
    serializer.is_valid(raise_exception=True)
    experiment = serializer.save()

    assert experiment.name == experiment_data["name"]
    assert MachineExperimentConnector.objects.filter(experiment=experiment, machine=machine).exists()

@pytest.mark.django_db
def test_sample_serializer_create(user, experiment):
    sample_data = {
        "name": "Test Sample",
        "experiment": experiment.id,
        "user": user.email,
    }
    serializer = SampleSerializer(data=sample_data)
    serializer.is_valid(raise_exception=True)
    sample = serializer.save()

    assert sample.name == sample_data["name"]
    assert sample.experiment == experiment
    assert sample.idle_time == 0
    assert UserSampleConnector.objects.all().count() == 1

@pytest.mark.django_db
def test_machine_serializer_create():
    machine_data = {
        "name": "Test Machine",
        "time_takes": 120,
    }
    serializer = MachineSerializer(data=machine_data)
    serializer.is_valid(raise_exception=True)
    machine = serializer.save()

    assert machine.name == machine_data["name"]
    assert machine.time_takes == machine_data["time_takes"]

@pytest.mark.django_db
def test_machine_experiment_connector_serializer_create(experiment, machine):
    connector_data = {
        "experiment": experiment.id,
        "machine": machine.id,
    }
    serializer = MachineExperimentConnectorSerializer(data=connector_data)
    serializer.is_valid(raise_exception=True)
    connector = serializer.save()

    assert connector.experiment == experiment
    assert connector.machine == machine

@pytest.mark.django_db
def test_user_sample_connector_serializer_create(user, sample):
    connector_data = {
        "user": user.email,
        "sample": sample.id,
    }
    serializer = UserSampleConnectorSerializer(data=connector_data)
    serializer.is_valid(raise_exception=True)
    connector = serializer.save()

    assert connector.user == user
    assert connector.sample == sample
