from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from models.usuario import Usuario
from werkzeug.security import check_password_hash

auth_bp = Blueprint('auth_bp', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    dados = request.get_json()
    nome = dados.get('nome')
    senha = dados.get('senha')

    if not nome or not senha:
        return jsonify({'erro': 'Nome e senha são obrigatórios.'}), 400

    usuario = Usuario.query.filter_by(nome=nome).first()
    if usuario and check_password_hash(usuario.senha, senha):
        token = create_access_token(identity=str(usuario.id))
        return jsonify({
            'token': f'Bearer {token}',
            'mensagem': 'Login realizado com sucesso!'
        }), 200
    else:
        return jsonify({'erro': 'Nome ou senha inválidos.'}), 401

