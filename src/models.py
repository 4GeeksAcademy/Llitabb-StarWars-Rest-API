from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Users(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    lastname = db.Column(db.String(250), nullable=False)
    email = db.Column(db.String(120), nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "lastname": self.lastname,
            "email": self.email
        }

class Planets(db.Model):
    __tablename__ = 'planet'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    terrain = db.Column(db.String(250), nullable=False)
    climate = db.Column(db.String(250), nullable=False)
    population = db.Column(db.String(250), nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "terrain": self.terrain,
            "climate": self.climate,
            "population": self.population
        }

class Characters(db.Model):
    __tablename__ = 'character'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    height = db.Column(db.String(250), nullable=False)
    mass = db.Column(db.String(250), nullable=False)
    haircolor = db.Column(db.String(250), nullable=False)
    skincolor = db.Column(db.String(250), nullable=False)
    planet_id = db.Column(db.Integer, db.ForeignKey('planet.id'))
    planet = db.relationship(Planets)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "height": self.height,
            "mass": self.mass,
            "haircolor": self.haircolor,
            "skincolor": self.skincolor,
            "planet_id": self.planet_id
        }

class Favorites_Characters(db.Model):
    __tablename__ = 'favorite_character'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship(Users)
    character_id = db.Column(db.Integer, db.ForeignKey('character.id'))
    character = db.relationship(Characters)

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "character_id": self.character_id
        }

class Favorites_Planets(db.Model):
    __tablename__ = 'favorite_planet'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship(Users)
    planet_id = db.Column(db.Integer, db.ForeignKey('planet.id'))
    planet = db.relationship(Planets)

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "planet_id": self.planet_id
        }
