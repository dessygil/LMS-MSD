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
        name="Test Experiment", created_at=timezone.now()
    )
    assert experiment.name == "Test Experiment"


@pytest.mark.django_db
def test_sample_model():
    experiment = Experiment.objects.create(
        name="Test Experiment", created_at=timezone.now()
    )
    sample = Sample.objects.create(
        name="Test Sample", experiment=experiment, created_at=timezone.now()
    )
    assert sample.name == "Test Sample"


@pytest.mark.django_db
def test_machine_model():
    machine = Machine.objects.create(
        name="Test Machine", duration=120, created_at=timezone.now()
    )
    assert machine.name == "Test Machine"


@pytest.mark.django_db
def test_machine_experiment_connector_model():
    experiment = Experiment.objects.create(
        name="Test Experiment", created_at=timezone.now()
    )
    machine = Machine.objects.create(
        name="Test Machine", duration=120, created_at=timezone.now()
    )
    connector = MachineExperimentConnector.objects.create(
        experiment=experiment, machine=machine, created_at=timezone.now()
    )
    assert connector.experiment == experiment
    assert connector.machine == machine


@pytest.mark.django_db
def test_experiment_reverse_relationship():
    experiment = Experiment.objects.create(
        name="Test Experiment", created_at=timezone.now()
    )
    sample = Sample.objects.create(
        name="Test Sample", experiment=experiment, created_at=timezone.now()
    )
    assert sample.experiment == experiment


@pytest.mark.django_db
def test_experiment_cascade_delete():
    experiment = Experiment.objects.create(
        name="Test Experiment", created_at=timezone.now()
    )
    sample = Sample.objects.create(
        name="Test Sample", experiment=experiment, created_at=timezone.now()
    )
    experiment.delete()
    assert Sample.objects.filter(id=sample.id).count() == 0


@pytest.mark.django_db
def test_user_cascade_delete():
    user = User.objects.create(email="testuser@gmail.com", name="testname")
    experiment = Experiment.objects.create(
        name="Test Experiment", created_at=timezone.now()
    )
    sample = Sample.objects.create(
        name="Test Sample", experiment=experiment, created_at=timezone.now()
    )
    user.delete()
    assert User.objects.all().count() == 0
