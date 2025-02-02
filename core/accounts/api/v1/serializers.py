from rest_framework import serializers
from django.contrib.auth.models import User
from  django.contrib.auth.password_validation import validate_password  
from rest_framework.exceptions import *


class CustomRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(required = True , write_only=True)
    password1 = serializers.CharField(required = True , write_only=True)

    class Meta:
        model = User
        fields = ['username' , 'password' , 'password1']

    def validate(self, attrs):
        if attrs['password'] != attrs['password1']:
            raise serializers.ValidationError({'detail' : 'passwords do not match'})
        try:
            validate_password(attrs.get('password'))
        except ValidationError as e:
            raise serializers.ValidationError({'password' : list(e.messages)})
        return super().validate(attrs)
        
    def create(self, validated_data):
        validated_data.pop('password1' , None)
        return User.objects.create_user(**validated_data)