from django.urls import path
from . import views

urlpatterns = [
    path('', views.api_not_found),
    path('api', views.api_not_found),
    path('api/public', views.public),
    path('api/private', views.private),
    path('api/private-scoped', views.private_scoped),
    path('create', views.create_user_view.as_view()),
]
