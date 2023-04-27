from rest_framework import serializers
from django.utils import timezone
from main.models import Experiment, Sample, Machine, MachineExperimentConnector, UserSampleConnector
from user.models import User  

class ExperimentSerializer(serializers.ModelSerializer):
    """Serializer for the experiment object

    Fields:
        id: Primary key for the experiment
        name: Name of the experiment
        created_at: Date the experiment was created
        machine_ids: List of machine ids to be used in the experiment
    """
    machine_ids = serializers.ListField(
        child=serializers.IntegerField(),
        required=True,
        write_only=True
    )
    name = serializers.CharField(max_length=255, required=True)
    class Meta:
        model = Experiment
        fields = ['id', 'name', 'created_at']
        
    def create(self, validated_data):
        machine_ids = validated_data.pop('machine_ids', [])
        experiment = Experiment.objects.create(**validated_data)
        
        for machine_id in machine_ids:
            machine = Machine.objects.get(pk=machine_id)
            MachineExperimentConnector.objects.create(experiment=experiment, machine=machine)

        return experiment

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.created_at = validated_data.get('created_at', instance.created_at)
        instance.save()
        return instance

class SampleSerializer(serializers.ModelSerializer):
    """serializer for the sample object

    Fields:
        id: Primary key for the sample
        name: Name of the sample
        experiment: Foreign key to the experiment
        idle_time: Time the sample is idle in seconds
        created_at: Date the sample was created
    """
    experiment = serializers.PrimaryKeyRelatedField(queryset=Experiment.objects.all(), required=True)
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=True)
    name = serializers.CharField(max_length=255, required=True)
    idle_time = serializers.IntegerField(required=True)
    
    class Meta:
        model = Sample
        fields = ['id', 'name', 'experiment', 'idle_time', 'created_at', 'user']

    def create(self, validated_data):
        experiment = validated_data.pop('experiment')
        user = validated_data.pop('user')
        sample = Sample.objects.create(experiment=experiment, **validated_data)

        user_sample_connector_data = {
            'user': user.email,
            'sample': sample.id,
            'created_at': timezone.now().date(),
        } 
        user_sample_connector_serializer = UserSampleConnectorSerializer(data=user_sample_connector_data)
        if user_sample_connector_serializer.is_valid():
            user_sample_connector_serializer.save()
        else:
            print(user_sample_connector_serializer.errors)

        return sample

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.experiment = validated_data.get('experiment', instance.experiment)
        instance.idle_time = validated_data.get('idle_time', instance.idle_time)
        instance.created_at = validated_data.get('created_at', instance.created_at)
        instance.save()
        return instance
        
class MachineSerializer(serializers.ModelSerializer):
    """Serializer for the machine object
    
    Fields:
        id: Primary key for the machine
        name: Name of the machine
        time_takes: Time it takes to run the machine in seconds
        created_at: Date the machine was created
    """
    class Meta:
        model = Machine
        fields = ['id', 'name', 'time_takes', 'created_at']
    
    def create(self, validated_data):
        return Machine.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.time_takes = validated_data.get('time_takes', instance.time_takes)
        instance.created_at = validated_data.get('created_at', instance.created_at)
        instance.save()
        return instance

class MachineExperimentConnectorSerializer(serializers.ModelSerializer):
    """Serializer for the machine experiment connector object

    Fields:
        id: Primary key for the machine experiment connector
        experiment: Foreign key to the experiment
        machine: Foreign key to the machine
        created_at: Date the machine experiment connector was created
    """
    experiment = serializers.PrimaryKeyRelatedField(queryset=Experiment.objects.all())
    machine = serializers.PrimaryKeyRelatedField(queryset=Machine.objects.all())

    class Meta:
        model = MachineExperimentConnector
        fields = ['id', 'experiment', 'machine', 'created_at']

    def create(self, validated_data):
        return MachineExperimentConnector.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.experiment = validated_data.get('experiment', instance.experiment)
        instance.machine = validated_data.get('machine', instance.machine)
        instance.created_at = validated_data.get('created_at', instance.created_at)
        instance.save()
        return instance

class UserSampleConnectorSerializer(serializers.ModelSerializer):
    """Serializer for the user sample connector object

    Fields:
        id: Primary key for the user sample connector
        user: Foreign key to the user
        sample: Foreign key to the sample
        created_at: Date the user sample connector was created
    """
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=True)
    sample = serializers.PrimaryKeyRelatedField(queryset=Sample.objects.all(), required=True)

    class Meta:
        model = UserSampleConnector
        fields = ['id', 'user', 'sample', 'created_at']

    def create(self, validated_data):
        return UserSampleConnector.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.user = validated_data.get('user', instance.user)
        instance.sample = validated_data.get('sample', instance.sample)
        instance.created_at = validated_data.get('created_at', instance.created_at)
        instance.save()
        return instance
        
