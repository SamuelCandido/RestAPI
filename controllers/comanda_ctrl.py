from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from services.comanda_service import ComandaService

comanda_bp = Blueprint('comanda_bp', __name__)

#____________________________________________________________________________________________________________________________________#
# Busca todas, retorna comandas + usuaio
@comanda_bp.route('/comandas', methods=['GET'])
def listar_comandas():
    comandas = ComandaService.listar_comandas()
    resultado = [{
        "idUsuario": c.usuario.id,
        "nomeUsuario": c.usuario.nome,
        "telefoneUsuario": c.usuario.telefone
    } for c in comandas]
    return jsonify(resultado), 200

#____________________________________________________________________________________________________________________________________#
# Busca por id, retorna comanda + usuario + produtos
@comanda_bp.route('/comandas/<int:id>', methods=['GET'])
def obter_comanda(id):
    comanda = ComandaService.obter_comanda(id)
    if not comanda:
        return jsonify({'erro': 'Comanda nao encontrada.'}), 404

    return jsonify({
        "idUsuario": comanda.usuario.id,
        "nomeUsuario": comanda.usuario.nome,
        "telefoneUsuario": comanda.usuario.telefone,
        "produtos": [{
            "id": p.id,
            "nome": p.nome,
            "preco": p.preco
        } for p in comanda.produtos]
    }), 200

#____________________________________________________________________________________________________________________________________#
# Cria comanda + produtos 
@comanda_bp.route('/comandas', methods=['POST'])
@jwt_required()
def criar_comanda():
    json_data = request.get_json()
    id_usuario = json_data.get('idUsuario')
    produtos_data = json_data.get('produtos')

    comanda, erro = ComandaService.criar_comanda(id_usuario, produtos_data)
    if erro:
        return jsonify({'erro': erro}), 400

    return jsonify({
        "idUsuario": comanda.usuario.id,
        "nomeUsuario": comanda.usuario.nome,
        "telefoneUsuario": comanda.usuario.telefone,
        "produtos": [{
            "id": p.id,
            "nome": p.nome,
            "preco": p.preco
        } for p in comanda.produtos]
    }), 201

#____________________________________________________________________________________________________________________________________#
# Atualiza
@comanda_bp.route('/comandas/<int:id>', methods=['PUT'])
@jwt_required()
def atualizar_comanda(id):
    json_data = request.get_json()
    produtos_data = json_data.get('produtos')

    comanda, erro = ComandaService.atualizar_comanda(id, produtos_data)
    if erro:
        return jsonify({'erro': erro}), 404

    return jsonify({
        "idUsuario": comanda.usuario.id,
        "nomeUsuario": comanda.usuario.nome,
        "telefoneUsuario": comanda.usuario.telefone,
        "produtos": [{
            "id": p.id,
            "nome": p.nome,
            "preco": p.preco
        } for p in comanda.produtos]
    }), 200

#____________________________________________________________________________________________________________________________________#
# Delete
@comanda_bp.route('/comandas/<int:id>', methods=['DELETE'])
@jwt_required()
def deletar_comanda(id):
    sucesso = ComandaService.deletar_comanda(id)
    if not sucesso:
        return jsonify({'erro': 'Comanda nao encontrada.'}), 404

    return jsonify({"success": {"text": "comanda removida"}}), 200
