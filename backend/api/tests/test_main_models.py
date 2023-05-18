import pytest
from django.utils import timezone
from main.models import (
    Experiment,
    Sample,
    Machine,
    MachineExperimentConnector,
)
from user.models import User


@pytest.mark.django_db
def test_experiment_model():
    experiment = Experiment.objects.create(
        name="Test Experiment", created_at=timezone.now(), notes="Test Notes",
    )
    assert experiment.name == "Test Experiment"
    assert experiment.notes == "Test Notes"


@pytest.mark.django_db
def test_sample_model():
    experiment = Experiment.objects.create(
        name="Test Experiment", notes="test notes", 
        created_at=timezone.now()
    )
    sample = Sample.objects.create(
        name="Test Sample", experiment=experiment, idle_time=4, 
        notes="test notes", created_at=timezone.now()
    )
    assert sample.name == "Test Sample"


@pytest.mark.django_db
def test_machine_model():
    machine = Machine.objects.create(
        name="Test Machine", model_number="3232", machine_type="test machine",
        manufacturer="test manufacturer", notes="test notes",
        created_at=timezone.now()
    )
    assert machine.name == "Test Machine"
    assert machine.model_number == "3232"
    assert machine.machine_type == "test machine"
    assert machine.manufacturer == "test manufacturer"
    assert machine.notes == "test notes"


@pytest.mark.django_db
def test_machine_experiment_connector_model():
    experiment = Experiment.objects.create(
        name="Test Experiment", notes="test notes", 
        created_at=timezone.now()
    )
    machine = Machine.objects.create(
        name="Test Machine", model_number="3232", machine_type="test machine",
        manufacturer="test manufacturer", notes="test notes",
        created_at=timezone.now()
    )
    connector = MachineExperimentConnector.objects.create(
        experiment=experiment, machine=machine, duration=10, 
        created_at=timezone.now()
    )
    assert connector.experiment == experiment
    assert connector.machine == machine
    assert connector.duration == 10


@pytest.mark.django_db
def test_experiment_reverse_relationship():
    experiment = Experiment.objects.create(
        name="Test Experiment", notes="test notes", 
        created_at=timezone.now()
    )
    sample = Sample.objects.create(
        name="Test Sample", experiment=experiment, idle_time=4, 
        notes="test notes", created_at=timezone.now()
    )
    assert sample.experiment == experiment
    assert sample.name == "Test Sample"
    assert sample.idle_time == 4

@pytest.mark.django_db
def test_experiment_cascade_delete():
    experiment = Experiment.objects.create(
        name="Test Experiment", notes="test notes", 
        created_at=timezone.now()
    )
    sample = Sample.objects.create(
        name="Test Sample", experiment=experiment, idle_time=4, 
        notes="test notes", created_at=timezone.now()
    )
    experiment.delete()
    assert Sample.objects.filter(id=sample.id).count() == 0


@pytest.mark.django_db
def test_user_cascade_delete():
    user = User.objects.create(email="testuser@gmail.com", name="testname")
    experiment = Experiment.objects.create(
        name="Test Experiment", notes="test notes", 
        created_at=timezone.now()
    )
    sample = Sample.objects.create(
        name="Test Sample", experiment=experiment, idle_time=4, 
        notes="test notes", created_at=timezone.now()
    )
    user.delete()
    assert User.objects.all().count() == 0
