from models.usuario import Usuario
from models.produto import Produto
from models.comanda import Comanda
from extensions import db
from dao.comanda_dao import ComandaDAO

class ComandaService:
#____________________________________________________________________________________________________________________________________#
# Busca todas, retorna comandas + usuaio
    @staticmethod
    def listar_comandas():
        return ComandaDAO.get_all()
#____________________________________________________________________________________________________________________________________#
# Busca por id, retorna comanda + usuario + produtos
    @staticmethod
    def obter_comanda(id):
        return ComandaDAO.get_by_id(id)

#____________________________________________________________________________________________________________________________________#
# Cria comanda + produtos 
    @staticmethod
    def criar_comanda(id_usuario, produtos_data):
        if not id_usuario:
            return None, 'idUsuario é obrigatório.'

        usuario = Usuario.query.get(id_usuario)
        if not usuario:
            return None, 'Usuario não encontrado.'

        if not produtos_data or not isinstance(produtos_data, list):
            return None, 'produtos é obrigatório.'

        produtos = []
        for p in produtos_data:
            produto = None
            if p.get('id'):
                produto = Produto.query.get(p['id'])

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
            return None, 'Produtos inválidos.'

        comanda = Comanda(usuario=usuario, produtos=produtos)
        ComandaDAO.add(comanda)
        return comanda, None

#____________________________________________________________________________________________________________________________________#
# Atualiza
    @staticmethod
    def atualizar_comanda(id, produtos_data):
        comanda = ComandaDAO.get_by_id(id)
        if not comanda:
            return None, 'Comanda nao encontrada.'

        novos_produtos = []
        for p in produtos_data:
            produto = None
            if p.get('id'):
                produto = Produto.query.get(p['id'])

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
            comanda.produtos.extend([p for p in novos_produtos if p not in comanda.produtos])

        ComandaDAO.update(comanda)
        return comanda, None

#____________________________________________________________________________________________________________________________________#
# Delete
    @staticmethod
    def deletar_comanda(id):
        comanda = ComandaDAO.get_by_id(id)
        if not comanda:
            return False
        ComandaDAO.delete(comanda)
        return True
