from rest_framework import serializers
from .models import Sample, Experiment, Machine, UserSampleConnector, MachineExperimentConnector


class sample_serializer(serializers.Serializer):
    name = serializers.CharField(required=True)
    experiment = serializers.CharField(required=True)
    idle_time = serializers.DecimalField(max_digits=8, decimal_places=2, default=0)
    class Meta:
        model = Sample
        fields = ['name', 'experiment', 'idle_time']
        
class experiment_serializer(serializers.Serializer):
    name = serializers.CharField(required=True)
    class Meta:
        model = Experiment
        fields = ['name']

class machine_serializer(serializers.Serializer):
    name = serializers.CharField(required=True)
    time_takes = serializers.DecimalField(max_digits=8, decimal_places=2)
    class Meta:
        model = Machine
        fields = ['name', 'time_takes']

class machine_experiment_connector_serializer(serializers.Serializer):
    experiment = ExperimentSerializer(required=True)
    machine = MachineSerializer(required=True)
    class Meta:
        model = MachineExperimentConnector
        fields = ['id', 'experiment', 'machine', 'created_at']

class user_sample_connector_serializer(serializers.Serializer):
    user = UserSerializer(required=True)
    sample = SampleSerializer(required=True)
    class Meta:
        model = UserSampleConnector
        fields = ['id', 'user', 'sample', 'created_at']
        
