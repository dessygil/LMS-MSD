from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from rest_framework import viewsets, status
from django.http import JsonResponse
import os
from main.models import (
    Experiment, 
    Sample, 
    Machine, 
)
from user.models import User
from .serializers import (
    ExperimentSerializer,
    SampleSerializer,
    MachineSerializer,
)


# Auth0 configuration
from authlib.integrations.django_oauth2 import ResourceProtector
from . import validator

from dotenv import load_dotenv
load_dotenv()

require_auth = ResourceProtector()
validator = validator.Auth0JWTBearerTokenValidator(
    os.getenv('JWT_ISSUER'),
    os.getenv('JWT_AUDIENCE')
)
require_auth.register_token_validator(validator)

class SampleViewSet(viewsets.ViewSet):
    serializer_class = SampleSerializer
    queryset = Sample.objects.all()
    
    def list(self, request):
        """Get all samples
        Args:
            request: Get request
        """
        serializer = self.serializer_class(self.queryset, many=True)
        return JsonResponse(serializer.data, status=200)

    def create(self, request, pk):
        """Create a new sample
        Args:
            request: Post request
            pk: primary key of the sample
        """
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        """Retrieve a single sample
        Args:
            request: Get request
            pk: primary key of the sample
        """
        try:
            sample = Sample.objects.get(pk=pk, experiment__user=request.user)
            serializer = SampleSerializer(sample)
            return JsonResponse(serializer.data, status=status.HTTP_200_OK)
        except Sample.DoesNotExist:
            return JsonResponse(status=status.HTTP_404_NOT_FOUND)

    def update(self, request, pk=None):
        """Update a single sample
        Args:
            request: Put request
            pk: primary key of the sample
        """
        try:
            sample = Sample.objects.get(pk=pk, experiment__user=request.user)
            serializer = SampleSerializer(sample, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse(serializer.data)
            return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Sample.DoesNotExist:
            return JsonResponse(status=status.HTTP_404_NOT_FOUND)


    def destroy(self, request, pk=None):
        """Delete a single sample
        Args:
            request: Delete request
            pk: primary key of the sample
        """
        sample = get_object_or_404(self.queryset, pk=pk)
        sample.delete()
        return JsonResponse({"message": "Sample deleted"}, status=204)
    
    
class ExperimentViewSet(viewsets.ViewSet):
    serializer_class = ExperimentSerializer
    queryset = Experiment.objects.all()
    
    def list(self, request):
        """Get all experiments
        Args:
            request: Get request
        """
        serializer = self.serializer_class(self.queryset, many=True)
        return JsonResponse(serializer.data, status=status.HTTP_200_OK)
    
    def create(self, request):
        """Create a new experiment. Machine_ids are to be included in the request body.
        and the serializer will create the MachineExperimentConnector objects.
        Args:
            request: Post request
        """
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
    def retrieve(self, request, pk=None):
        """Retrieve a single experiment
        Args:
            request: Get request
            pk: primary key of the experiment
        """
        experiment = get_object_or_404(self.queryset, pk=pk)
        serializer = self.serializer_class(experiment)
        return JsonResponse(serializer.data, status=200)
        
    def update(self, request, pk=None):
        """Update a single experiment
        Args:
            request: Put request
            pk: primary key of the experiment
        """
        experiment = get_object_or_404(self.queryset, pk=pk)
        serializer = self.serializer_class(experiment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
    def destroy(self, request, pk=None):
        """Delete a single experiment
        Args:
            request: Delete request
            pk: primary key of the experiment
        """
        experiment = get_object_or_404(self.queryset, pk=pk)
        experiment.delete()
        return JsonResponse({"message": "Experiment deleted"}, status=204)
    
    
class MachineViewSet(viewsets.ViewSet):
    queryset = Machine.objects.all()
    serializer_class = MachineSerializer
    
    def list(self, request):
        """Get all machines
        Args:
            request: Get request 
        """
        serializer = self.serializer_class(self.queryset, many=True)
        return JsonResponse(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        """Create a new machine
        Args:
            request: Post request
        """
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.validated_data, status=201)
        return JsonResponse(serializer.errors, status=400)

    def retrieve(self, request, pk=None):
        """Retrieve a single machine
        Args:
            request: Get request
            pk: primary key of the machine
        """
        machine = get_object_or_404(self.queryset, pk=pk)
        serializer = self.serializer_class(machine)
        return JsonResponse(serializer.data, status=200)

    def update(self, request, pk=None):
        """Update a machine
        Args:
            request: Put request
            pk: primary key of the machine
        """
        machine = get_object_or_404(self.queryset, pk=pk)
        serializer = self.serializer_class(machine, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=200)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        """Delete a machine
        Args:
            request: Delete request
            pk: primary key of the machine
        """
        machine = get_object_or_404(self.queryset, pk=pk)
        machine.delete()
        return JsonResponse(status=status.HTTP_204_NO_CONTENT)
