# dao/usuario_dao.py
from models.usuario import Usuario
from extensions import db

class UsuarioDAO:
    @staticmethod
    def get_all():
        return Usuario.query.all()

    @staticmethod
    def get_by_id(id):
        return Usuario.query.get(id)

    @staticmethod
    def get_by_nome(nome):
        return Usuario.query.filter_by(nome=nome).first()

    @staticmethod
    def add(usuario):
        db.session.add(usuario)
        db.session.commit()
        return usuario

    @staticmethod
    def delete(usuario):
        db.session.delete(usuario)
        db.session.commit()

    @staticmethod
    def delete_all():
        Usuario.query.delete()
        db.session.commit()
