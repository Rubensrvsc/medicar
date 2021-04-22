from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIRequestFactory, APIClient
import requests
# Create your tests here.

class TesteMedicar(TestCase):

    @classmethod
    def setUpTestData(cls):
        data = {
            "username": "Joao",
            "password": "JoaoJoao"
        }

    def test_especialidades(self):
        factory = APIClient()
        response = factory.get('/especialidades/')
        self.assertEquals(response.status_code,status.HTTP_200_OK)

    def test_medicos(self): 
        factory = APIClient()
        response = factory.get('/medicos/')
        self.assertEquals(response.status_code,status.HTTP_200_OK)
    
    def test_agendas(self):
        factory = APIClient()
        response = factory.get('/agendas/')
        self.assertEquals(response.status_code,status.HTTP_200_OK)