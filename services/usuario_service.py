from werkzeug.security import generate_password_hash
from dao.usuario_dao import UsuarioDAO
from models.usuario import Usuario

class UsuarioService:
#____________________________________________________________________________________________________________________________________#    
    @staticmethod
    def criar_usuario(nome, telefone, senha):
        if not nome or not telefone or not senha:
            return None, 'Nome, telefone e senha são obrigatórios.'

        if UsuarioDAO.get_by_nome(nome):
            return None, 'Nome de usuário já cadastrado.'

        usuario = Usuario(nome=nome, telefone=telefone, senha=generate_password_hash(senha))
        UsuarioDAO.add(usuario)
        return usuario, None

#____________________________________________________________________________________________________________________________________#
    @staticmethod
    def listar_usuarios():
        return UsuarioDAO.get_all()

#____________________________________________________________________________________________________________________________________#
    @staticmethod
    def obter_usuario(id):
        return UsuarioDAO.get_by_id(id)

#____________________________________________________________________________________________________________________________________#
    @staticmethod
    def deletar_usuario(id):
        usuario = UsuarioDAO.get_by_id(id)
        if not usuario:
            return False
        UsuarioDAO.delete(usuario)
        return True

#____________________________________________________________________________________________________________________________________#
    @staticmethod
    def deletar_todos():
        UsuarioDAO.delete_all()
