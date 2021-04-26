# Medicar


## Repositorio do teste de backend na IntMed

### Tecnologias usadas

```
Python3
Pip3
SQLITE3
Django
Django Rest Framework
```
### Running this project

#### Entre na pasta backend e rode o seguintes comandos

```
pip3 install -r requirements
```

```
python3 manage.py makemigrations
```

```
python3 manage.py migrate
```

```
python3 manage.py runserver
```

### Running Tests

```
python3 manage.py test
```

### EndPoints

| Method |EndPoint | Description |
|---|---|---|
| POST | `http://localhost:8000/user_create/` | Cria um usuário |
| GET | `http://localhost:8000/obter_token/` | Obtém o token de um usuário |
| GET | `http://localhost:8000/especialidades/` | Obtém as especialidades cadastrados |
| GET | `http://localhost:8000/medicos/` | Obtém os médicos cadastradas |
| GET | `http://localhost:8000/consultas/` | Obtém as consultas do usuário logado |
| POST | `http://localhost:8000/agendar_consulta/` | Marca uma consulta para o usuário logado |
| GET | `http://localhost:8000/agendas/` | Obtém as agendas livres |
| DELETE | `http://localhost:8000/desmarcar_consulta/<int:id>` | Desmarca uma consulta do usuário logado |


## Documentation of EndPoints

### Endpoint:

- POST: `/user_create/`

+ Request

            {
                
                "username": "Maria",
                "email":"Maria@gmail.com",
                "password": "Maria12345",
                
            }
+ Response

      {"token":"a394f0b3d620a3c8081d7beac398ea73ec14f1e4"}
      
### Endpoint:

- POST: `/obter_token/`

+ Request

            {
                
                "username": "Maria",
                "password": "Maria12345",
                
            }
+ Response

      {"token":"a394f0b3d620a3c8081d7beac398ea73ec14f1e4"}
      
      
### Autenticação

##### Com exceção dos endpoints /user_create/ e /obter_token/, para todos os outros devem ser enviado o token do usuário. Veja um exemplo

```
GET /medicos/
Authorization: Token a394f0b3d620a3c8081d7beac398ea73ec14f1e4
```

### Para facilitar o processo de teste da aplicação é recomendável o uso do aplicativo Postman para fazer as requisições necessárias

### EndPoint


- GET: `/medicos/`

        {
          "id": 1,
          "crm": "1234",
          "nome_medico": "Medico 1",
            "especialidade": [
              {
                "id": 1,
                "nome_especialidade": "Urologia"
              }
          ]
        },
        {
          "id": 2,
          "crm": "4321",
          "nome_medico": "Medico 2",
          "especialidade": [
            {
                "id": 2,
                "nome_especialidade": "Pediatria"
            }
        ]
      }
 
 #### Filtros
 
 ```
GET /medicos/?search=Joao&especialidade=1&especialidade=3
```

### EndPoint


- GET: `/especialidades/`

      {
        "id": 1,
        "nome_especialidade": "Urologia"
      },
      {
        "id": 2,
        "nome_especialidade": "Pediatria"
      },
      {
        "id": 3,
        "nome_especialidade": "Cardiologia"
      },
      {
        "id": 4,
        "nome_especialidade": "Oncologia"
      }
      
#### Filtros
 
 ```
GET /especialidades/?search=ped
```

### EndPoint


- GET: `/agendas/`

        {
          "id": 2,
          "medico": {
            "id": 1,
            "crm": "1234",
            "nome_medico": "Medico 1",
            "especialidade": [
                {
                    "id": 1,
                    "nome_especialidade": "Urologia"
                }
            ]
        },
        "dia": "2021-04-25",
        "horarios": [
            "17:00:00",
            "18:00:00",
            "19:00:00"
        ]
      },
      {
        "id": 4,
        "medico": {
            "id": 3,
            "crm": "4567",
            "nome_medico": "Medico 3",
            "especialidade": [
                {
                    "id": 3,
                    "nome_especialidade": "Cardiologia"
                }
            ]
        },
        "dia": "2021-04-26",
        "horarios": [
            "17:00:00",
            "18:00:00",
            "19:00:00"
        ]
      }
      
 #### Regras de negócio
 
+ As agendas vem ordenadas por ordem crescente de data
+ Agendas para datas passadas ou que todos os seus horários já foram preenchidos são excluídas da listagem
+ Horários dentro de uma agenda que já passaram ou que foram preenchidos devem ser excluídos da listagem


 #### Filtros
 
 + Identificador de um ou mais médicos
 + Identificador de uma ou mais especialidades
 + Intervalo de data
 
 ```
GET /agendas/?medico=1&especialidade=2&data_inicio=2021-04-01&data_fim=2021-04-29
```

### Endpoint:

- POST: `/agendar_consulta/`

+ Request

            {
                
                "agenda_id": 5,
                "horario":"18:00"
                
            }
+ Response

      {
        "id": 4,
        "dia": "2021-04-27",
        "horario": "18:00:00",
        "data_agendamento": "2021-04-25T13:36:33.642614Z",
        "medico": {
              "id": 3,
              "crm": "4567",
              "nome": "Medico 3",
              "especialidade": {
                  "id": 3,
                  "especialidade": "Cardiologia"
              }
        }
      }
#### Regras de negócio

+ A data em que o agendamento foi feito é salva ao se marcar uma consulta
+ Não é possível marcar uma consulta para um dia e horário passados
+ Não é possível marcar uma consulta se o usuário já possui uma consulta marcada no mesmo dia e horário
+ Não é possível marcar uma consulta se o dia e horário já foram preenchidos


### Endpoint:

- GET: `/consultas/`


+ Response

      {
        "id": 4,
        "dia": "2021-04-27",
        "horario": "18:00:00",
        "data_agendamento": "2021-04-25T13:36:33.642614Z",
        "medico": {
              "id": 3,
              "crm": "4567",
              "nome": "Medico 3",
              "especialidade": {
                  "id": 3,
                  "especialidade": "Cardiologia"
              }
        }
      }
      
      
#### Regras de negócio

+ A listagem não exibem consultas para dia e horário passados
+ Os itens da listagem vem ordenados por ordem crescente do dia e horário da consulta
      
### Endpoint:

- DELETE: `/desmarcar_consulta/<int:id>`


+ Response 200 OK

#### Regras de negócio

+ Não é possível desmarcar uma consulta que não foi marcada pelo usuário logado
+ Não é possível desmarcar uma consulta que nunca foi marcada (identificador inexistente)
+ Não é possível desmarcar uma consulta que já aconteceu

      
