import pytest
from django.utils import timezone
from main.models import Experiment, Sample, Machine, MachineExperimentConnector, UserSampleConnector
from user.models import User
from main.serializers import SampleSerializer

@pytest.mark.django_db
def test_experiment_model():
    experiment = Experiment.objects.create(name="Test Experiment", created_at=timezone.now().date())
    assert experiment.name == "Test Experiment"

@pytest.mark.django_db
def test_sample_model():
    experiment = Experiment.objects.create(name="Test Experiment", created_at=timezone.now().date())
    sample = Sample.objects.create(name="Test Sample", experiment=experiment, created_at=timezone.now().date())
    assert sample.name == "Test Sample"

@pytest.mark.django_db
def test_machine_model():
    machine = Machine.objects.create(name="Test Machine", time_takes=120, created_at=timezone.now().date())
    assert machine.name == "Test Machine"

@pytest.mark.django_db
def test_machine_experiment_connector_model():
    experiment = Experiment.objects.create(name="Test Experiment", created_at=timezone.now().date())
    machine = Machine.objects.create(name="Test Machine", time_takes=120, created_at=timezone.now().date())
    connector = MachineExperimentConnector.objects.create(experiment=experiment, machine=machine, created_at=timezone.now().date())
    assert connector.experiment == experiment
    assert connector.machine == machine

@pytest.mark.django_db
def test_user_sample_connector_model():
    user = User.objects.create(email='testuser@gmail.com', name='testname')
    experiment = Experiment.objects.create(name="Test Experiment", created_at=timezone.now().date())
    sample = Sample.objects.create(name="Test Sample", experiment=experiment, created_at=timezone.now().date())
    user_sample_connector = UserSampleConnector.objects.create(user=user, sample=sample, created_at=timezone.now().date())
    assert user_sample_connector.user == user
    assert user_sample_connector.sample == sample
    assert UserSampleConnector.objects.all().count() == 1
    
@pytest.mark.django_db
def test_experiment_reverse_relationship():
    experiment = Experiment.objects.create(name="Test Experiment", created_at=timezone.now().date())
    sample = Sample.objects.create(name="Test Sample", experiment=experiment, created_at=timezone.now().date())
    assert sample.experiment == experiment

@pytest.mark.django_db
def test_user_reverse_relationship():
    user = User.objects.create(email='testuser@gmail.com', name='testname')
    experiment = Experiment.objects.create(name="Test Experiment", created_at=timezone.now().date())
    sample_data = {
            'name': 'Test Sample',
            'experiment': experiment.id,
            'user': user.email,
            'idle_time': 0,
            'created_at': timezone.now().date()
        }
    sample_serializer = SampleSerializer(data=sample_data)
    if sample_serializer.is_valid():
            sample_serializer.save()
            
    assert Experiment.objects.all().count() == 1
    assert Sample.objects.all().count() == 1
    assert UserSampleConnector.objects.all().count() == 1
    
@pytest.mark.django_db
def test_experiment_cascade_delete():
    experiment = Experiment.objects.create(name="Test Experiment", created_at=timezone.now().date())
    sample = Sample.objects.create(name="Test Sample", experiment=experiment, created_at=timezone.now().date())
    experiment.delete()
    assert Sample.objects.filter(id=sample.id).count() == 0

@pytest.mark.django_db
def test_user_cascade_delete():
    user = User.objects.create(email="testuser@gmail.com", name="testname")
    experiment = Experiment.objects.create(name="Test Experiment", created_at=timezone.now().date())
    sample = Sample.objects.create(name="Test Sample", experiment=experiment, created_at=timezone.now().date())
    user.delete()
    assert UserSampleConnector.objects.filter(user=user, sample=sample).count() == 0
    assert User.objects.all().count() == 0    
