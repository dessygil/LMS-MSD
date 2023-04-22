from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from rest_framework import viewsets, status
from rest_framework.request import Request
from django.db import transaction
import os
from django.core.exceptions import ValidationError, ObjectDoesNotExist

from .models import Sample, Experiment, Machine, UserSampleConnector, MachineExperimentConnector
from .serializers import sample_serializer, experiment_serializer, machine_serializer, user_sample_connector_serializer, machine_experiment_connector_serializer

#TODO needs more error checking
#TODO needs more auth0

class SampleViewSet(viewsets.ViewSet):
    serializer = sample_serializer
    queryset = Sample.objects.all()
    
    def list(self, request: Request):
        """Get all samples
        Args:
            request: Get request
        """
        serializer = self.serializer(self.queryset, many=True)
        return JsonResponse(serializer.data, status=200)

    def create(self, request: Request, pk):
        serializer = self.serializer(data=request.data)
        if serializer.is_valid():
            name = serializer.validated_data.get('name')
            experiment = serializer.validated_data.get('experiment')
            machine = Sample(name=name, experiment=experiment)
            machine.save()
            return JsonResponse(serializer.validated_data, status=201)
        else:
            return JsonResponse(serializer.errors, status=400)

        

    def retrieve(self, request: Request, pk=None):
        """Retrieve a single sample
        Args:
            request: Get request
            pk: primary key of the sample
        """
        sample = get_object_or_404(self.queryset, pk=pk)
        serializer = self.serializer(sample)
        return JsonResponse(serializer.data, status=200)

    def update(self, request: Request, pk=None):
        pass

    def partial_update(self, request: Request, pk=None):
        pass

    def destroy(self, request: Request, pk=None):
        pass
    
    
class ExperimentViewSet(viewsets.ViewSet):
    serializer_class = experiment_serializer
    queryset = Experiment.objects.all()
    
    def list(self, request: Request):
        """Get all experiments
        Args:
            request: Get request
        """
        
        serializer = self.serializer(self.queryset, many=True)
        return JsonResponse(serializer.data, status=status.HTTP_200_OK)
    
    @transaction.atomic
    def create(self, request: Request):
        """Create a new experiment. The passed in machines should be an array. If it fails, since the
        database is set up to cascade the experiment through the machineExperimentConnector, only the
        experiment needs to be rolled back.
        Args:
            request: Post request
        """
        serializer = self.serializer(data=request.data)
        if serializer.is_valid():
            try:
                name = serializer.validated_data.get('name')
                experiment = Experiment(name=name)
                experiment.save()
                new_experiment_id = experiment.id

                # Use machine PK and create datasets within the experiMentmachineConnector
                machines = serializer.validated_data.get('machines', [])
                
                # Check all machines exist
                machine_ids = [machine for machine in machines if self.queryset.objects.filter(id=machine).exists()]
                if len(machine_ids) != len(machines):
                    return JsonResponse({"Error" : "One or more machines do not exist."} status=400)
                
                machine_experiment_connectors = [
                    MachineExperimentConnector(experiment_id=new_experiment_id, machine_id=machine)
                    for machine in machine_ids
                ]
                MachineExperimentConnector.objects.bulk_create(machine_experiment_connectors)
                
                # If experiment and all connectors are created, return the experiment
                return JsonResponse(serializer.validated_data, status=201)
            
            # If any of the above fails, roll back the experiment creation
            except ValidationError as e:
                raise ValidationError(str(e))
            except ObjectDoesNotExist as e:
                raise ObjectDoesNotExist(str(e))
        else:
            return JsonResponse(serializer.errors, status=400)
            

    def retrieve(self, request: Request, pk=None):
        """Retrieve a single experiment
        Args:
            request: Get request
            pk: primary key of the experiment
        """
        experiment = get_object_or_404(self.queryset, pk=pk)
        serializer = self.serializer(experiment)
        return JsonResponse(serializer.data, status=200)
        

    def update(self, request: Request, pk=None):
        pass

    def partial_update(self, request: Request, pk=None):
        pass

    def destroy(self, request: Request, pk=None):
        pass
    
    
class MachineViewSet(viewsets.ViewSet):
    queryset = Machine.objects.all()
    serializer = machine_serializer
    
    def list(self, request: Request):
        """Get all machines
        Args:
            request: Get request 
        """
        serializer = self.serializer(self.queryset, many=True)
        return JsonResponse(serializer.data, status=status.HTTP_200_OK)

    def create(self, request: Request):
        """Create a new machine
        Args:
            request: Post request
        """
        serializer = self.serializer(data=request.data)
        if serializer.is_valid():
            name = serializer.validated_data.get('name')
            time_takes = serializer.validated_data.get('time_takes')
            machine = Machine(name=name, time_takes=time_takes)
            machine.save()
            return JsonResponse(serializer.validated_data, status=201)
        else:
            return JsonResponse(serializer.errors, status=400)

    def retrieve(self, request: Request, pk=None):
        """Retrieve a single machine
        Args:
            request: Get request
            pk: primary key of the machine
        """
        machine = get_object_or_404(self.queryset, pk=pk)
        serializer = self.serializer(machine)
        return JsonResponse(serializer.data, status=200)

    def update(self, request: Request, pk=None):
        """Update a machine
        Args:
            request: Put request
            pk: primary key of the machine
        """
        experiment = get_object_or_404(self.queryset, pk=pk)
        serializer = self.serializer_class(experiment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=200)
        else:
            return JsonResponse(serializer.errors, status=400)

    def destroy(self, request: Request, pk=None):
        """Delete a machine
        Args:
            request: Delete request
            pk: primary key of the machine
        """
        machine = get_object_or_404(self.queryset, pk=pk)
        machine.delete()
        return JsonResponse(status=204)
    
class userSampleConnectorViewSet(viewsets.ViewSet):
    queryset = UserSampleConnector.objects.all()
    serializer = user_sample_connector_serializer
    
    def list(self, request: Request):
        """Get all userSampleConnectors
        Args:
            request: Get request 
        """
        serializer = self.serializer(self.queryset, many=True)
        return JsonResponse(serializer.data, status=status.HTTP_200_OK)

    def create(self, request: Request):
        """Create a new userSampleConnector. Will also create a new sample but needs extra
        information to do so (name, experiment)
        Args:
            request: Post request
        """
        serializer = self.serializer(data=request.data)
        if serializer.is_valid():
            user_id = serializer.validated_data.get('user_id')
            sample_id = serializer.validated_data.get('sample_id')
            
            # Create a new sample
            try:
                sample_viewset = SampleViewSet()
                sample_viewset.create(request)
            except:
                return JsonResponse(serializer.errors, status=500)
            
            # If the sample was created successfully, save the userSampleConnector
            userSampleConnector = UserSampleConnector(user_id=user_id, sample_id=sample_id)
            userSampleConnector.save()
            
            return JsonResponse(serializer.validated_data, status=201)
        else:
            return JsonResponse(serializer.errors, status=400)

    def retrieve(self, request: Request, pk=None):
        """Retrieve a single userSampleConnector
        Args:
            request: Get request
            pk: primary key of the userSampleConnector
        """
        userSampleConnector = get_object_or_404(self.queryset, pk=pk)
        serializer = self.serializer(userSampleConnector)
        return JsonResponse(serializer.data, status=200)

    def update(self, request: Request, pk=None):
        """Update a userSampleConnector
        Args:
            request: Put request
            pk: primary key of the userSampleConnector
        """
        userSampleConnector = get_object_or_404(self.queryset, pk=pk)
        serializer = self.serializer_class(userSampleConnector, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=200)
        else:
            return JsonResponse(serializer.errors, status=400)

    def destroy(self, request: Request, pk=None):
        """Delete a userSampleConnector
        Args:
            request: Delete request
            pk: primary key of the userSampleConnector
        """
        userSampleConnector = get_object_or_404(self.queryset, pk=pk)
        userSampleConnector.delete()
        return JsonResponse(status=204)
    
class MachineExperimentConnectorViewSet(viewsets.ViewSet):
    queryset = MachineExperimentConnector.objects.all()
    serializer = machine_experiment_connector_serializer
    
    def list(self, request: Request):
        """Get all machineExperimentConnectors
        Args:
            request: Get request 
        """
        serializer = self.serializer(self.queryset, many=True)
        return JsonResponse(serializer.data, status=status.HTTP_200_OK)

    def create(self, request: Request):
        """Create a new machineExperimentConnector
        Args:
            request: Post request
        """
        serializer = self.serializer(data=request.data)
        if serializer.is_valid():
            machine_id = serializer.validated_data.get('machine_id')
            experiment_id = serializer.validated_data.get('experiment_id')
            machineExperimentConnector = MachineExperimentConnector(machine_id=machine_id, experiment_id=experiment_id)
            machineExperimentConnector.save()
            return JsonResponse(serializer.validated_data, status=201)
        else:
            return JsonResponse(serializer.errors, status=400)

    def retrieve(self, request: Request, pk=None):
        """Retrieve a single machineExperimentConnector
        Args:
            request: Get request
            pk: primary key of the machineExperimentConnector
        """
        machineExperimentConnector = get_object_or_404(self.queryset, pk=pk)
        serializer = self.serializer(machineExperimentConnector)
        return JsonResponse(serializer.data, status=200)

    def update(self, request: Request, pk=None):
        """Update a machineExperimentConnector
        Args:
            request: Put request
            pk: primary key of the machineExperimentConnector
        """
        machineExperimentConnector = get_object_or_404(self.queryset, pk=pk)
        serializer = self.serializer_class(machineExperimentConnector, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=200)
        else:
            return JsonResponse(serializer.errors, status=400)

    def destroy(self, request: Request, pk=None):
        """Delete a machineExperimentConnector
        Args:
            request: Delete request
            pk: primary key of the machineExperimentConnector
        """
        machineExperimentConnector = get_object_or_404(self.queryset, pk=pk)
        machineExperimentConnector.delete()
        return JsonResponse(status=204)
    
    
    
