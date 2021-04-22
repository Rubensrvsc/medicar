from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIRequestFactory, APIClient
import requests
from.models import *
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
# Create your tests here.

class TesteMedicar(TestCase):

    @classmethod
    def setUpTestData(cls):
        data = {
            "username": "Joao",
            "email":"Joao@mail.com",
            "password": "JoaoJoao"
        }
        factory = APIClient()
        factory.post('/user_create/',data=data)
        Horario.objects.create(hora='22:00')
        Horario.objects.create(hora='18:00')
        Horario.objects.create(hora='17:00')

        Especialidade.objects.create(nome_especialidade='pediatria')
        Especialidade.objects.create(nome_especialidade='cardiologia')
        Especialidade.objects.create(nome_especialidade='oncologia')

        especialidade = Especialidade.objects.get(id=1)

        Medico.objects.create(nome_medico="Luiz",
        crm="6543",
        email="Luiz@mail.com",
        telefone="9847464",
        especialidade_medico=especialidade
        )

        h1 = Horario.objects.get(id=1)
        h2 = Horario.objects.get(id=2)
        h3 = Horario.objects.get(id=3)

        m1 = Medico.objects.get(id=1)

        a=Agenda.objects.create(dia='2021-04-25',medico=m1)
        a.horario.add(h1)
        a.horario.add(h2)

        a2=Agenda.objects.create(dia='2021-04-18',medico=m1)
        a2.horario.add(h2)
        a2.horario.add(h3)
        
    def test_especialidades(self):
        factory = APIClient()
        token = Token.objects.get(user__username='Joao')
        factory.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = factory.get('/especialidades/')
        self.assertEquals(response.status_code,status.HTTP_200_OK)

    def test_medicos(self): 
        factory = APIClient()
        token = Token.objects.get(user__username='Joao')
        factory.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = factory.get('/medicos/')
        self.assertEquals(response.status_code,status.HTTP_200_OK)
    
    def test_agendas(self):
        factory = APIClient()
        token = Token.objects.get(user__username='Joao')
        factory.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = factory.get('/agendas/')
        self.assertEquals(response.status_code,status.HTTP_200_OK)
    
    def test_consultas(self):
        factory = APIClient()
        token = Token.objects.get(user__username='Joao')
        factory.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = factory.get('/consultas/')
        self.assertEquals(response.status_code,status.HTTP_200_OK)
    
    def test_agendas_livres(self):
        factory = APIClient()
        token = Token.objects.get(user__username='Joao')
        factory.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = factory.get('/agendas/')
        self.assertEqual(len(response.json()),1)
        self.assertEquals(response.status_code,status.HTTP_200_OK)
    
    def test_consultas_usuario_logado(self):
        factory = APIClient()
        token = Token.objects.get(user__username='Joao')
        factory.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = factory.get('/consultas/')
        self.assertEqual(len(response.json()),0)
    
    def test_especialidades_parametros(self):
        factory = APIClient()
        token = Token.objects.get(user__username='Joao')
        factory.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = factory.get('/especialidades/?search=c')
        self.assertEqual(len(response.json()),2)
        self.assertEquals(response.status_code,status.HTTP_200_OK)
    
    def test_medicos_parametros(self):
        factory = APIClient()
        token = Token.objects.get(user__username='Joao')
        factory.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = factory.get('/medicos/?search=l&especialidade=1&especialidade=3')
        self.assertEqual(len(response.json()),1)
        self.assertEquals(response.status_code,status.HTTP_200_OK)
    
    def test_agendar_consulta(self):
        factory = APIClient()
        token = Token.objects.get(user__username='Joao')
        factory.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        data = {
            'agenda': 1,
            'horario': '18:00'
        }
        response = factory.post('/agendar_consulta/',data)
        self.assertEquals(response.status_code,status.HTTP_200_OK)

    def test_desmarcar_consulta(self):
        factory = APIClient()
        token = Token.objects.get(user__username='Joao')
        factory.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        data = {
            'agenda': 1,
            'horario': '18:00'
        }
        factory.post('/agendar_consulta/',data)
        response = factory.delete('/desmarcar_consulta/1')
        self.assertEquals(response.status_code,status.HTTP_200_OK)

    def test_marcar_consulta_agenda_dia_passada(self):
        factory = APIClient()
        token = Token.objects.get(user__username='Joao')
        factory.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        data = {
            'agenda': 2,
            'horario': '18:00'
        }
        response = factory.post('/agendar_consulta/',data)
        self.assertEquals(response.status_code,status.HTTP_401_UNAUTHORIZED)
