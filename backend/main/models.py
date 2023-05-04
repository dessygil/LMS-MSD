from django.db import models
from user.models import User
from django.utils import timezone

# TODO
# Notes/Description
# Ways of tracking data eg logs??
# created time and updated
# different types of users eg lab manager vs research scientist
# different labs biology vs chemistry vs materials focused
# make sure all naming conventions are followed for this project


class Experiment(models.Model):
    """An Experiment is referenced by the sample and is used by MachineExperimentConnector
    to reference what machines are needed per experiment.

    Fields:
        id: Primary key for the experiment
        name: Name of the experiment
        created_at: Date the experiment was created
    """

    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(default=timezone.now)

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
    """

    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True
    )
    experiment = models.ForeignKey(
        Experiment, on_delete=models.CASCADE, related_name="samples"
    )
    idle_time = models.DecimalField(
        max_digits=8, decimal_places=2, default=0
    )
    created_at = models.DateTimeField(
        default=timezone.now
    )

    def __str__(self):
        return self.name


class Machine(models.Model):
    """A machine is what the sample will be processed in.

    Fields:
        id: Primary key for the machine
        name: Name of the machine
        time_takes: Time it takes to run the machine in seconds
        created_at: Date the machine was created
    """

    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255)
    time_takes = models.DecimalField(max_digits=8, decimal_places=2)
    created_at = models.DateTimeField(default=timezone.now)

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
    """

    id = models.BigAutoField(primary_key=True)
    experiment = models.ForeignKey(
        Experiment, on_delete=models.CASCADE, related_name="machines"
    )
    machine = models.ForeignKey(
        Machine, on_delete=models.CASCADE, related_name="experiments"
    )
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.experiment.name + " " + self.machine.name


class UserSampleConnector(models.Model):
    """Connects the user to the sample. Each user will have multiple samples.

    Fields:
        id: Primary key for the connector
        user: Foreign key to the user
        sample: Foreign key to the sample
        created_at: Date the connector was created
    """

    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="samples"
    )
    sample = models.ForeignKey(
        Sample, on_delete=models.CASCADE, related_name="users"
    )
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return str(self.user) + " " + str(self.sample)
