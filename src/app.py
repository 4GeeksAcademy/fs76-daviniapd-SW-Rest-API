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
    user = Users.query.filter_by(id=user_id).first()
    if user is None:
        return jsonify({"msg": "User not found"}), 404

    favorite_characters = Favorite_Character.query.filter_by(users_id=user_id).all()
    favorite_planets = Favorite_Planet.query.filter_by(users_id=user_id).all()
    favorite_vehicles = Favorite_Vehicle.query.filter_by(users_id=user_id).all()

    favorite_characters_data = []
    for favorite_character in favorite_characters:
        character = Characters.query.filter_by(id=favorite_character.characters_id).first()
        favorite_characters_data.append(character.serialize())

    favorite_planets_data = []
    for favorite_planet in favorite_planets:
        planet = Planets.query.filter_by(id=favorite_planet.planets_id).first()
        favorite_planets_data.append(planet.serialize())

    favorite_vehicles_data = []
    for favorite_vehicle in favorite_vehicles:
        vehicle = Vehicles.query.filter_by(id=favorite_vehicle.vehicles_id).first()
        favorite_vehicles_data.append(vehicle.serialize())

    return jsonify({
        "characters": favorite_characters_data,
        "planets": favorite_planets_data,
        "vehicles": favorite_vehicles_data
    }), 200



# @app.route('/users', methods=['POST'])
# def add_user():
#     body = request.get_json()
#     required_fields = ['username', 'firstname', 'lastname', 'email']
    
#     for field in required_fields:
#         if field not in body:
#             return jsonify(f'ERROR: You must return a {field}'), 400
#         elif body[field] == '':
#             return jsonify(f"ERROR: {field} can't be empty"), 400
             
#     user = Users(username = body['username'], firstname = body['firstname'], lastname = body['lastname'], email = body['email'])
#     db.session.add(user)
#     db.session.commit()
    
#     return jsonify(user.serialize()), 200


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
