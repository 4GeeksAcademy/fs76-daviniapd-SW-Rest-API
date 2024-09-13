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
from models import db, Users, Planets, Characters, Vehicles, Favorite_Planet, Favorite_Character, Favorite_Vehicle
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

@app.route('/users', methods=['GET'])
def get_users():
    all_users = Users.query.all()
    results = list(map(lambda user: user.serialize(), all_users))

    return jsonify(results), 200

@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = Users.query.filter_by(id=user_id).first()

    return jsonify(user.serialize()), 200

@app.route('/planets', methods=['GET'])
def get_planets():
    all_planets = Planets.query.all()
    results = list(map(lambda planet: planet.serialize(), all_planets))

    return jsonify(results), 200

@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_planet(planet_id):
    planet = Planets.query.filter_by(id=planet_id).first()

    return jsonify(planet.serialize()), 200

@app.route('/characters', methods=['GET'])
def get_characters():
    all_characters = Characters.query.all()
    results = list(map(lambda character: character.serialize(), all_characters))

    return jsonify(results), 200

@app.route('/characters/<int:character_id>', methods=['GET'])
def get_character(character_id):
    character = Characters.query.filter_by(id=character_id).first()

    return jsonify(character.serialize()), 200

@app.route('/vehicles', methods=['GET'])
def get_vehicles():
    all_vehicles = Vehicles.query.all()
    results = list(map(lambda vehicle: vehicle.serialize(), all_vehicles))

    return jsonify(results), 200

@app.route('/vehicles/<int:vehicle_id>', methods=['GET'])
def get_vehicle(vehicle_id):
    vehicle = Vehicles.query.filter_by(id=vehicle_id).first()

    return jsonify(vehicle.serialize()), 200

@app.route('/users/<int:user_id>/favorites', methods=['GET'])
def get_user_favorites(user_id):
    
    #Para confirmar que el usuario que buscas existe
    user = Users.query.filter_by(id=user_id).first()
    if user is None:
        return jsonify("ERROR: User not found"), 400

    favorite_characters = Favorite_Character.query.filter_by(user_id=user_id).all()
    favorite_planets = Favorite_Planet.query.filter_by(user_id=user_id).all()
    favorite_vehicles = Favorite_Vehicle.query.filter_by(user_id=user_id).all()

    favorite_characters_data = []
    for favorite_character in favorite_characters:
        character = Characters.query.filter_by(id=favorite_character.character_id).first()
        favorite_characters_data.append(character.serialize())

    favorite_planets_data = []
    for favorite_planet in favorite_planets:
        planet = Planets.query.filter_by(id=favorite_planet.planet_id).first()
        favorite_planets_data.append(planet.serialize())

    favorite_vehicles_data = []
    for favorite_vehicle in favorite_vehicles:
        vehicle = Vehicles.query.filter_by(id=favorite_vehicle.vehicle_id).first()
        favorite_vehicles_data.append(vehicle.serialize())

    return jsonify({
        "characters": favorite_characters_data,
        "planets": favorite_planets_data,
        "vehicles": favorite_vehicles_data
    }), 200



@app.route('/favorites/planets', methods=['POST'])
def add_favorite_planet():
    request_body = request.get_json()

    #Para que no se introduzca el id de un usuario que exista             
    user = Users.query.get(request_body["user_id"])
    if user is None:
        return jsonify("ERROR: user_id not exist"), 400

    #Para que no se introduzca el id de un planeta que exista
    planet = Planets.query.get(request_body["planet_id"])
    if planet is None:
        return jsonify("ERROR: planet_id not exist"), 400
    
    #Para no duplicar favoritos de un mismo usuario
    existing_favorite = Favorite_Planet.query.filter_by(user_id=request_body["user_id"], planet_id=request_body["planet_id"]).first()
    if existing_favorite:
        return jsonify("ERROR: favorite planet already exists for this user"), 400

    new_favorite = Favorite_Planet(
        user_id=request_body["user_id"],
        planet_id=request_body["planet_id"],
        #Para que se muestre una descripcion de quien le dio like a qué y no solo sean ids
        description=f"{user.username} likes {planet.name}"
    )

    db.session.add(new_favorite)
    db.session.commit()

    return jsonify(new_favorite.serialize()), 200

@app.route('/favorites/characters', methods=['POST'])
def add_favorite_character():
    request_body = request.get_json()
             
    user = Users.query.get(request_body["user_id"])
    if user is None:
        return jsonify("ERROR: user_id not exist"), 400

    character = Characters.query.get(request_body["character_id"])
    if character is None:
        return jsonify("ERROR: character_id not exist"), 400
    
    existing_favorite = Favorite_Character.query.filter_by(user_id=request_body["user_id"], character_id=request_body["character_id"]).first()
    if existing_favorite:
        return jsonify("ERROR: favorite character already exists for this user"), 400

    new_favorite = Favorite_Character(
        user_id=request_body["user_id"],
        character_id=request_body["character_id"],
        description=f"{user.username} likes {character.name}"
    )

    db.session.add(new_favorite)
    db.session.commit()

    return jsonify(new_favorite.serialize()), 200

@app.route('/favorites/vehicles', methods=['POST'])
def add_favorite_vehicle():
    request_body = request.get_json()
             
    user = Users.query.get(request_body["user_id"])
    if user is None:
        return jsonify("ERROR: user_id not exist"), 400

    vehicle = Vehicles.query.get(request_body["vehicle_id"])
    if vehicle is None:
        return jsonify("ERROR: vehicle_id not exist"), 400
    
    existing_favorite = Favorite_Vehicle.query.filter_by(user_id=request_body["user_id"], vehicle_id=request_body["vehicle_id"]).first()
    if existing_favorite:
        return jsonify("ERROR: favorite vehicle already exists for this user"), 400

    new_favorite = Favorite_Vehicle(
        user_id=request_body["user_id"],
        vehicle_id=request_body["vehicle_id"],
        description=f"{user.username} likes {vehicle.name}"
    )

    db.session.add(new_favorite)
    db.session.commit()

    return jsonify(new_favorite.serialize()), 200

@app.route('/favorites/planets/<int:favorite_planet_id>', methods=['DELETE'])
def delete_favorite_planet(favorite_planet_id):
    
    #Para confirmar que existe el id que se quiere eliminar
    favorite_planet = Favorite_Planet.query.filter_by(id=favorite_planet_id).first()
    if favorite_planet is None:
        return jsonify("ERROR: Favorite planet not found"), 400

    db.session.delete(favorite_planet)
    db.session.commit()

    return jsonify(favorite_planet.serialize()), 200

@app.route('/favorites/characters/<int:favorite_character_id>', methods=['DELETE'])
def delete_favorite_character(favorite_character_id):
    
    favorite_character = Favorite_Character.query.filter_by(id=favorite_character_id).first()
    if favorite_character is None:
        return jsonify("ERROR: Favorite character not found"), 400

    db.session.delete(favorite_character)
    db.session.commit()

    return jsonify(favorite_character.serialize()), 200

@app.route('/favorites/vehicles/<int:favorite_vehicle_id>', methods=['DELETE'])
def delete_favorite_vehicle(favorite_vehicle_id):
    
    favorite_vehicle = Favorite_Vehicle.query.filter_by(id=favorite_vehicle_id).first()
    if favorite_vehicle is None:
        return jsonify("ERROR: Favorite vehicle not found"), 400

    db.session.delete(favorite_vehicle)
    db.session.commit()

    return jsonify(favorite_vehicle.serialize()), 200


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
