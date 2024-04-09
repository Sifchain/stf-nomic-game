from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# set SQLAlchemy to use sqlite database file
SQLALCHEMY_DATABASE_URI = 'sqlite:///app_database.db'

db = SQLAlchemy(engine_options={'url': SQLALCHEMY_DATABASE_URI})

class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    score = db.Column(db.Integer, default=0)
    # Relationship to Game
    game_id = db.Column(db.Integer, db.ForeignKey('game.id'), nullable=True)
    game = db.relationship('Game', back_populates='players')

    def __repr__(self):
        return f'<Player {self.name}>'

class Rule(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.Text, nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    # Relationship to Game
    game_id = db.Column(db.Integer, db.ForeignKey('game.id'), nullable=False)
    game = db.relationship('Game', back_populates='rules')

    def __repr__(self):
        return f'<Rule {self.description[:30]}>...'

class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    state = db.Column(db.JSON, nullable=True)  # This can store a JSON representation of the game state if needed
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    # Relationships
    players = db.relationship('Player', back_populates='game', lazy='dynamic')
    rules = db.relationship('Rule', back_populates='game', lazy='dynamic')

    def __repr__(self):
        return f'<Game {self.id}>'
