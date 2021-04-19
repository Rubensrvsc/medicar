from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
from django.utils.timezone import now
from django.db.models import Q
from django.http import HttpResponse

# Create your models here.

class Especialidade(models.Model):

    nome_especialidade = models.CharField(max_length=100,unique=True)

    def __str__(self):
        return self.nome_especialidade

class Medico(models.Model):
    nome_medico = models.CharField(max_length=100)
    crm = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    telefone = models.CharField(max_length=20)
    especialidade_medico = models.ForeignKey(Especialidade,related_name="medico",on_delete=models.CASCADE)

    def __str__(self):
        return self.nome_medico

class Horario(models.Model):
    hora = models.TimeField()
    
    def __str__(self):
        return str(self.hora)
        
class Agenda(models.Model):
    dia = models.DateField()
    medico = models.ForeignKey(Medico,related_name="agenda",on_delete=models.CASCADE)
    horario = models.ManyToManyField(Horario,related_name="agenda")


    def __str__(self):
        return self.medico.nome_medico + " "+ str(self.dia)
    

class Consulta(models.Model):
    agenda = models.ForeignKey(Agenda,related_name="consulta_agenda",on_delete=models.CASCADE)
    cliente = models.ForeignKey(User,related_name="consulta_cliente",on_delete=models.CASCADE)
    data_agendamento = models.TimeField(default=now)
    horario = models.ForeignKey(Horario,related_name="consulta_horario",on_delete=models.CASCADE, null=True, blank=True)
    isMarcada = models.BooleanField(default=True)

    def __str__(self):
        return str(self.isMarcada)
