# dao/comanda_dao.py
from models.comanda import Comanda
from extensions import db

class ComandaDAO:
    @staticmethod
    def get_all():
        return Comanda.query.all()

    @staticmethod
    def get_by_id(id):
        return Comanda.query.get(id)

    @staticmethod
    def add(comanda):
        db.session.add(comanda)
        db.session.commit()
        return comanda

    @staticmethod
    def update(comanda):
        db.session.merge(comanda)
        db.session.commit()

    @staticmethod
    def delete(comanda):
        db.session.delete(comanda)
        db.session.commit()
