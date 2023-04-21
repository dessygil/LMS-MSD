from rest_framework import serializers
from .models import Sample, Experiment, Machine


class sample_serializer(serializers.Serializer):
    class Meta:
        model = Sample
        fields = ['name', 'description', 'experiment', 'machine']
        
class experiment_serializer(serializers.Serializer):
    class Meta:
        model = Experiment
        fields = ['name', 'description', 'machine']

class machine_serializer(serializers.Serializer):
    class Meta:
        model = Machine
        fields = ['name', 'description']
