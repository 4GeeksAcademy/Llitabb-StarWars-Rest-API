"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, Users, Characters, Planets, Favorites_Characters, Favorites_Planets
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

# USERS
@app.route('/user', methods=['GET'])
def handle_hello():
    all_users = Users.query.all()
    results = list(map(lambda user: user.serialize(), all_users))
    return jsonify(results), 200

@app.route('/user', methods=['POST'])
def create_user():
    data = request.json
    required_fields = ["email", "password"]
    for field in required_fields:
        if field not in data: 
            return "The '" + field + "' cannot be empty", 400
    new_user = Users(email=data['email'], password=data['password'], is_active=data['is_active'])
    db.session.add(new_user)
    db.session.commit()
    return "User created!", 200

@app.route("/user/<int:user_id>", methods=["GET"])
def get_user(user_id):
    user = Users.query.get(user_id)
    return jsonify(user.serialize()), 200

@app.route("/user/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    user = Users.query.get(user_id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'User deleted'}), 200

# CHARACTERS
@app.route('/characters', methods=['GET'])
def get_characters():
    all_characters = Characters.query.all()
    results = list(map(lambda character: character.serialize(), all_characters))
    response_body = {
        "msg": "Leer los personajes "
    }
    return jsonify(results), 200

@app.route('/characters', methods=['POST'])
def create_character():
    data = request.json
    required_fields = ["name", "url"]
    for field in required_fields:
        if field not in data:
            return "The '" + field + "' cannot be empty", 400
    new_character = Characters(**data)
    db.session.add(new_character)
    db.session.commit()
    return "Character created!", 200

@app.route('/characters/<int:character_id>', methods=['GET'])
def get_character(character_id):
    character = Characters.query.get(character_id)
    if character is None:
        return "Character not found", 404
    return jsonify(character.serialize()), 200

@app.route("/characters/<int:character_id>", methods=["DELETE"])
def delete_character(character_id):
    character = Characters.query.get(character_id)
    if character is None:
        return "Character not found", 404
    db.session.delete(character)
    db.session.commit()
    return jsonify({'message': 'Character deleted'}), 200

# PLANETS
@app.route('/planets', methods=['GET'])
def get_planets():
    all_planets = Planets.query.all()
    results = list(map(lambda planet: planet.serialize(), all_planets))
    response_body = {
        "msg": "Leer los planetas "
    }
    return jsonify(results), 200

@app.route('/planets', methods=['POST'])
def create_planet():
    data = request.json
    required_fields = ["name", "url"]
    for field in required_fields:
        if field not in data:
            return "The '" + field + "' cannot be empty", 400
    new_planet = Planets(**data)
    db.session.add(new_planet)
    db.session.commit()
    return "Planet created!", 200

@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_planet(planet_id):
    planet = Planets.query.get(planet_id)
    if planet is None:
        return "Planet not found", 404
    return jsonify(planet.serialize()), 200

@app.route("/planets/<int:planet_id>", methods=["DELETE"])
def delete_planet(planet_id):
    planet = Planets.query.get(planet_id)
    if planet is None:
        return "Planet not found", 404
    db.session.delete(planet)
    db.session.commit()
    return jsonify({'message': 'Planet deleted'}), 200

# FAVORITE CHARACTERS
@app.route('/user/<int:user_id>/favorite_characters', methods=['GET'])
def get_favorite_characters(user_id):
    user = Users.query.get(user_id)
    if user is None:
        return "User not found", 404
    favorite_characters = [fav_char.serialize() for fav_char in Favorites_Characters.query.filter_by(user_id=user_id).all()]
    return jsonify(favorite_characters), 200

@app.route('/user/<int:user_id>/favorite_characters', methods=['POST'])
def add_favorite_character(user_id):
    data = request.json
    required_fields = ["character_id"]
    for field in required_fields:
        if field not in data:
            return "The '" + field + "' cannot be empty", 400
    user = Users.query.get(user_id)
    if user is None:
        return "User not found", 404
    favorite_character = Favorites_Characters(user_id=user_id, character_id=data["character_id"])
    db.session.add(favorite_character)
    db.session.commit()
    return "Favorite character added!", 200

@app.route('/user/<int:user_id>/favorite_characters/<int:favorite_id>', methods=['DELETE'])
def delete_favorite_character(user_id, favorite_id):
    user = Users.query.get(user_id)
    if user is None:
        return "User not found", 404
    favorite_character = Favorites_Characters.query.filter_by(id=favorite_id, user_id=user_id).first()
    if favorite_character is None:
        return "Favorite character not found", 404
    db.session.delete(favorite_character)
    db.session.commit()
    return "Favorite character deleted!", 200

# FAVORITE PLANETS
@app.route('/user/<int:user_id>/favorite_planets', methods=['GET'])
def get_favorite_planets(user_id):
    user = Users.query.get(user_id)
    if user is None:
        return "User not found", 404
    favorite_planets = [fav_planet.serialize() for fav_planet in Favorites_Planets.query.filter_by(user_id=user_id).all()]
    return jsonify(favorite_planets), 200

@app.route('/user/<int:user_id>/favorite_planets', methods=['POST'])
def add_favorite_planet(user_id):
    data = request.json
    required_fields = ["planet_id"]
    for field in required_fields:
        if field not in data:
            return "The '" + field + "' cannot be empty", 400
    user = Users.query.get(user_id)
    if user is None:
        return "User not found", 404
    favorite_planet = Favorites_Planets(user_id=user_id, planet_id=data["planet_id"])
    db.session.add(favorite_planet)
    db.session.commit()
    return "Favorite planet added!", 200

@app.route('/user/<int:user_id>/favorite_planets/<int:favorite_id>', methods=['DELETE'])
def delete_favorite_planet(user_id, favorite_id):
    user = Users.query.get(user_id)
    if user is None:
        return "User not found", 404
    favorite_planet = Favorites_Planets.query.filter_by(id=favorite_id, user_id=user_id).first()
    if favorite_planet is None:
        return "Favorite planet not found", 404
    db.session.delete(favorite_planet)
    db.session.commit()
    return "Favorite planet deleted!", 200

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
