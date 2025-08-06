# Rest API - Comandas e Usuários

API RESTful desenvolvida em Flask para gerenciamento de usuários, comandas e autenticação JWT.  
Inclui documentação interativa via Swagger UI.

## Funcionalidades

- Cadastro, consulta e remoção de usuários
- Autenticação via JWT (login)
- Cadastro, consulta, atualização e remoção de comandas com produtos
- Documentação Swagger UI

## Instalação

1. Clone o repositório:
   ```sh
   git clone https://github.com/seu-usuario/seu-repo.git
   cd Rest
   ```

2. Instale as dependências:
   ```sh
   pip install -r requirements.txt
   ```

3. Execute a aplicação:
   ```sh
   python app.py
   ```

## Documentação Swagger

Acesse [http://localhost:8080/apidocs](http://localhost:8080/apidocs) para visualizar e testar os endpoints.

## Exemplos de Uso

### Cadastro de Usuário

```json
POST /RestAPIFurb/usuarios
{
  "nome": "joao",
  "telefone": "478888888",
  "senha": "123"
}
```

### Login

```json
POST /RestAPIFurb/login
{
  "nome": "joao",
  "senha": "123"
}
```

### Cadastro de Comanda

```json
POST /RestAPIFurb/comandas
{
  "idUsuario": 1,
  "produtos": [
    {"nome": "X-Salada", "preco": 30}
  ]
}
```

## Observações

- O banco de dados é SQLite e já está configurado em `config.py`.
- O Swagger UI está integrado e lê o arquivo `swagger/swagger.yaml`.
- Para endpoints protegidos, envie o token JWT no header:
  ```
  Authorization: Bearer <seu_token>
  ```

## Dependências

Veja o arquivo [`requirements.txt`](requirements.txt):

```
flask
flask_sqlalchemy
flask_marshmallow
marshmallow-sqlalchemy
flask-jwt-extended
flasgger
flask-cors
```
