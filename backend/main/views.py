from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view
import os
from main.models import (
    Experiment,
    Sample,
    Machine,
)
from .serializers import (
    ExperimentSerializer,
    SampleSerializer,
    MachineSerializer,
)

# TODO
# We are going to want add only the ability for the lab manager to create new machines
# and new experiments. This can be done through auth0 using @require_auth(<permission>)

# Auth0 configuration
from authlib.integrations.django_oauth2 import ResourceProtector
from . import validator

from dotenv import load_dotenv

load_dotenv()

require_auth = ResourceProtector()
validator = validator.Auth0JWTBearerTokenValidator(
    os.getenv("JWT_ISSUER"), os.getenv("JWT_AUDIENCE")
)
require_auth.register_token_validator(validator)


@api_view(["GET"])
def test_endpoint(request):
    return JsonResponse({"message": "Hello World!"})


@api_view(["GET"])
@require_auth(None)
def list_samples(request):
    """List all samples for the current user"""
    queryset = Sample.objects.all()
    serializer = SampleSerializer(queryset, many=True)
    return JsonResponse(serializer.data, safe=False, status=status.HTTP_200_OK)


@api_view(["POST"])
@require_auth(None)
def create_sample(request):
    """Create a new sample

    Required fields:
        id: Primary key for the sample
        name: Name of the sample
        user: Foreign key to the user
        experiment: Foreign key to the experiment
        idle_time: Time the sample is idle in seconds
        created_at: Date the sample was created
    """
    serializer = SampleSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user=request.user)
        return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
    return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
@require_auth(None)
def retrieve_sample(request, pk=None):
    """retrieve a sample by id

    Required fields:
        id: Primary key for the sample
    """
    try:
        sample = Sample.objects.get(pk=pk, experiment__user=request.user)
        serializer = SampleSerializer(sample)
        return JsonResponse(serializer.data, status=status.HTTP_200_OK)
    except Sample.DoesNotExist:
        return JsonResponse(serializer.errors,
                            status=status.HTTP_404_NOT_FOUND)


@api_view(["PUT"])
@require_auth(None)
def update_sample(request, pk=None):
    """Update a sample using the id

    Required fields:
        id: Primary key for the sample
        name: Name of the sample
        idle_time: Time the sample is idle in seconds
        experiment: Foreign key to the experiment
    """
    try:
        sample = Sample.objects.get(pk=pk, experiment__user=request.user)
        serializer = SampleSerializer(sample, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors,
                            status=status.http_400_bad_request)
    except Sample.DoesNotExist:
        return JsonResponse(serializer.errors,
                            status=status.http_404_not_found)


@api_view(["DELETE"])
@require_auth(None)
def destroy_sample(request, pk=None):
    """Delete a sample using the id

    Required fields:
        id: Primary key for the sample
    """
    queryset = Sample.objects.all()
    sample = get_object_or_404(queryset, pk=pk)
    sample.delete()
    return JsonResponse({"message": "Sample deleted"},
                        status=status.HTTP_204_NO_CONTENT)


# TODO
# add back auth0


@api_view(["GET"])
def list_experiments(request):
    """List all experiments"""
    queryset = Experiment.objects.all()
    serializer = ExperimentSerializer(queryset, many=True)
    return JsonResponse(serializer.data, safe=False, status=status.HTTP_200_OK)


@api_view(["POST"])
def create_experiment(request):
    """Create a new experiment

    Args:
        id: Primary key for the experiment
        name: Name of the experiment
        created_at: Date the experiment was created
        machine_ids: List of machine ids to be used in the experiment
    """
    serializer = ExperimentSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
    return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def retrieve_experiment(request, pk=None):
    """Retrieve an experiment by id

    Args:
        id: Primary key for the experiment
    """
    queryset = Experiment.objects.all()
    experiment = get_object_or_404(queryset, pk=pk)
    serializer = ExperimentSerializer(experiment)
    return JsonResponse(serializer.data, status=status.HTTP_200_OK)


@api_view(["PUT"])
def update_experiment(request, pk=None):
    """Update an experiment by id

    Args:
        name: Name of the experiment
    """
    queryset = Experiment.objects.all()
    experiment = get_object_or_404(queryset, pk=pk)
    serializer = ExperimentSerializer(experiment, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return JsonResponse(serializer.data)
    return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["DELETE"])
def destroy_experiment(request, pk=None):
    """Delete an experiment by id

    Args:
        id: Primary key for the experiment
    """
    queryset = Experiment.objects.all()
    experiment = get_object_or_404(queryset, pk=pk)
    experiment.delete()
    return JsonResponse(
        {"message": "Experiment deleted"}, status=status.HTTP_204_NO_CONTENT
    )


@api_view(["GET"])
def list_machines(request):
    """List all machines"""
    queryset = Machine.objects.all()
    serializer = MachineSerializer(queryset, many=True)
    return JsonResponse(serializer.data, safe=False, status=status.HTTP_200_OK)


@api_view(["POST"])
def create_machine(request):
    """Create a new machine

    Args:
        id: Primary key for the machine
        time: Time the machine was created
    """
    serializer = MachineSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save() 
        return JsonResponse(serializer.validated_data,
                            status=status.HTTP_201_CREATED)
    return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def retrieve_machine(request, pk=None):
    """Retrieve a machine by id

    Args:
        id: Primary key for the machine
    """
    queryset = Machine.objects.all()
    machine = get_object_or_404(queryset, pk=pk)
    serializer = MachineSerializer(machine)
    return JsonResponse(serializer.data, status=status.HTTP_200_OK)


@api_view(["PUT"])
def update_machine(request, pk=None):
    """Update a machine by id

    Args:
        id: Primary key for the machine
        time_takes: Time the machine takes to process a sample
    """
    queryset = Machine.objects.all()
    machine = get_object_or_404(queryset, pk=pk)
    serializer = MachineSerializer(machine, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return JsonResponse(serializer.data, status=status.HTTP_200_OK)
    return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["DELETE"])
def destroy_machine(request, pk=None):
    """Delete a machine by id

    Args:
        id: Primary key for the machine
    """
    queryset = Machine.objects.all()
    machine = get_object_or_404(queryset, pk=pk)
    machine.delete()
    return JsonResponse({"message": "Experiment deleted"}, status=status.HTTP_204_NO_CONTENT)
