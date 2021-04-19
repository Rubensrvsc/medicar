from django.contrib import admin
from .models import *
from .forms import *

# Register your models here.

@admin.register(Especialidade)
class EspecialidadeAdmin(admin.ModelAdmin):
    list_display = ['nome_especialidade']

@admin.register(Horario)
class HorarioAdmin(admin.ModelAdmin):
    list_display = ['hora']

@admin.register(Agenda)
class AgendaAdmin(admin.ModelAdmin):
    list_display = ['dia','medico',]
    form = AgendaForm

@admin.register(Medico)
class MedicoAdmin(admin.ModelAdmin):
    list_display = ['nome_medico','crm','email','telefone','especialidade_medico',]
