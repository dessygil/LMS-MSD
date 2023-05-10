from rest_framework import serializers
import datetime
from main.models import (
    Experiment,
    Sample,
    Machine,
    MachineExperimentConnector,
)
from user.models import User


class ExperimentSerializer(serializers.ModelSerializer):
    """Serializer for the experiment object

    Fields:
        id: Primary key for the experiment
        name: Name of the experiment
        machine_ids: List of machine ids to be used in the experiment
        notes: Notes about the experiment
    """

    machine_ids = serializers.ListField(
        child=serializers.IntegerField(), required=True, write_only=True
    )
    name = serializers.CharField(max_length=255, required=True)
    notes = serializers.CharField(max_length=255, allow_blank=True, required=False)

    class Meta:
        model = Experiment
        fields = ["id", "name", "created_at", "machine_ids", "notes"]

    def validate_machine_ids(self, value):
        if len(value) == 0:
            raise serializers.ValidationError(
                "You must provide at least one machine id"
            )
        return value

    def create(self, validated_data):
        machine_ids = validated_data.pop("machine_ids", [])

        if len(machine_ids) == 0:
            raise serializers.ValidationError(
                "You must provide at least one machine id"
            )

        experiment = Experiment.objects.create(**validated_data)

        for machine_id in machine_ids:
            machine = Machine.objects.get(pk=machine_id)
            MachineExperimentConnector.objects.create(
                experiment=experiment, machine=machine
            )

        return experiment

    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)
        instance.updated_at = datetime.datetime.now()
        instance.notes = validated_data.get("notes", instance.notes)
        instance.save()
        return instance


class SampleSerializer(serializers.ModelSerializer):
    """serializer for the sample object

    Fields:
        id: Primary key for the sample
        name: Name of the sample
        user: Foreign key to the user
        experiment: Foreign key to the experiment
        idle_time: Time the sample is idle in seconds
        notes: Notes about the sample
    """

    experiment = serializers.PrimaryKeyRelatedField(
        queryset=Experiment.objects.all(), required=True
    )
    user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), required=True
    )
    name = serializers.CharField(max_length=255, required=True)
    idle_time = serializers.IntegerField(required=False)
    notes = serializers.CharField(max_length=255, allow_blank=True, required=False)

    class Meta:
        model = Sample
        fields = ["id", "name", "experiment", "user", "idle_time", "notes"]

    def create(self, validated_data):
        experiment = validated_data.pop("experiment")
        user = validated_data.pop("user")
        sample = Sample.objects.create(
            experiment=experiment, user=user, **validated_data
        )
        return sample

    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)
        instance.experiment = validated_data.get("experiment", instance.experiment)
        instance.idle_time = validated_data.get("idle_time", instance.idle_time)
        instance.updated_at = datetime.datetime.now()
        instance.notes = validated_data.get("notes", instance.notes)
        instance.save()
        return instance


class MachineSerializer(serializers.ModelSerializer):
    """Serializer for the machine object

    Fields:
        id: Primary key for the machine
        name: Name of the machine
        time_takes: Time it takes to run the machine in seconds
        model_number: Foreign key to the model
        manufacturer: Foreign key to the manufacturer
        notes: Notes about the machine
    """

    name = serializers.CharField(max_length=255, required=True)
    time_takes = serializers.IntegerField(required=True)
    model_number = serializers.CharField(max_length=255, required=True)
    manufacturer = serializers.CharField(max_length=255, required=True)
    notes = serializers.CharField(max_length=255, allow_blank=True, required=False)

    class Meta:
        model = Machine
        fields = ["id", "name", "time_takes", "model_number", "manufacturer", "notes"]

    def create(self, validated_data):
        return Machine.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)
        instance.time_takes = validated_data.get("time_takes", instance.time_takes)
        instance.updated_at = datetime.datetime.now()
        instance.model_number = validated_data.get(
            "model_number", instance.model_number
        )
        instance.manufacturer = validated_data.get(
            "manufacturer", instance.manufacturer
        )
        instance.notes = validated_data.get("notes", instance.notes)
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
        fields = ["id", "experiment", "machine"]

    def create(self, validated_data):
        return MachineExperimentConnector.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.experiment = validated_data.get("experiment", instance.experiment)
        instance.machine = validated_data.get("machine", instance.machine)
        instance.updated_at = datetime.datetime.now()
        instance.save()
        return instance
