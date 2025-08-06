from flask import Blueprint, request, jsonify
from extensions import db
from models.usuario import Usuario
from werkzeug.security import generate_password_hash
from flask_jwt_extended import create_access_token

usuario_bp = Blueprint('usuario_bp', __name__)

@usuario_bp.route('/usuarios', methods=['POST'])
def criar_usuario():
    dados = request.get_json()
    nome = dados.get('nome')
    telefone = dados.get('telefone')
    senha = dados.get('senha')

    if not nome or not telefone or not senha:
        return jsonify({'erro': 'Nome, telefone e senha são obrigatórios.'}), 400

    if Usuario.query.filter_by(nome=nome).first():
        return jsonify({'erro': 'Nome de usuário já cadastrado.'}), 409

    usuario = Usuario(
        nome=nome,
        telefone=telefone,
        senha=generate_password_hash(senha)
    )
    db.session.add(usuario)
    db.session.commit()

    # Gera o token JWT para o novo usuário
    token = create_access_token(identity=str(usuario.id))

    return jsonify({
        'mensagem': 'Usuário cadastrado com sucesso!',
        'token': f'Bearer {token}'
    }), 201

@usuario_bp.route('/usuarios', methods=['GET'])
def listar_usuarios():
    usuarios = Usuario.query.all()
    lista = []
    for u in usuarios:
        lista.append({
            'id': u.id,
            'nome': u.nome,
            'telefone': u.telefone
        })
    return jsonify(lista), 200

@usuario_bp.route('/usuarios/<int:id>', methods=['GET'])
def obter_usuario(id):
    usuario = Usuario.query.get(id)
    if not usuario:
        return jsonify({'erro': 'Usuário não encontrado.'}), 404
    return jsonify({
        'id': usuario.id,
        'nome': usuario.nome,
        'telefone': usuario.telefone
    }), 200

@usuario_bp.route('/usuarios/<int:id>', methods=['DELETE'])
def deletar_usuario(id):
    usuario = Usuario.query.get(id)
    if not usuario:
        return jsonify({'erro': 'Usuário não encontrado.'}), 404
    db.session.delete(usuario)
    db.session.commit()
    return jsonify({'mensagem': f'Usuário {id} removido com sucesso!'}), 200

@usuario_bp.route('/usuarios', methods=['DELETE'])
def deletar_todos_usuarios():
    Usuario.query.delete()
    db.session.commit()
    return jsonify({'mensagem': 'Todos os usuários foram removidos.'}), 200