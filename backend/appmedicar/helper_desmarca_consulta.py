from .models import Consulta
from django.utils.timezone import now,localtime,localdate 
from django.db.models import Q
from rest_framework.response import Response
from rest_framework import status

def desmarcar_consulta(id,username):
    consulta = Consulta.objects.filter(id=id)
    if consulta.exists():
        consulta_usuario=consulta.filter(Q(cliente__username=username) & Q(id=id))
        if consulta_usuario.exists():
            consulta_horario = consulta_usuario.filter(Q(agenda__dia__lt=localdate())  & Q(isMarcada=True)
                | Q(agenda__dia=localdate()) & Q(horario__hora__lte=localtime()) & Q(isMarcada=True) )
                
            if consulta_horario.exists():
                return Response({'Erro':'consulta já passou'},status=status.HTTP_404_NOT_FOUND)


            return Response(consulta_usuario.filter(id=id).first().delete(),status=status.HTTP_200_OK)
            
        return Response({'Erro':'Essa consulta não foi marcada pelo usuário logado'},status=status.HTTP_404_NOT_FOUND)
    return Response({'Erro':'Essa consulta não existe'},status=status.HTTP_404_NOT_FOUND)