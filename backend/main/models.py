from django.db import models
from user.models import User
from django.utils import timezone

# TODO
# Ways of tracking data eg logs??
# different labs biology vs chemistry vs materials focused
# make sure all naming conventions are followed for this project
# time_takes should be called duration
# the duration should be variable for the machine based on the experiment


class Experiment(models.Model):
    """An Experiment is referenced by the sample and is used by MachineExperimentConnector
    to reference what machines are needed per experiment.

    Fields:
        id: Primary key for the experiment
        name: Name of the experiment
        notes: Notes about the experiment
        created_at: Date the experiment was created
        updated_at: Date the experiment was last updated
    """

    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255)
    notes = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name


class Sample(models.Model):
    """A sample is the ultimate

    Fields:
        id: Primary key for the sample
        name: Name of the sample
        experiment: Foreign key to the experiment
        idle_time: Time the sample is idle in seconds
        created_at: Date the sample was created
        updated_at: Date the sample was last updated
    """

    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    experiment = models.ForeignKey(
        Experiment, on_delete=models.CASCADE, related_name="samples"
    )
    idle_time = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    notes = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name


class Machine(models.Model):
    """A machine is what the sample will be processed in.

    Fields:
        id: Primary key for the machine
        name: Name of the machine
        time_takes: Time it takes to run the machine in seconds
        created_at: Date the machine was created
        updated_at: Date the machine was last updated
    """

    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255)
    model_number = models.CharField(max_length=255, default="Unknown")
    manufacturer = models.CharField(max_length=255, default="Unknown")
    time_takes = models.DecimalField(max_digits=8, decimal_places=2)
    notes = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name


class MachineExperimentConnector(models.Model):
    """This acts as a list to reference what machines are needed
    per experiment. Each experiment will reference multiple machines

    Fields:
        id: Primary key for the connector
        experiment: Foreign key to the experiment
        machine: Foreign key to the machine
        created_at: Date the connector was created
        updated_at: Date the connector was last updated
    """

    id = models.BigAutoField(primary_key=True)
    experiment = models.ForeignKey(
        Experiment, on_delete=models.CASCADE, related_name="machines"
    )
    machine = models.ForeignKey(
        Machine, on_delete=models.CASCADE, related_name="experiments"
    )
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.experiment.name + " " + self.machine.name
