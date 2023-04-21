from rest_framework import serializers
from .models import User

#TODO might be able to delete this class below
class user_serializer(serializers.Serializer):
    class Meta:
        model = User
        fields = ['email', 'name']

class create_user_serializer(serializers.Serializer):
    
    name = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    
    class Meta:
        model = User
        fields = ['email', 'name']
