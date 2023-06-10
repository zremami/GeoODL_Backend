
# import urllib library
# importing module
from pandas import *
import pandas as pd
import sqlalchemy as db

engine = db.create_engine('postgresql://postgres:123456@localhost:5432/geoODLdb')
connection = engine.connect()
metadata = db.MetaData()
odl_precipitations = db.Table('odls_precipitations', metadata, autoload=True, autoload_with=engine)


def getAllOdl_precipitations():
    #query = db.select([odls]) 
    
    #ResultProxy = connection.execute(query)
    #ResultSet = ResultProxy.fetchall()
    df = table_df = pd.read_sql_table( odl_precipitations, con=engine)
    print(df.sum())

getAllOdl_precipitations()