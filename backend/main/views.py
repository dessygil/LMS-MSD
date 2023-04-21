from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from rest_framework import viewsets, status
from rest_framework.request import Request
import os

from .models import Sample, Experiment, Machine
from .serializers import sample_serializer, experiment_serializer, machine_serializer

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

    def create(self, request: Request):
        pass

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
        machine = get_object_or_404(self.queryset, pk=pk)
        machine.delete()
        return JsonResponse(status=204)
    
    
