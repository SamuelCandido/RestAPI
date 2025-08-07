from flask import Blueprint, request, jsonify
from services.auth_service import AuthService

auth_bp = Blueprint('auth_bp', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    dados = request.get_json()
    nome = dados.get('nome')
    senha = dados.get('senha')

    token, erro = AuthService.autenticar(nome, senha)
    if erro:
        status = 400 if 'obrigatórios' in erro else 401
        return jsonify({'erro': erro}), status

    return jsonify({
        'token': f'Bearer {token}',
        'mensagem': 'Login realizado com sucesso!'
    }), 200
