from models.usuario import Usuario
from werkzeug.security import check_password_hash
from flask_jwt_extended import create_access_token

class AuthService:
    @staticmethod
    def autenticar(nome, senha):
        if not nome or not senha:
            return None, 'Nome e senha são obrigatórios.'

        usuario = Usuario.query.filter_by(nome=nome).first()
        if usuario and check_password_hash(usuario.senha, senha):
            token = create_access_token(identity=str(usuario.id))
            return token, None
        else:
            return None, 'Nome ou senha inválidos.'
