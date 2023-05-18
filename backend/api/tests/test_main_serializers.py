import pytest
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from main.models import (
    Experiment,
    Sample,
    Machine,
    MachineExperimentConnector,
)
from user.models import User
from main.serializers import (
    ExperimentSerializer,
    SampleSerializer,
    MachineSerializer,
    MachineExperimentConnectorSerializer,
)


@pytest.fixture
def user():
    return User.objects.create(email="test@example.com", name="testname")


@pytest.fixture
def experiment():
    return Experiment.objects.create(
        name="Test Experiment", notes="test notes",
    )


@pytest.fixture
def machine():
    return Machine.objects.create(
        name="Test Machine",
        machine_type="Test Machine",
        model_number="Test Model",
        manufacturer="Test Manufacturer",
        notes="Test Notes",
    )


@pytest.fixture
def machine_two():
    machine_one = Machine.objects.create(
        name="Test Machine One",
        machine_type="Test Machine",
        model_number="Test Model",
        manufacturer="Test Manufacturer",
        notes="Test Notes",
    )
    machine_two = Machine.objects.create(
        name="Test Machine Two",
        machine_type="Test Machine",
        model_number="Test Model",
        manufacturer="Test Manufacturer",
        notes="Test Notes", 
    )
    return [machine_one, machine_two]


@pytest.fixture
def sample(experiment, user):
    return Sample.objects.create(name="Test Sample", experiment=experiment, user=user)


@pytest.mark.django_db
def test_experiment_serializer_create(user, machine):
    experiment_data = {
        "name": "Test Experiment",
        "machine_ids": [machine.id],
        "durations": [10],
    }
    serializer = ExperimentSerializer(data=experiment_data)
    serializer.is_valid(raise_exception=True)
    experiment = serializer.save()

    assert experiment.name == experiment_data["name"]
    assert MachineExperimentConnector.objects.filter(
        experiment=experiment, machine=machine
    ).exists()


@pytest.mark.django_db
def test_experiment_serializer_create_multiple_machines(user, machine_two):
    experiment_data = {
        "name": "Test Experiment",
        "machine_ids": [machine_two[0].id, machine_two[1].id],
        "durations": [10, 20],
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
        "durations": [],
    }
    serializer = ExperimentSerializer(data=experiment_data)
    with pytest.raises(serializers.ValidationError):
        serializer.is_valid(raise_exception=True)


@pytest.mark.django_db
def test_sample_serializer_create(experiment):
    user = User.objects.create(email="test@example.com", name="Test User")
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
        "model_number": "Test Model",
        "manufacturer": "Test Manufacturer",
        "machine_type": "Test Machine",
        "notes": "Test Notes",
    }
    serializer = MachineSerializer(data=machine_data)
    serializer.is_valid(raise_exception=True)
    machine = serializer.save()

    assert machine.name == machine_data["name"]
    assert machine.model_number == machine_data["model_number"]
    assert machine.manufacturer == machine_data["manufacturer"]
    assert machine.machine_type == machine_data["machine_type"]
    assert machine.notes == machine_data["notes"]


@pytest.mark.django_db
def test_machine_experiment_connector_serializer_create(experiment, machine):
    connector_data = {
        "experiment": experiment.id,
        "machine": machine.id,
        "duration": 10,
    }
    serializer = MachineExperimentConnectorSerializer(data=connector_data)
    serializer.is_valid(raise_exception=True)
    connector = serializer.save()

    assert connector.experiment == experiment
    assert connector.machine == machine
    assert connector.duration == connector_data["duration"]


@pytest.mark.django_db
def test_experiment_serializer_update(experiment, machine):
    experiment_data = {
        "name": "Updated Experiment",
    }
    serializer = ExperimentSerializer(experiment, data=experiment_data, partial=True)
    serializer.is_valid(raise_exception=True)
    updated_experiment = serializer.save()

    assert updated_experiment.name == experiment_data["name"]
    assert updated_experiment.created_at == experiment.created_at


@pytest.mark.django_db
def test_sample_serializer_update(sample, experiment):
    sample_data = {
        "name": "Updated Sample",
        "idle_time": 100,
    }
    serializer = SampleSerializer(sample, data=sample_data, partial=True)
    serializer.is_valid(raise_exception=True)
    updated_sample = serializer.save()

    assert updated_sample.name == sample_data["name"]
    assert updated_sample.experiment == experiment
    assert updated_sample.idle_time == sample_data["idle_time"]
    assert updated_sample.created_at == sample.created_at


@pytest.mark.django_db
def test_machine_serializer_update(machine):
    machine_data = {
        "name": "Updated Machine",
        "machine_type": "Updated Machine",
        "model_number": "Updated Model",
        "manufacturer": "Updated Manufacturer",
        "notes": "Updated Notes",
    }
    serializer = MachineSerializer(machine, data=machine_data, partial=True)
    serializer.is_valid(raise_exception=True)
    updated_machine = serializer.save()

    assert updated_machine.name == machine_data["name"]
    assert updated_machine.machine_type == machine_data["machine_type"]
    assert updated_machine.model_number == machine_data["model_number"]
    assert updated_machine.manufacturer == machine_data["manufacturer"]
    assert updated_machine.notes == machine_data["notes"]


@pytest.mark.django_db
def test_machine_experiment_connector_serializer_update(experiment, machine):
    new_experiment = Experiment.objects.create(name="New Experiment")
    new_machine = Machine.objects.create(name="New Machine")
    connector = MachineExperimentConnector.objects.create(
        experiment=experiment, machine=machine
    )
    connector_data = {
        "experiment": new_experiment.id,
        "machine": new_machine.id,
    }
    serializer = MachineExperimentConnectorSerializer(
        connector, data=connector_data, partial=True
    )
    serializer.is_valid(raise_exception=True)
    updated_connector = serializer.save()

    assert updated_connector.experiment == new_experiment
    assert updated_connector.machine == new_machine
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
        "duration": -1,
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
