# medicar


## Repositorio do teste de backend engenieer na IntMed

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
| GET | `http://localhost:8000/especialidades/` | Obtém as especialidades cadastradas |
| GET | `http://localhost:8000/medicos/` | Obtém os médicos cadastradas |
| GET | `http://localhost:8000/consultas/` | Obtém as consultas do usuário logado |
| POST | `http://localhost:8000/agendar_consulta/` | Marca uma consulta para o usuário logado |
| GET | `http://localhost:8000/agendas/` | Obtém as agendas livres |
| DELETE | `http://localhost:8000/desmarcar_consulta/<int:id>` | Desmarca uma consulta do usuário logado |
