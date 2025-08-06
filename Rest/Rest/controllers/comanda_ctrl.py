from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from extensions import db
from models.usuario import Usuario
from models.produto import Produto
from models.comanda import Comanda

comanda_bp = Blueprint('comanda_bp', __name__)

# LISTA todas as comandas (só dados do usuário)
@comanda_bp.route('/comandas', methods=['GET'])
def listar_comandas():
    comandas = Comanda.query.all()
    resultado = []
    for comanda in comandas:
        resultado.append({
            "idUsuario": comanda.usuario.id,
            "nomeUsuario": comanda.usuario.nome,
            "telefoneUsuario": comanda.usuario.telefone
        })
    return jsonify(resultado), 200

# BUSCA comanda específica (usuário + produtos)
@comanda_bp.route('/comandas/<int:id>', methods=['GET'])
def obter_comanda(id):
    comanda = Comanda.query.get(id)
    if not comanda:
        return jsonify({'erro': 'Comanda nao encontrada.'}), 404
    return jsonify({
        "idUsuario": comanda.usuario.id,
        "nomeUsuario": comanda.usuario.nome,
        "telefoneUsuario": comanda.usuario.telefone,
        "produtos": [
            {
                "id": produto.id,
                "nome": produto.nome,
                "preco": produto.preco
            } for produto in comanda.produtos
        ]
    }), 200

# CRIA comanda + produtos juntos
@comanda_bp.route('/comandas', methods=['POST'])
@jwt_required()
def criar_comanda():
    json_data = request.get_json()
    if not json_data:
        return jsonify({'erro': 'Dados nao fornecidos.'}), 400

    id_usuario = json_data.get('idUsuario')
    produtos_data = json_data.get('produtos')

    if not id_usuario:
        return jsonify({'erro': 'idUsuario é obrigatório.'}), 400

    usuario = Usuario.query.get(id_usuario)
    if not usuario:
        return jsonify({'erro': 'Usuario nao encontrado.'}), 404

    if not produtos_data or not isinstance(produtos_data, list):
        return jsonify({'erro': 'produtos é obrigatório.'}), 400

    produtos = []
    for p in produtos_data:
        produto = None
        if p.get('id'):
            produto = Produto.query.get(p.get('id'))
        if not produto:
            nome = p.get('nome')
            preco = p.get('preco')
            if not nome or preco is None:
                continue
            produto = Produto(nome=nome, preco=preco)
            db.session.add(produto)
            db.session.flush()
        produtos.append(produto)

    if not produtos:
        return jsonify({'erro': 'Produtos invalidos.'}), 400

    comanda = Comanda(usuario=usuario, produtos=produtos)
    db.session.add(comanda)
    db.session.commit()

    return jsonify({
        "idUsuario": usuario.id,
        "nomeUsuario": usuario.nome,
        "telefoneUsuario": usuario.telefone,
        "produtos": [
            {
                "id": produto.id,
                "nome": produto.nome,
                "preco": produto.preco
            } for produto in comanda.produtos
        ]
    }), 201

# ATUALIZA produtos da comanda (JWT)
@comanda_bp.route('/comandas/<int:id>', methods=['PUT'])
@jwt_required()
def atualizar_comanda(id):
    comanda = Comanda.query.get(id)
    if not comanda:
        return jsonify({'erro': 'Comanda nao encontrada.'}), 404

    json_data = request.get_json()
    if not json_data:
        return jsonify({'erro': 'Dados nao fornecidos.'}), 400

    if 'produtos' in json_data:
        novos_produtos = []
        for p in json_data['produtos']:
            produto = None
            if p.get('id'):
                produto = Produto.query.get(p.get('id'))
            if not produto:
                nome = p.get('nome')
                preco = p.get('preco')
                if not nome or preco is None:
                    continue
                produto = Produto(nome=nome, preco=preco)
                db.session.add(produto)
                db.session.flush()
            novos_produtos.append(produto)
        if novos_produtos:
            comanda.produtos = novos_produtos

    db.session.commit()

    return jsonify({
        "idUsuario": comanda.usuario.id,
        "nomeUsuario": comanda.usuario.nome,
        "telefoneUsuario": comanda.usuario.telefone,
        "produtos": [
            {
                "id": produto.id,
                "nome": produto.nome,
                "preco": produto.preco
            } for produto in comanda.produtos
        ]
    }), 200

# REMOVE uma comanda
@comanda_bp.route('/comandas/<int:id>', methods=['DELETE'])
@jwt_required()
def deletar_comanda(id):
    comanda = Comanda.query.get(id)
    if not comanda:
        return jsonify({'erro': 'Comanda nao encontrada.'}), 404
    db.session.delete(comanda)
    db.session.commit()
    return jsonify({"success": {"text": "comanda removida"}}), 200
