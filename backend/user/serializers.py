from rest_framework import serializers
from .models import User

class UserSerializer(serializers.Serializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'name', 'password', 'username']
        extra_kwargs = {'password': {'write_only': True}}
    
    #hash password
    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        
        if password is not None:
            instance.set_password(password)
            
        instance.save()
        
        return instance
    
