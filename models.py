from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext import mutable
from flask_migrate import Migrate
from flask import Flask,render_template,request
import pandas as pd
 
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:123456@localhost:5432/geoODLdb"


db = SQLAlchemy()

db.init_app(app)
migrate = Migrate(app, db)

class CarsModel(db.Model):
    __tablename__ = 'cars'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    model = db.Column(db.String())
    doors = db.Column(db.Integer())

    def __init__(self, name, model, doors):
        self.name = name
        self.model = model
        self.doors = doors

    def __repr__(self):
        return f"{self.name}:{self.model}"

class ODLModel(db.Model):
    __tablename__ = 'odls'

    ID = db.Column(db.Integer, primary_key=True)
    Locality_code = db.Column(db.String())
    Value = db.Column(db.String())
    Value_e = db.Column(db.String())
    Start_measure = db.Column(db.String())
    End_measure = db.Column(db.String())

    def __init__(self, Locality_code, Value, Value_e, Start_measure, End_measure):
        self.Locality_code = Locality_code
        self.Value = Value
        self.Value_e = Value_e
        self.Start_measure = Start_measure
        self.End_measure = End_measure

    def __repr__(self):
        return f"{self.name}:{self.model}"

class PrecipitationModel(db.Model):
    __tablename__ = 'precipitations'

    id = db.Column(db.Integer, primary_key=True)
    kenn = db.Column(db.Integer)
    value = db.Column(db.String())
    start_measure = db.Column(db.String())
    end_measure = db.Column(db.String())

    def __init__(self, kenn, value, start_measure, end_measure):
        self.kenn = kenn
        self.value = value
        self.start_measure = start_measure
        self.end_measure = end_measure

    def __repr__(self):
        return f"{self.name}:{self.model}"

    
    