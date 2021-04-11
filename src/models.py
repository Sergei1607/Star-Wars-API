from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, ForeignKey, Integer, String

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }

class Planets(db.Model):

    id = db.Column(Integer, primary_key=True)
    name = db.Column(String(250), nullable=False)
    rotation_period = db.Column(Integer, nullable=True)
    orbital_period = db.Column(Integer, nullable=True)
    diameter = db.Column(Integer, nullable=True)
    climate = db.Column(String(250), nullable=True)
    gravity = db.Column(String(250), nullable=True)
    terrain = db.Column(String(250), nullable=True)
    surface_water = db.Column(Integer, nullable=True)
    population = db.Column(Integer, nullable=True)

class Characters(db.Model):
    id = db.Column(Integer, primary_key=True)
    name = db.Column(String(250), nullable=False)
    height = db.Column(Integer, nullable=True)
    mass = db.Column(Integer, nullable=True)
    hair_color = db.Column(String(250), nullable=True)
    skin_color = db.Column(String(250), nullable=True)
    eye_color = db.Column(String(250), nullable=True)
    birth_year = db.Column(Integer, nullable=True)
    gender = db.Column(String(250), nullable=True)

class Favorites(db.Model):
    id = db.Column(Integer, primary_key=True)
    usuario_id = db.Column(Integer, ForeignKey(User.id))
    planeta_id = db.Column(Integer, ForeignKey(Planets.id))
    personaje_id = db.Column(Integer, ForeignKey(Characters.id))