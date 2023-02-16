
# import urllib library
# importing module
from pandas import *
import pandas as pd
import sqlalchemy as db
from modelURL import ODL, precipitation
from sqlalchemy.orm import Session
from sqlalchemy import select
from pathlib import Path
from pandas_geojson import to_geojson
import json  

def ConverttoGeojson():

    dataCoordinate = read_csv("/home/raha/Raha/Thesis/Data/BaseMap.csv")
    # converting column data to list
    dfCoordinate= pd.DataFrame(dataCoordinate)

    geo_json = to_geojson(df=dfCoordinate, lat='latitude', lon='longitude',
                 properties=['Locality_code'])
    print(geo_json)

    from pandas_geojson import write_geojson
    write_geojson(geo_json, filename='random.geojson', indent=4)

    with open('basemap' + '.json', 'w', encoding='utf-8') as f:
        json.dump(geo_json, f, ensure_ascii=False, indent=4)

    #df_train = pd.read_sql_table( MultiLinearRegression_Train, con=engine)
    #filepath_train = Path('/home/raha/Raha/Thesis/Data/MultiLinearRegression_Train.csv')  
    #df_train.to_csv(filepath_train)

ConverttoGeojson()