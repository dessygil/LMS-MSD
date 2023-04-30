from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.http import JsonResponse
from rest_framework import viewsets, status
from rest_framework.decorators import api_view
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

#TODO
# We are going to want add only the ability for the lab manager to create new machines
# and new experiments. This can be done through auth0 using @require_auth(<permission>)

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


@api_view(['GET'])
@require_auth(None)
def list_samples(request):
    queryset = Sample.objects.all()
    serializer = SampleSerializer(queryset, many=True)
    return JsonResponse(serializer.data, safe=False, status=200)

@api_view(['POST'])
@require_auth(None)
def create_sample(request):
    serializer = SampleSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user=request.user)
        return JsonResponse(serializer.data, status=201)
    return JsonResponse(serializer.errors, status=400)

@api_view(['GET'])
@require_auth(None)
def retrieve_sample(request, pk=None):
    try:
        sample = Sample.objects.get(pk=pk, experiment__user=request.user)
        serializer = SampleSerializer(sample)
        return JsonResponse(serializer.data, status=200)
    except Sample.DoesNotExist:
        return JsonResponse(status=404)

@api_view(['PUT'])
@require_auth(None)
def update_sample(request, pk=None):
    try:
        sample = Sample.objects.get(pk=pk, experiment__user=request.user)
        serializer = SampleSerializer(sample, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)
    except Sample.DoesNotExist:
        return JsonResponse(status=404)

@api_view(['DELETE'])
@require_auth(None)
def destroy_sample(request, pk=None):
    queryset = Sample.objects.all()
    sample = get_object_or_404(queryset, pk=pk)
    sample.delete()
    return JsonResponse({"message": "Sample deleted"}, status=204)

#TODO
# add back auth0

@api_view(['GET'])
def list_experiments(request):
    queryset = Experiment.objects.all()
    serializer = ExperimentSerializer(queryset, many=True)
    return JsonResponse(serializer.data, safe=False, status=200)

@api_view(['POST'])
def create_experiment(request):
    serializer = ExperimentSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return JsonResponse(serializer.data, status=201)
    return JsonResponse(serializer.errors, status=400)

@api_view(['GET'])
def retrieve_experiment(request, pk=None):
    queryset = Experiment.objects.all()
    experiment = get_object_or_404(queryset, pk=pk)
    serializer = ExperimentSerializer(experiment)
    return JsonResponse(serializer.data, status=200)

@api_view(['PUT'])
def update_experiment(request, pk=None):
    queryset = Experiment.objects.all()
    experiment = get_object_or_404(queryset, pk=pk)
    serializer = ExperimentSerializer(experiment, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return JsonResponse(serializer.data)
    return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def destroy_experiment(request, pk=None):
    queryset = Experiment.objects.all()
    experiment = get_object_or_404(queryset, pk=pk)
    experiment.delete()
    return JsonResponse({"message": "Experiment deleted"}, status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
def list_machines(request):
    queryset = Machine.objects.all()
    serializer = MachineSerializer(queryset, many=True)
    return JsonResponse(serializer.data, safe=False, status=status.HTTP_200_OK)

@api_view(['POST'])
def create_machine(request):
    serializer = MachineSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return JsonResponse(serializer.validated_data, status=status.HTTP_201_CREATED)
    return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def retrieve_machine(request, pk=None):
    queryset = Machine.objects.all()
    machine = get_object_or_404(queryset, pk=pk)
    serializer = MachineSerializer(machine)
    return JsonResponse(serializer.data, status=status.HTTP_200_OK)

@api_view(['PUT'])
def update_machine(request, pk=None):
    queryset = Machine.objects.all()
    machine = get_object_or_404(queryset, pk=pk)
    serializer = MachineSerializer(machine, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return JsonResponse(serializer.data, status=status.HTTP_200_OK)
    return JsonResponse(serializer.errors, status=400)

@api_view(['DELETE'])
def destroy_machine(request, pk=None):
    queryset = Machine.objects.all()
    machine = get_object_or_404(queryset, pk=pk)
    machine.delete()
    return JsonResponse({"message": "Experiment deleted"}, status=204)
