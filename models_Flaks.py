from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask import Flask
from flask_cors import CORS
 
app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:123456@localhost:5432/geoODLdb"


db = SQLAlchemy()
db.init_app(app)

# apply changes in the database 
migrate = Migrate(app, db)

# mapp PMultiLinearRegression_Trained table
class BasemapModel(db.Model):
    __tablename__ = 'PMultiLinearRegression_Trained'

    Locality_code = db.Column(db.String(), primary_key=True)
    Locality_name = db.Column(db.String())
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

    def __init__(self, Locality_code, Locality_name,b0,b_Precipitation,b_PrecipitationMinus2,b_Month1,b_Month2,b_Month3,b_Month4,b_Month5,b_Month6,b_Month7,b_Month8,b_Month9,b_Month10,b_Month11,b_Month12, latitude, longitude):
        self.Locality_code = Locality_code
        self.Locality_name = Locality_name
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