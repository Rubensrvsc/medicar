from rest_framework import serializers
from django.contrib.auth.models import User
from django.utils.timezone import now,localtime,localdate 
from .models import *
from django.db.models import Q
from rest_framework.response import Response

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

    def validate(self, data):

        agenda = Agenda.objects.filter(id=data['agenda'])
        if agenda.exists() == False:
            raise serializers.ValidationError("Essa agenda não existe")

        if agenda.filter(Q(dia__lt=localdate())).exists():
            raise serializers.ValidationError("Agenda é de um dia passado")

        agenda_user = Agenda.objects.get(id=data['agenda'])

        if agenda_user.horario.filter(hora=data['horario']).exists()==False:
            raise serializers.ValidationError("Esse horario não existe nessa agenda")
        if agenda_user.dia == localdate() and datetime.strptime(data['horario'],'%H:%M').time() < localtime().time():
            raise serializers.ValidationError("Agenda do dia de hoje mas o horário já passou")
        

        consulta_cliente = Consulta.objects.filter(Q(agenda__id=agenda_user.id) & Q(agenda__dia=agenda_user.dia) 
        & Q(horario__hora=data['horario']) & Q(cliente__username=self.context['request'].user.username) & Q(isMarcada=True))
        if consulta_cliente.exists():
            raise serializers.ValidationError("Cliente já marcou uma consulta para este dia e horario")


        consulta_ja_marcada = Consulta.objects.filter(Q(agenda__id=agenda_user.id) & Q(agenda__dia=agenda_user.dia) 
            & Q(horario__hora=data['horario'])& Q(isMarcada=True))

        if consulta_ja_marcada.exists() == True:
            raise serializers.ValidationError("Já existe uma consulta para este dia e horario")
 
        return data
    
    def create(self, validated_data):
        horario = Horario.objects.get(hora=validated_data['horario'])
        agenda = Agenda.objects.get(id=validated_data['agenda'])
        user = User.objects.get(username='victor')
        consulta_criada = Consulta.objects.create(agenda=agenda,cliente=user,
            horario=horario)

        return consulta_criada
        
    
    def to_representation(self, instance):
        return {
                'id':instance.id,
                'dia':instance.agenda.dia,
                'horario':instance.horario.hora,
                'data_agendamento':instance.data_agendamento,
                'medico':{
                    'id': instance.agenda.medico.id,
                    'crm':instance.agenda.medico.crm,
                    'nome': instance.agenda.medico.nome_medico,
                    'especialidade':{
                        'id': instance.agenda.medico.especialidade_medico.id,
                        'especialidade': instance.agenda.medico.especialidade_medico.nome_especialidade
                    },
                },
            }
    

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
                return instance.horario.all().values("hora")
                for j in instance.horario.filter(hora__gt=localtime()):
                    lista.append(j.hora)
            elif instance.consulta_agenda.count()>0:
                return instance.horario.filter(~Q(hora__in=instance.consulta_agenda.all().values("horario__hora")) & 
                Q(hora__gt=localtime())).values("hora")
                for i in instance.consulta_agenda.all(): 
                    for j in instance.horario.filter(hora__gt=localtime()): 
                        if j.hora != i.horario.hora: 
                            lista.append(j.hora)
        
            return lista
        if instance.dia > localdate():
  
            
            if instance.consulta_agenda.count()==0:
                return instance.horario.all().values("hora")
                for j in instance.horario.all():
                    lista.append(j.hora)
            elif instance.consulta_agenda.count()>0:
                return instance.horario.filter(~Q(hora__in=instance.consulta_agenda.all().values("horario__hora"))).values("hora") 
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