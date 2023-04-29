from django.urls import path
from .views import (list_samples, create_sample, retrieve_sample, update_sample, destroy_sample,
                    list_experiments, create_experiment, retrieve_experiment, update_experiment, destroy_experiment,
                    list_machines, create_machine, retrieve_machine, update_machine, destroy_machine)

urlpatterns = [
    # Sample views
    path('samples/', list_samples, name='sample-list'),
    path('samples/create/', create_sample, name='sample-create'),
    path('samples/<int:pk>/', retrieve_sample, name='sample-retrieve'),
    path('samples/<int:pk>/update/', update_sample, name='sample-update'),
    path('samples/<int:pk>/delete/', destroy_sample, name='sample-destroy'),

    # Experiment views
    path('experiments/', list_experiments, name='experiment-list'),
    path('experiments/create/', create_experiment, name='experiment-create'),
    path('experiments/<int:pk>/', retrieve_experiment, name='experiment-retrieve'),
    path('experiments/<int:pk>/update/', update_experiment, name='experiment-update'),
    path('experiments/<int:pk>/delete/', destroy_experiment, name='experiment-destroy'),

    # Machine views
    path('machines/', list_machines, name='machine-list'),
    path('machines/create/', create_machine, name='machine-create'),
    path('machines/<int:pk>/', retrieve_machine, name='machine-retrieve'),
    path('machines/<int:pk>/update/', update_machine, name='machine-update'),
    path('machines/<int:pk>/delete/', destroy_machine, name='machine-destroy'),
]
