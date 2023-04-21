from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SampleViewSet, ExperimentViewSet, MachineViewSet


# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'samples', SampleViewSet, basename='sample')
router.register(r'experiments', ExperimentViewSet, basename='experiment')
router.register(r'machines', MachineViewSet, basename='machine')


urlpatterns = [
    path('', include(router.urls)),
]


"""
/samples/
/samples/<pk>/
/experiments/
/experiments/<pk>/
/machines/
/machines/<pk>/
"""
