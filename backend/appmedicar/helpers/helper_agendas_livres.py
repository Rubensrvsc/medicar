from ..models import Agenda
from django.utils.timezone import now,localtime,localdate 
from django.db.models import Q

def agendas_livres():
    agenda = Agenda.objects.all()
    agenda = Agenda.objects.filter(Q(dia__gte=localdate()) | Q(dia=localdate()) ).order_by('dia')
    for i in agenda.filter(Q(dia__gte=localdate())): 
        if i.dia == localdate():
            hora_passada=0
            hora_marcadas= i.consulta_agenda.filter(Q(isMarcada=True) & Q(horario__hora__gt=localtime())).count()
            hora_passada = i.horario.filter(Q(hora__lt=localtime()) & Q(agenda__dia=localdate())).count()
            hora_agenda= i.horario.count() 
   
            if hora_marcadas+ hora_passada == hora_agenda: 
                    agenda=agenda.exclude(id=i.id) 
        hora_marcadas= i.consulta_agenda.filter(Q(isMarcada=True)).count() 

        hora_agenda= i.horario.count() 
  
        if hora_marcadas == hora_agenda: 
            agenda=agenda.exclude(id=i.id)

    return agenda

def agendas_filtro(medico_params,especialidade_params,data_inicio,data_fim,agenda):
    if medico_params:
        condition_medico = Q()
        for m in medico_params:
            condition_medico |= Q(medico=m)
        agenda = agenda.filter(condition_medico)
    if especialidade_params:
        condition_especialidade = Q()
        for e in especialidade_params:
            condition_especialidade |= Q(medico__especialidade_medico=e)
        agenda = agenda.filter(condition_especialidade)
        
    if data_inicio and data_fim:
        agenda = agenda.filter(Q(dia__range=[data_inicio,data_fim]))
    
    return agenda.all()