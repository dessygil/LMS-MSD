from django.urls import path
from . import views

urlpatterns = [
    path('', views.api_not_found),
    path('api', views.api_not_found),
    path('api/public', views.public),
    path('api/private', views.private),
    path('api/private-scoped', views.private_scoped),
    path('api/user', views.check_or_create_user),
]
