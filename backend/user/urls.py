from django.urls import path
from . import views

urlpatterns = [
    path('', views.CreateUserView.as_view(), name='create-user'),
]
