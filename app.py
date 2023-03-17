from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask import Flask,render_template,request
from models_Flaks import db,app,CarsModel,ODLModel, PrecipitationModel,BasemapModel
from MultiLinearRegression_Test import MultiLinearRegression_Test
import pandas as pd
import numpy as np
# import urllib library
from urllib.request import urlopen
# importing module
from pandas import *
# import json
import json

# reading CSV file
data = read_csv("/home/raha/Raha/Thesis/Data/currently_active_odl_stations.csv")
 
# converting column data to list
loc_Codes = data['locality_code'].tolist()

'''datajson = WFSURL()
datanorm= pd.json_normalize(datajson,"features")
@app.route("/")
def home():
return datajson'''


@app.route('/cars', methods=['POST', 'GET'])
def handle_cars():
    if request.method == 'POST':
        if request.is_json:
            data = request.get_json()
            new_car = CarsModel(name=data['name'], model=data['model'], doors=data['doors'])
            db.session.add(new_car)
            db.session.commit()
            return {"message": f"car {new_car.name} has been created successfully."}
        else:
            return {"error": "The request payload is not in JSON format"}

    elif request.method == 'GET':
        cars = CarsModel.query.all()
        results = [
            {
                "name": car.name,
                "model": car.model,
                "doors": car.doors
            } for car in cars]
    return {"count": len(results), "cars": results}

if __name__ == '__main__':
    app.run(debug=True)

@app.route('/stations', methods=['GET'])
def Show_basemap():
    if request.method == 'GET':
        basemaps = BasemapModel.query.all()
        results = [
        {
            "type": "Feature",
            "properties": {
                "Locality_code": basemap.Locality_code,
            },
            "geometry": {
                "type": "Point",
                "coordinates": [
                    basemap.longitude,
                    basemap.latitude,
                ]
            }
        } for basemap in basemaps]
    return {"type": "FeatureCollection", "features": results}

if __name__ == '__main__':
    app.run(debug=True)


@app.route('/odls/<locality_code>/7-days', methods=['GET'])
def handle_getallODL(locality_code):
    if request.method == 'GET':
        url = "https://www.imis.bfs.de/ogc/opendata/wfs?typeName=opendata:odlinfo_timeseries_odl_1h&_dc=1665655122146&service=WFS&version=1.1.0&request=GetFeature&outputFormat=application%2Fjson&srsname=EPSG%3A3857&cql_filter=id%20%3D%20%27"+locality_code+"%27%20"

        # store the response of URL
        response = urlopen(url)
        
        # storing the JSON response 
        # from url in data
        data_json = json.loads(response.read())

        #datanorm= pd.json_normalize(data_json,"features") 
        return (data_json)

if __name__ == '__main__':
    app.run(debug=True)

@app.route('/prediction/<locality_code>/', methods=['GET'])
def handle_linearRegressionTest(locality_code):
    if request.method == 'GET':
        # store the response of URL
        response = MultiLinearRegression_Test(locality_code)

        return (response)