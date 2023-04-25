from rest_framework import serializers
from .models import User

class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['name', 'email']

    def create(self, validated_data):
        return User.objects.create(**validated_data)

class MainUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email']
