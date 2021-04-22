from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIRequestFactory, APIClient
import requests
from rest_framework.authtoken.models import Token
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
    