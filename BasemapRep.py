
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


engine = db.create_engine('postgresql://postgres:123456@localhost:5432/geoODLdb')
connection = engine.connect()
metadata = db.MetaData()
MultiLinearRegression_Test = db.Table('MultiLinearRegression_Test', metadata, autoload=True, autoload_with=engine)
MultiLinearRegression_Train = db.Table('MultiLinearRegression_Train', metadata, autoload=True, autoload_with=engine)

def SaveBasemap():

    df = pd.read_sql_table( MultiLinearRegression_Test, con=engine)
    df= df.loc[df['Locality_code']== 'DEZ2634'] 
    print(df)
    #filepath_test = Path('/home/raha/Raha/Thesis/Data/MultiLinearRegression_Test.csv')  
    #df.to_csv(filepath_test)

    geo_json = to_geojson(df=df, lat='latitude', lon='longitude',
                 properties=['Locality_code','y_ODL_real'])
    print(geo_json)

    from pandas_geojson import write_geojson
    write_geojson(geo_json, filename='test.geojson', indent=4)

    with open('MultiLinearRegression_Test' + '.json', 'w', encoding='utf-8') as f:
      json.dump(geo_json, f, ensure_ascii=False, indent=4)

SaveBasemap()