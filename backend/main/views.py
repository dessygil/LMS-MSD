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
    serializer_class = sample_serializer
    
    
    def list(self, request: Request):
        """Get all samples
        Args:
            request: Get request
        """
        queryset = Sample.objects.all()
        serializer = sample_serializer(queryset, many=True)
        return JsonResponse(serializer.data, status=200)

    def create(self, request: Request, pk):
        pass

    def retrieve(self, request: Request, pk=None):
        """Retrieve a single sample
        Args:
            request: Get request
            pk: primary key of the sample
        """
        queryset = Sample.objects.all()
        sample = get_object_or_404(queryset, pk=pk)
        serializer = sample_serializer(sample)
        return JsonResponse(serializer.data, status=200)

    def update(self, request: Request, pk=None):
        p

    def partial_update(self, request: Request, pk=None):
        pass

    def destroy(self, request: Request, pk=None):
        pass
    
    
class ExperimentViewSet(viewsets.ViewSet):
    serializer_class = experiment_serializer
    
    
    def list(self, request: Request):
        """Get all experiments
        Args:
            request: Get request
        """
        queryset = Experiment.objects.all()
        serializer = experiment_serializer(queryset, many=True)
        return JsonResponse(serializer.data, status=status.HTTP_200_OK)

    def create(self, request: Request):
        pass

    def retrieve(self, request: Request, pk=None):
        """Retrieve a single experiment
        Args:
            request: Get request
            pk: primary key of the experiment
        """
        queryset = Experiment.objects.all()
        experiment = get_object_or_404(queryset, pk=pk)
        serializer = experiment_serializer(experiment)
        return JsonResponse(serializer.data, status=200)
        

    def update(self, request: Request, pk=None):
        pass

    def partial_update(self, request: Request, pk=None):
        pass

    def destroy(self, request: Request, pk=None):
        pass
    
    
class MachineViewSet(viewsets.ViewSet):
    
    def list(self, request: Request):
        """Get all machines
        Args:
            request: Get request 
        """
        queryset = Machine.objects.all()
        serializer = machine_serializer(queryset, many=True)
        return JsonResponse(serializer.data, status=status.HTTP_200_OK)

    def create(self, request: Request):
        pass

    def retrieve(self, request: Request, pk=None):
        """Retrieve a single machine
        Args:
            request: Get request
            pk: primary key of the machine
        """
        queryset = Machine.objects.all()
        machine = get_object_or_404(queryset, pk=pk)
        serializer = machine_serializer(machine)
        return JsonResponse(serializer.data, status=200)

    def update(self, request: Request, pk=None):
        pass

    def partial_update(self, request: Request, pk=None):
        pass

    def destroy(self, request: Request, pk=None):
        pass
    
    
