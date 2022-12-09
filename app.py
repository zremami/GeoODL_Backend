from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask import Flask,render_template,request
from models import db,app,CarsModel,ODLModel, PrecipitationModel
from WFSRepository import getWFSData
import pandas as pd
import numpy as np

datajson=getWFSData()
datanorm= pd.json_normalize(datajson,"features")

@app.route("/")
def home():

    return datajson


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
        for index in range(len(datanorm)):
            new_ODL = ODLModel(
                kenn=datanorm['properties.kenn'][index], 
                value=datanorm['properties.value'][index],
                start_measure=datanorm['properties.start_measure'][index],
                end_measure=datanorm['properties.end_measure'][index]
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