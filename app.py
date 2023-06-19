from flask import request
from models_Flaks import app,BasemapModel
from MultiLinearRegression_Prediction import MultiLinearRegression_Prediction


#HTTPRequest1, return the information for map
@app.route('/stations', methods=['GET'])
def Show_basemap():
    if request.method == 'GET':
        basemaps = BasemapModel.query.all()
        results = [
        {
            "type": "Feature",
            "properties": {
                "Locality_code": basemap.Locality_code,
                "Locality_name": basemap.Locality_name,
                "Geometry": [basemap.latitude, basemap.longitude],
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

#HTTPRequest2: return information for visualizaton
@app.route('/prediction/<locality_code>/<started>/<ended>/<effect>/<effect2>', methods=['GET'])
def handle_linearRegressionTest(locality_code, started, ended, effect, effect2):
    if request.method == 'GET':
        response = MultiLinearRegression_Prediction(locality_code, started, ended, effect, effect2)

        return (response)
if __name__ == '__main__':
    app.run(debug=True)