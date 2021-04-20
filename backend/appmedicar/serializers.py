from rest_framework import serializers
from django.contrib.auth.models import User
from .models import *

class EspecialidadeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Especialidade
        fields = '__all__'

class MedicoListSerializer(serializers.ModelSerializer):

    especialidade = serializers.SerializerMethodField()

    class Meta:
        model = Medico
        fields = ['id','nome_medico','crm','email','telefone','especialidade']
    
    def get_especialidade(self,instance):
        return Especialidade.objects.filter(medico=instance.id).values('id','nome_especialidade')

class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password')

class ObterTokenSerializer(serializers.Serializer):

    username = serializers.CharField
    password = serializers.CharField