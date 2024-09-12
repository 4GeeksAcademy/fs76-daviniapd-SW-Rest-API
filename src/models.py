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
    galactic_location = db.Column(db.String(120), unique=True, nullable=True)
    climate = db.Column(db.String(120), unique=True, nullable=True)
    population = db.Column(db.String(120), unique=True, nullable=True)
    native_species = db.Column(db.String(120), unique=True, nullable=True)
    government  = db.Column(db.String(120), unique=True, nullable=True)

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
            # do not serialize the password, its a security breach
        }

class Characters(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    specie = db.Column(db.String(120), unique=True, nullable=True)
    role = db.Column(db.String(120), unique=True, nullable=True)
    life_status = db.Column(db.String(120), unique=True, nullable=True)
    gender = db.Column(db.String(120), unique=True, nullable=True)
    homeworld_id = db.Column(db.Integer, db.ForeignKey('planets.id'))
    planets = db.relationship(Planets)


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
            # do not serialize the password, its a security breach
        }
        
class Vehicles(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    vehicles_class = db.Column(db.String(120), unique=True, nullable=True)
    manufacturer = db.Column(db.String(120), unique=True, nullable=True)
    autonomy = db.Column(db.String(120), unique=True, nullable=True)
    weapons = db.Column(db.String(120), unique=True, nullable=True)
    passengers  = db.Column(db.String(120), unique=True, nullable=True)

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
            # do not serialize the password, its a security breach
        }