from . import db
from flask_login import UserMixin
from sqlalchemy.orm import validates

# Tabela asocjacyjna między UserProfile a Collection
user_collections = db.Table('user_collections',
    db.Column('profile_id', db.Integer, db.ForeignKey('user_profile.id'), primary_key=True),
    db.Column('collection_id', db.Integer, db.ForeignKey('collection.id'), primary_key=True)
)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    profile = db.relationship('UserProfile', backref='user', uselist=False)

class UserProfile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), unique=True, nullable=False)
    collections = db.relationship('Collection', secondary=user_collections, backref='profiles')
    user_cards = db.relationship('UserCard', backref='profile', lazy=True)

class Collection(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), unique=True, nullable=False)
    cards = db.relationship('Card', backref='collection', lazy=True)

    def __repr__(self):
        return f'<Collection {self.name}>'

class Card(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    identifier = db.Column(db.String(50), unique=True, nullable=False)
    name = db.Column(db.String(150), nullable=False)
    rarity = db.Column(db.String(50), nullable=False)
    collection_id = db.Column(db.Integer, db.ForeignKey('collection.id'), nullable=False)

    def __repr__(self):
        return f'<Card {self.name}>'

class UserCard(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    profile_id = db.Column(db.Integer, db.ForeignKey('user_profile.id'), nullable=False)
    card_id = db.Column(db.Integer, db.ForeignKey('card.id'), nullable=False)
    quantity = db.Column(db.Integer, default=0, nullable=False)

    card = db.relationship('Card', backref='user_cards', lazy=True)

    @validates('quantity')
    def validate_quantity(self, key, value):
        if value < 0:
            raise ValueError('Ilość nie może być poniżej 0')
        return value

    def __repr__(self):
        return f'<UserCard {self.profile.user.username} - {self.card.name}>'
