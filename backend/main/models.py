from django.db import models

"""
main.models is used for the gantt chart we are building to represent a laboratory schedule.
the connectors are meant to act as list to reference what machines are needed per experiment and 
what samples a user has.
"""

# Notes/Description will be needed
# Ways of tracking data will be needed

class Experiment(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255)
    created_at = models.DateField()

class Sample(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255)
    experiment = models.ForeignKey(Experiment, on_delete=models.CASCADE, related_name='samples')
    idle_time = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    created_at = models.DateField()

class Machine(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255)
    time_takes = models.DecimalField(max_digits=8, decimal_places=2)
    created_at = models.DateField()

class MachineExperimentConnector(models.Model):
    id = models.BigAutoField(primary_key=True)
    experiment = models.ForeignKey(Experiment, on_delete=models.CASCADE, related_name='machines')
    machine = models.ForeignKey(Machine, on_delete=models.CASCADE, related_name='experiments')
    created_at = models.DateField()

class UserSampleConnector(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey('user.User', on_delete=models.CASCADE, related_name='samples')
    sample = models.ForeignKey(Sample, on_delete=models.CASCADE, related_name='users')
    created_at = models.DateField()
