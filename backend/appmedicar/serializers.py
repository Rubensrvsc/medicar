from rest_framework import serializers
from django.contrib.auth.models import User
from .models import *

class EspecialidadeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Especialidade
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password')

class ObterTokenSerializer(serializers.Serializer):

    username = serializers.CharField
    password = serializers.CharField