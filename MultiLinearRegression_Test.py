from pandas import *
from DataFrameRep import JSPRMLModel
import pandas as pd
import numpy as np
import sklearn 
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error as mae
import random
import matplotlib.pyplot as plt
from scipy import stats
import statsmodels.api as sm
from sklearn import linear_model
import pandas as pd
import sqlalchemy as db
from modelURL import ODL, precipitation
from sqlalchemy.orm import Session
from sqlalchemy import select
from WFSRepositoryLates7days import getOdl_1h,getPrecipitation_15min
from DataFrameRepLates7days import DataFramelastes7daysModel
from pathlib import Path
import json   

def MultiLinearRegression_Test(locality_code):

    engine = db.create_engine('postgresql://postgres:123456@localhost:5432/geoODLdb')
    connection = engine.connect()
    metadata = db.MetaData()
    MultiLinearRegression_Train = db.Table('MultiLinearRegression_Train', metadata, autoload=True, autoload_with=engine)

    table_df = pd.read_sql_table( MultiLinearRegression_Train, con=engine)

    data = read_csv("/home/raha/Raha/Thesis/Data/currently_active_odl_stations_selection.csv")
    # converting column data to list
    df= pd.DataFrame(table_df)
    loc_Codes = data['locality_code'].tolist()

    df_M= df.loc[df['Locality_code']== locality_code]

    data_json1=getOdl_1h(locality_code)
    datanorm1= pd.json_normalize(data_json1,"features")
    df1 = pd.DataFrame(datanorm1)
    if df1.empty:
        return 0

    df1 = df1[['properties.id','properties.start_measure','properties.end_measure','properties.value']]
    df1.columns = ['Locality_code', 'Start_measure','End_measure','Value']
    #print(df1.info())
    data_json2=getPrecipitation_15min(locality_code)
    datanorm2= pd.json_normalize(data_json2,"features")
    df2 = pd.DataFrame(datanorm2)

    if df2.empty:
        return 0

    df2 = df2[['properties.id','properties.start_measure','properties.end_measure','properties.value']]
    df2.columns = ['Locality_code', 'Start_measure','End_measure','Value']
    #print(df2.info())

    df_7days = DataFramelastes7daysModel(df1,df2)
    #print(df_7days.head())

    df7_dummies = pd.get_dummies(df_7days,columns=['Month'])


    y_prediction=[]
    y_real=[]
    #mae = []
    y_prediction=[]

    for index in range(len(df_7days)):
        y_prediction.append((df_M['b0'])+(df7_dummies['Value_precipitation'][index])*df_M['b_Precipitation'] + (df7_dummies['Value_precipitationMinus2'][index])*df_M['b_PrecipitationMinus2'] + (df7_dummies['Month_2'][index])*df_M['b_Month2'])

    y_prediction=np.array(y_prediction)
    y_real = np.array(df7_dummies['Value_odl'])
    meanAE = mae(y_real,y_prediction)
    #print(meanAE)
    df_final = pd.DataFrame()
    df_final['Locality_code']= np.array(df7_dummies['Locality_code'])
    df_final['Start_measure']= df7_dummies.index
    df_final['precipitation'] = np.array(df_7days['Value_precipitation'])
    df_final['y_ODL_real'] = y_real
    df_final['y_ODL_prediction'] = y_prediction
    df_final['mean absolute error']= meanAE

    #pssql_table = "MultiLinearRegression_Test"
    #df_final.to_sql(name=pssql_table, con=connection, if_exists='append',index=False)
    result = df_final.to_json(orient="records")
    jsonResult = json.loads(result)

    return jsonResult