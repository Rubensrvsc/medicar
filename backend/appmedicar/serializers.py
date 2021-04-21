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
        fields = ['id','crm','nome_medico','especialidade']
    
    def get_especialidade(self,instance):
        return Especialidade.objects.filter(medico=instance.id).values('id','nome_especialidade')


class ConsultaSerializerList(serializers.ModelSerializer):

    dia = serializers.PrimaryKeyRelatedField(source='agenda.dia',queryset=Agenda.objects.all())
    horario = serializers.PrimaryKeyRelatedField(source='horario.hora',queryset=Horario.objects.all())
    medico = serializers.SerializerMethodField()

    class Meta:
        model = Consulta
        fields = ['id','dia','horario','data_agendamento','medico',]
    
    def get_medico(self,instance):
        medico = MedicoListSerializer(
            instance=instance.agenda.medico,
            many=False
        )
        return medico.data

class ConsultaSerializerCreate(serializers.Serializer):

    agenda = serializers.IntegerField()
    horario = serializers.TimeField()


class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password')

class ObterTokenSerializer(serializers.Serializer):

    username = serializers.CharField
    password = serializers.CharField

class DesmarcarConsultaSerializer(serializers.ModelSerializer):

    class Meta:
        model = Consulta
        fields = '__all__'