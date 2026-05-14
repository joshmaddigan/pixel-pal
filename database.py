from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Pet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    age = db.Column(db.Integer, default=1)
    mood = db.Column(db.String(20), nullable=False)
    hunger = db.Column(db.Integer, default=10)
    happiness = db.Column(db.Integer, default=10)
    energy = db.Column(db.Integer, default=10)
    max_value = db.Column(db.Integer, default=10)
    evo_stage = db.Column(db.String(20), default='Baby')
