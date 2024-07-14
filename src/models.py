from flask_login import UserMixin, current_user
from src import db


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(50), nullable=False)
    depenses = db.relationship("Depense", backref="user")


class Depense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(50), nullable=False)
    libelle = db.Column(db.String(50), nullable=False)
    montant = db.Column(db.Integer, nullable=False)
    categorie = db.Column(db.String(50), nullable=False)
    user_id = db.Column(
        db.Integer, db.ForeignKey("user.id"), default=lambda: current_user.get_id()
    )
