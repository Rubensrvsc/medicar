from rest_framework import serializers
from django.contrib.auth.models import User
from django.utils.timezone import now,localtime,localdate 
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

class AgendaSerializer(serializers.ModelSerializer):

    horarios = serializers.SerializerMethodField()
    medico = MedicoListSerializer()

    class Meta:
        model = Agenda
        fields = ['id','medico','dia','horarios',]

    def get_horarios(self,instance):
        lista = []
        if instance.dia == localdate():
            if instance.consulta_agenda.count()==0:
                for j in instance.horario.filter(hora__gt=localtime()):
                    lista.append(j.hora)
            elif instance.consulta_agenda.count()>0:
                for i in instance.consulta_agenda.all(): 
                    for j in instance.horario.filter(hora__gt=localtime()): 
                        if j.hora != i.horario.hora: 
                            lista.append(j.hora)
        
            return lista
        if instance.dia > localdate():
  
            
            if instance.consulta_agenda.count()==0:
                for j in instance.horario.all():
                    lista.append(j.hora)
            elif instance.consulta_agenda.count()>0:
                for i in instance.consulta_agenda.all(): 
                    for j in instance.horario.all(): 
                        if j.hora != i.horario.hora: 
                            lista.append(j.hora)
        
            return lista


class ObterTokenSerializer(serializers.Serializer):

    username = serializers.CharField
    password = serializers.CharField

class DesmarcarConsultaSerializer(serializers.ModelSerializer):

    class Meta:
        model = Consulta
        fields = '__all__'