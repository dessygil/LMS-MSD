from rest_framework import serializers
from .models import Sample, Experiment, Machine, UserSampleConnector, MachineExperimentConnector
from user.serializers import MainUserSerializer


#Change all serializers to Camelcase
class sample_serializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    
    name = serializers.CharField(required=True)
    experiment = serializers.CharField(required=True)
    idle_time = serializers.DecimalField(max_digits=8, decimal_places=2, default=0)
    class Meta:
        model = Sample
        fields = ['name', 'experiment', 'idle_time']
        
class experiment_serializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    
    name = serializers.CharField(required=True)
    class Meta:
        model = Experiment
        fields = ['name']

class machine_serializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    
    name = serializers.CharField(required=True)
    time_takes = serializers.DecimalField(max_digits=8, decimal_places=2)
    class Meta:
        model = Machine
        fields = ['name', 'time_takes']

class machine_experiment_connector_serializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    
    experiment = experiment_serializer(required=True)
    machine = machine_serializer(required=True)
    class Meta:
        model = MachineExperimentConnector
        fields = ['id', 'experiment', 'machine', 'created_at']

class user_sample_connector_serializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    
    user = MainUserSerializer(required=True)
    sample = sample_serializer(required=True)
    class Meta:
        model = UserSampleConnector
        fields = ['id', 'user', 'sample', 'created_at']
        
