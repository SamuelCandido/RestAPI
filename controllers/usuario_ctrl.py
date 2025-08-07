from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from services.usuario_service import UsuarioService

usuario_bp = Blueprint('usuario_bp', __name__)

#____________________________________________________________________________________________________________________________________#
@usuario_bp.route('/usuarios', methods=['POST'])
def criar_usuario():
    dados = request.get_json()
    nome = dados.get('nome')
    telefone = dados.get('telefone')
    senha = dados.get('senha')

    usuario, erro = UsuarioService.criar_usuario(nome, telefone, senha)
    if erro:
        status = 409 if 'ja cadastrado' in erro else 400
        return jsonify({'erro': erro}), status

    token = create_access_token(identity=str(usuario.id))
    return jsonify({
        'mensagem': 'Usuario cadastrado com sucesso!',
        'token': f'Bearer {token}'
    }), 201

#____________________________________________________________________________________________________________________________________#
@usuario_bp.route('/usuarios', methods=['GET'])
def listar_usuarios():
    usuarios = UsuarioService.listar_usuarios()
    lista = [{
        'id': u.id,
        'nome': u.nome,
        'telefone': u.telefone
    } for u in usuarios]
    return jsonify(lista), 200

#____________________________________________________________________________________________________________________________________#
@usuario_bp.route('/usuarios/<int:id>', methods=['GET'])
def obter_usuario(id):
    usuario = UsuarioService.obter_usuario(id)
    if not usuario:
        return jsonify({'erro': 'Usuario nao encontrado.'}), 404

    return jsonify({
        'id': usuario.id,
        'nome': usuario.nome,
        'telefone': usuario.telefone
    }), 200

#____________________________________________________________________________________________________________________________________#
@usuario_bp.route('/usuarios/<int:id>', methods=['DELETE'])
def deletar_usuario(id):
    sucesso = UsuarioService.deletar_usuario(id)
    if not sucesso:
        return jsonify({'erro': 'Usuario nao encontrado.'}), 404

    return jsonify({'mensagem': f'Usuario {id} removido com sucesso!'}), 200

#____________________________________________________________________________________________________________________________________#
@usuario_bp.route('/usuarios', methods=['DELETE'])
def deletar_todos_usuarios():
    UsuarioService.deletar_todos()
    return jsonify({'mensagem': 'Todos os usuarios foram removidos.'}), 200
