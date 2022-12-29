from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask import Flask,render_template,request
from models import db,app,CarsModel,ODLModel, PrecipitationModel
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

@app.route('/showallODL', methods=['GET'])
def Show_allODLs():
    if request.method == 'GET':
        odls = ODLModel.query.all()
        results = [
            {
                "kenn":odl.kenn,
                "value": odl.value,
                "start_measure": odl.start_measure,
                "end_measure": odl.end_measure,
            } for odl in odls]
    return {"count": len(results), "odls": results}

if __name__ == '__main__':
    app.run(debug=True)


@app.route('/getallODL', methods=['GET'])
def handle_getallODL():
    if request.method == 'GET':
        for id in loc_Codes:
            url = "https://entw-imis.lab.bfs.de/ogc/opendata/wfs?typeName=opendata:public_odl_brutto_1h&_dc=1665655122146&service=WFS&version=1.1.0&request=GetFeature&outputFormat=application%2Fjson&srsname=EPSG%3A3857&cql_filter=id%20%3D%20%27"+id+"%27%20AND%20end_measure%3E%272021-01-01T00%3A00%3A00.000Z%27%20AND%20end_measure%3C%272022-12-28T00%3A00%3A00.000Z%27"

            # store the response of URL
            response = urlopen(url)
            
            # storing the JSON response 
            # from url in data
            data_json = json.loads(response.read())

            datanorm= pd.json_normalize(data_json,"features")
            for index in range(len(datanorm)):
                new_ODL = ODLModel(
                    Locality_code=datanorm['properties.id'][index], 
                    Value=datanorm['properties.value'][index],
                    Value_e=datanorm['properties.value'][index],
                    Start_measure=datanorm['properties.start'][index],
                    End_measure=datanorm['properties.end_measure'][index]
                    )
                db.session.add(new_ODL)
                db.session.commit()   
        return ("count")

if __name__ == '__main__':
    app.run(debug=True)

@app.route('/getallPrecipitation', methods=['GET'])
def handle_getallPrecipitation():
    if request.method == 'GET':
        for index in range(len(datanorm)):
            new_precipitation = PrecipitationModel(
                kenn=np.array(datanorm['properties.kenn']).tolist()[index], 
                value=np.array(datanorm['properties.value']).tolist()[index],
                start_measure=np.array(datanorm['properties.start_measure']).tolist()[index],
                end_measure=np.array(datanorm['properties.end_measure']).tolist()[index]
                )
            db.session.add(new_precipitation)
        db.session.commit()       
    return ("count")

if __name__ == '__main__':
    app.run(debug=True)