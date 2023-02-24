from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext import mutable
from flask_migrate import Migrate
from flask import Flask,render_template,request
import pandas as pd
from sqlalchemy import Table, Column, Integer, String, Float
from flask_cors import CORS
 
app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:123456@localhost:5432/geoODLdb"


db = SQLAlchemy()

db.init_app(app)
migrate = Migrate(app, db)


class BasemapModel(db.Model):
    __tablename__ = 'MultiLinearRegression_Train'

    Locality_code = db.Column(db.String(), primary_key=True)
    R_squared = db.Column(db.Float())
    R_squared_adjusted = db.Column(db.Float())
    b0 = db.Column(db.Float())
    b_Precipitation = db.Column(db.Float())
    b_PrecipitationMinus2 = db.Column(db.Float())
    b_Month1 = db.Column(db.Float())
    b_Month2 = db.Column(db.Float())
    b_Month3 = db.Column(db.Float())
    b_Month4 = db.Column(db.Float())
    b_Month5 = db.Column(db.Float())
    b_Month6 = db.Column(db.Float())
    b_Month7 = db.Column(db.Float())
    b_Month8 = db.Column(db.Float())
    b_Month9 = db.Column(db.Float())
    b_Month10 = db.Column(db.Float())
    b_Month11 = db.Column(db.Float())
    b_Month12 = db.Column(db.Float())
    latitude = db.Column(db.Float())
    longitude = db.Column(db.Float())

    def __init__(self, Locality_code,R_squared,R_squared_adjusted,b0,b_Precipitation,b_PrecipitationMinus2,b_Month1,b_Month2,b_Month3,b_Month4,b_Month5,b_Month6,b_Month7,b_Month8,b_Month9,b_Month10,b_Month11,b_Month12, latitude, longitude):
        self.Locality_code = Locality_code
        self.R_squared =R_squared
        self.R_squared_adjusted = R_squared_adjusted
        self.b0 = b0
        self.b_Precipitation = b_Precipitation
        self.b_PrecipitationMinus2 = b_PrecipitationMinus2
        self.b_Month1 = b_Month1
        self.b_Month2 = b_Month2
        self.b_Month3 = b_Month3
        self.b_Month4 = b_Month4
        self.b_Month5 = b_Month5
        self.b_Month6 = b_Month6
        self.b_Month7 = b_Month7
        self.b_Month8 = b_Month8
        self.b_Month9 = b_Month9
        self.b_Month10 = b_Month10
        self.b_Month11 = b_Month11
        self.b_Month12 = b_Month12
        self.latitude = latitude
        self.longitude = longitude
    def __repr__(self):
        return f"{self.name}:{self.model}"

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

    
    