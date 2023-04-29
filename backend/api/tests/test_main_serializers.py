import pytest
from django.utils import timezone
from rest_framework import serializers
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
def machine_two():
    machine_one = Machine.objects.create(name="Test Machine One", time_takes=120)
    machine_two = Machine.objects.create(name="Test Machine Two", time_takes=120)
    return [machine_one, machine_two]

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
def test_experiment_serializer_create_multiple_machines(user, machine_two):
    experiment_data = {
        "name": "Test Experiment",
        "machine_ids": [machine_two[0].id, machine_two[1].id],
    }
    serializer = ExperimentSerializer(data=experiment_data)
    serializer.is_valid(raise_exception=True)
    experiment = serializer.save()

    assert experiment.name == experiment_data["name"]
    assert MachineExperimentConnector.objects.all().count() == 2

@pytest.mark.django_db
def test_experiment_serializer_create_no_machine(user):
    experiment_data = {
        "name": "Test Experiment",
        "machine_ids": [],
    }
    serializer = ExperimentSerializer(data=experiment_data)
    with pytest.raises(serializers.ValidationError) as exc_info:
        serializer.is_valid(raise_exception=True)

@pytest.mark.django_db
def test_sample_serializer_create(experiment):
    user = User.objects.create(email='test@example.com', name='Test User')
    sample_data = {
        "name": "Test Sample",
        "experiment": experiment.id,
        "user": user.id,
    }
    serializer = SampleSerializer(data=sample_data)
    serializer.is_valid(raise_exception=True)
    sample = serializer.save()

    assert sample.name == sample_data["name"]
    assert sample.experiment == experiment
    assert sample.idle_time == 0

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
        "user": user.id,
        "sample": sample.id,
    }
    serializer = UserSampleConnectorSerializer(data=connector_data)
    serializer.is_valid(raise_exception=True)
    connector = serializer.save()

    assert connector.user == user
    assert connector.sample == sample
    
@pytest.mark.django_db
def test_experiment_serializer_update(experiment, machine):
    new_name = "Updated Experiment"
    experiment_data = {
        "name": new_name,
    }
    serializer = ExperimentSerializer(experiment, data=experiment_data, partial=True)
    serializer.is_valid(raise_exception=True)
    updated_experiment = serializer.save()

    assert updated_experiment.name == new_name
    assert updated_experiment.created_at == experiment.created_at

@pytest.mark.django_db
def test_sample_serializer_update(sample, experiment):
    new_name = "Updated Sample"
    new_idle_time = 100
    sample_data = {
        "name": new_name,
        "idle_time": new_idle_time,
    }
    serializer = SampleSerializer(sample, data=sample_data, partial=True)
    serializer.is_valid(raise_exception=True)
    updated_sample = serializer.save()

    assert updated_sample.name == new_name
    assert updated_sample.experiment == experiment
    assert updated_sample.idle_time == new_idle_time
    assert updated_sample.created_at == sample.created_at

@pytest.mark.django_db
def test_machine_serializer_update(machine):
    new_name = "Updated Machine"
    new_time_takes = 200
    machine_data = {
        "name": new_name,
        "time_takes": new_time_takes,
    }
    serializer = MachineSerializer(machine, data=machine_data, partial=True)
    serializer.is_valid(raise_exception=True)
    updated_machine = serializer.save()

    assert updated_machine.name == new_name
    assert updated_machine.time_takes == new_time_takes
    assert updated_machine.created_at == machine.created_at

@pytest.mark.django_db
def test_machine_experiment_connector_serializer_update(experiment, machine):
    new_experiment = Experiment.objects.create(name="New Experiment")
    new_machine = Machine.objects.create(name="New Machine", time_takes=100)
    connector = MachineExperimentConnector.objects.create(experiment=experiment, machine=machine)
    connector_data = {
        "experiment": new_experiment.id,
        "machine": new_machine.id,
    }
    serializer = MachineExperimentConnectorSerializer(connector, data=connector_data, partial=True)
    serializer.is_valid(raise_exception=True)
    updated_connector = serializer.save()

    assert updated_connector.experiment == new_experiment
    assert updated_connector.machine == new_machine
    assert updated_connector.created_at == connector.created_at

@pytest.mark.django_db
def test_user_sample_connector_serializer_update(user, sample):
    new_user = User.objects.create(email="new@example.com", name="newname")
    new_sample = Sample.objects.create(name="New Sample", experiment=sample.experiment)
    connector = UserSampleConnector.objects.create(user=user, sample=sample)
    connector_data = {
        "user": new_user.id,
        "sample": new_sample.id,
    }
    serializer = UserSampleConnectorSerializer(connector, data=connector_data, partial=True)
    serializer.is_valid(raise_exception=True)
    updated_connector = serializer.save()

    assert updated_connector.user == new_user
    assert updated_connector.sample == new_sample
    assert updated_connector.created_at == connector.created_at

@pytest.mark.django_db
def test_experiment_serializer_invalid_data(machine):
    invalid_experiment_data = {
        "name": "",
        "machine_ids": [machine.id],
    }
    serializer = ExperimentSerializer(data=invalid_experiment_data)
    with pytest.raises(ValidationError):
        serializer.is_valid(raise_exception=True)
        
@pytest.mark.django_db
def test_sample_serializer_invalid_data(user, experiment):
    invalid_sample_data = {
        "name": "",
        "experiment": experiment.id,
        "user": user.id,
    }
    serializer = SampleSerializer(data=invalid_sample_data)
    with pytest.raises(ValidationError):
        serializer.is_valid(raise_exception=True)

@pytest.mark.django_db
def test_machine_serializer_invalid_data():
    invalid_machine_data = {
        "name": "",
        "time_takes": -1,
    }
    serializer = MachineSerializer(data=invalid_machine_data)
    with pytest.raises(ValidationError):
        serializer.is_valid(raise_exception=True)

@pytest.mark.django_db
def test_machine_experiment_connector_serializer_invalid_data(experiment, machine):
    invalid_connector_data = {
        "experiment": 9999,
        "machine": machine.id,
    }
    serializer = MachineExperimentConnectorSerializer(data=invalid_connector_data)
    with pytest.raises(ValidationError):
        serializer.is_valid(raise_exception=True)

@pytest.mark.django_db
def test_user_sample_connector_serializer_invalid_data(user, sample):
    invalid_connector_data = {
        "user": "invalid-email",
        "sample": sample.id,
    }
    serializer = UserSampleConnectorSerializer(data=invalid_connector_data)
    with pytest.raises(ValidationError):
        serializer.is_valid(raise_exception=True)
