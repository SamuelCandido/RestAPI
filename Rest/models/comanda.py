# models/comanda.py
from extensions import db

class Comanda(db.Model):
    __tablename__ = 'comandas'
    id = db.Column(db.Integer, primary_key=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    usuario = db.relationship('Usuario')
    produtos = db.relationship('Produto', secondary='comanda_produto')

# FK
comanda_produto = db.Table('comanda_produto',
    db.Column('comanda_id', db.Integer, db.ForeignKey('comandas.id'), primary_key=True),
    db.Column('produto_id', db.Integer, db.ForeignKey('produtos.id'), primary_key=True)
)
