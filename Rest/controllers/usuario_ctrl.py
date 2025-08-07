from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash
from flask_jwt_extended import create_access_token
from dao.usuario_dao import UsuarioDAO

usuario_bp = Blueprint('usuario_bp', __name__)

#____________________________________________________________________________________________________________________________________#
@usuario_bp.route('/usuarios', methods=['POST'])
def criar_usuario():
    dados = request.get_json()
    nome = dados.get('nome')
    telefone = dados.get('telefone')
    senha = dados.get('senha')

    if not nome or not telefone or not senha:
        return jsonify({'erro': 'Nome, telefone e senha são obrigatórios.'}), 400

    if UsuarioDAO.get_by_nome(nome):
        return jsonify({'erro': 'Nome de usuário já cadastrado.'}), 409

    usuario = UsuarioDAO.add(
        type('Usuario', (), {})(
            nome=nome,
            telefone=telefone,
            senha=generate_password_hash(senha)
        )
    )

    token = create_access_token(identity=str(usuario.id))

    return jsonify({
        'mensagem': 'Usuário cadastrado com sucesso!',
        'token': f'Bearer {token}'
    }), 201

#____________________________________________________________________________________________________________________________________#
@usuario_bp.route('/usuarios', methods=['GET'])
def listar_usuarios():
    usuarios = UsuarioDAO.get_all()
    lista = []

    for u in usuarios:
        lista.append({
            'id': u.id,
            'nome': u.nome,
            'telefone': u.telefone
        })
    return jsonify(lista), 200

#____________________________________________________________________________________________________________________________________#
@usuario_bp.route('/usuarios/<int:id>', methods=['GET'])
def obter_usuario(id):
    usuario = UsuarioDAO.get_by_id(id)
    if not usuario:
        return jsonify({'erro': 'Usuário não encontrado.'}), 404
    
    return jsonify({
        'id': usuario.id,
        'nome': usuario.nome,
        'telefone': usuario.telefone
    }), 200

#____________________________________________________________________________________________________________________________________#
@usuario_bp.route('/usuarios/<int:id>', methods=['DELETE'])
def deletar_usuario(id):
    usuario = UsuarioDAO.get_by_id(id)
    if not usuario:
        return jsonify({'erro': 'Usuário não encontrado.'}), 404
    
    UsuarioDAO.delete(usuario)
    return jsonify({'mensagem': f'Usuário {id} removido com sucesso!'}), 200

#____________________________________________________________________________________________________________________________________#
@usuario_bp.route('/usuarios', methods=['DELETE'])
def deletar_todos_usuarios():
    UsuarioDAO.delete_all()
    return jsonify({'mensagem': 'Todos os usuários foram removidos.'}), 200