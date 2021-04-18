from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, ForeignKey, Integer, String

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }

class Planets(db.Model):

    id = db.Column(Integer, primary_key=True)
    name = db.Column(String(250), nullable=False)
    rotation = db.Column(Integer, nullable=True)
    climate = db.Column(String(250), nullable=True)
    gravity = db.Column(String(250), nullable=True)
    terrain = db.Column(String(250), nullable=True)
    population = db.Column(Integer, nullable=True)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "rotation": self.rotation,
            "climate" : self.climate,
            "gravity": self.gravity,
            "terrain": self.terrain,
            "population": self.population
        }

    def get_planets():
        all_planets = Planets.query.all()
        all_planets = list(map(lambda x: x.serialize(), all_planets))
        return all_planets

class Characters(db.Model):
    id = db.Column(Integer, primary_key=True)
    name = db.Column(String(250), nullable=False)
    height = db.Column(Integer, nullable=True)
    hair_color = db.Column(String(250), nullable=True)
    skin_color = db.Column(String(250), nullable=True)
    eye_color = db.Column(String(250), nullable=True)
    birth_year = db.Column(String(250), nullable=True)
    gender = db.Column(String(250), nullable=True)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "height": self.height,
            "hair_color": self.hair_color,
            "skin_color": self.skin_color,
            "eye_color": self.eye_color,
            "birth_year": self.birth_year,
            "genderr": self.gender
        }

    def get_characters():
        all_characters = Characters.query.all()
        all_characters = list(map(lambda x: x.serialize(), all_characters))
        return all_characters

class Favorites(db.Model):
    id = db.Column(Integer, primary_key=True)
    user_id = db.Column(Integer, ForeignKey(User.id))
    planet_id = db.Column(Integer, ForeignKey(Planets.id))
    character_id = db.Column(Integer, ForeignKey(Characters.id))
    planets = db.relationship("Planets")
    user = db.relationship("User")
    characters = db.relationship("Characters")