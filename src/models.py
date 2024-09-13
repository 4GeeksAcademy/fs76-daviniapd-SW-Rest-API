from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    firstname = db.Column(db.String(120), unique=False, nullable=False)
    lastname = db.Column(db.String(120), unique=False, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)
    db.relationship('Favorite_Planet', backref='users', lazy=True)
    db.relationship('Favorite_Character', backref='users', lazy=True)
    db.relationship('Favorite_Vehicle', backref='users', lazy=True)

    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "firstname": self.firstname,
            "lastname": self.lastname,
            "email": self.email,
            "is_active": self.is_active,
            # do not serialize the password, its a security breach
        }
    
class Planets(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    galactic_location = db.Column(db.String(120), nullable=True)
    climate = db.Column(db.String(120), nullable=True)
    population = db.Column(db.String(120), nullable=True)
    native_species = db.Column(db.String(120), nullable=True)
    government  = db.Column(db.String(120), nullable=True)
    db.relationship('Characters', backref='planets', lazy=True)
    db.relationship('Favorite_Planet', backref='planets', lazy=True)

    def __repr__(self):
        return '<Planet %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "galactic_location": self.galactic_location,
            "climate": self.climate,
            "population": self.population,
            "native_species": self.native_species,
            "government": self.government,            
        }


class Characters(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    specie = db.Column(db.String(120), nullable=True)
    role = db.Column(db.String(120), nullable=True)
    life_status = db.Column(db.String(120), nullable=True)
    gender = db.Column(db.String(120), nullable=True)
    homeworld_id = db.Column(db.Integer, db.ForeignKey('planets.id'))
    planets = db.relationship(Planets)
    db.relationship('Favorite_Character', backref='characters', lazy=True)

    def __repr__(self):
        return '<Character %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "specie": self.specie,
            "role": self.role,
            "life_status": self.life_status,
            "gender": self.gender,
            "homeworld_id": self.homeworld_id,            
        }
        
        
class Vehicles(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    vehicles_class = db.Column(db.String(120), nullable=True)
    manufacturer = db.Column(db.String(120), nullable=True)
    autonomy = db.Column(db.String(120), nullable=True)
    weapons = db.Column(db.String(120), nullable=True)
    passengers  = db.Column(db.String(120), nullable=True)
    db.relationship('Favorite_Vehicle', backref='vehicles', lazy=True)

    def __repr__(self):
        return '<Vehicle %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "vehicles_class": self.vehicles_class,
            "manufacturer": self.manufacturer,
            "autonomy": self.autonomy,
            "weapons": self.weapons,
            "passengers": self.passengers,            
        }
        
        
class Favorite_Planet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    planet_id = db.Column(db.Integer, db.ForeignKey('planets.id'), nullable=False)
    description = db.Column(db.String(200), nullable=True)
    
    def __repr__(self):
        return '<Favorite_Planet %r>' % self.name

    def serialize(self):
        #Para traerme los datos del user y del planet por el id y asi poder poner una descripción dinámica
        user = Users.query.get(self.user_id)
        planet = Planets.query.get(self.planet_id)
        self.description = f"{user.username} likes {planet.name}"
        return {
            "id": self.id,
            "user_id": self.user_id,
            "planet_id": self.planet_id,
            "description": self.description
        }
    
    
class Favorite_Character(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    character_id = db.Column(db.Integer, db.ForeignKey('characters.id'), nullable=False)
    description = db.Column(db.String(200), nullable=True)
    
    def __repr__(self):
        return '<Favorite_Character %r>' % self.name

    def serialize(self):
        user = Users.query.get(self.user_id)
        character = Characters.query.get(self.character_id)
        self.description = f"{user.username} likes {character.name}"
        
        return {
            "id": self.id,
            "user_id": self.user_id,  
            "character_id": self.character_id, 
            "description": self.description      
        }
    
    
class Favorite_Vehicle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicles.id'), nullable=False)
    description = db.Column(db.String(200), nullable=True)
    
    def __repr__(self):
        return '<Favorite_Vehicle %r>' % self.name

    def serialize(self):
        user = Users.query.get(self.user_id)
        vehicle = Vehicles.query.get(self.vehicle_id)
        self.description = f"{user.username} likes {vehicle.name}"
        
        return {
            "id": self.id,
            "user_id": self.user_id,  
            "vehicle_id": self.vehicle_id,
            "description": self.description   
        }
    
    
    
# class Favorites(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     users_id = db.Column(db.Integer, db.ForeignKey('users.id'))
#     users = db.relationship(Users)
#     planets_id = db.Column(db.Integer, db.ForeignKey('planets.id'))
#     planets = db.relationship(Planets)
#     characters_id = db.Column(db.Integer, db.ForeignKey('characters.id'))
#     characters = db.relationship(Characters)
#     vehicles_id = db.Column(db.Integer, db.ForeignKey('vehicles.id'))
#     vehicles = db.relationship(Vehicles)


#     def __repr__(self):
#         return '<Favorite %r>' % self.name

#     def serialize(self):
#         return {
#             "id": self.id,
#             "user_id": self.users_id,  
#             "planets_id": self.planets_id,  
#             "characters_id": self.characters_id,   
#             "vehicles_id": self.vehicles_id,           
#         }