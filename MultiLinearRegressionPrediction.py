from pandas import *
def MultiLinearRegressionPrediction():
    from DataFrameRepFly import JSPRMLModel
    import pandas as pd
    import numpy as np
    import sklearn 
    from sklearn.linear_model import LinearRegression
    import random
    import matplotlib.pyplot as plt
    from scipy import stats
    import statsmodels.api as sm
    from sklearn import linear_model
    import pandas as pd
    import sqlalchemy as db
    from models import ODL, precipitation
    from sqlalchemy.orm import Session
    from sqlalchemy import select
    from WFSURLRepositoryLates7days import getOdl_1h,getPrecipitation_15min
    from DataFrameRepLates7days import DataFramelastes7daysModel
    from pathlib import Path  
    

    engine = db.create_engine('postgresql://postgres:123456@localhost:5432/geoODLdb')
    connection = engine.connect()
    metadata = db.MetaData()
    MultiLinearRegression_Train = db.Table('MultiLinearRegression_Train2', metadata, autoload=True, autoload_with=engine)

    table_df = pd.read_sql_table( MultiLinearRegression_Train, con=engine)

    data = read_csv("/home/raha/Raha/Thesis/Data/currently_active_odl_stations_selection.csv")
    # converting column data to list
    df= pd.DataFrame(table_df)
    loc_Codes = data['locality_code'].tolist()
    for i in loc_Codes:
        df_M= df.loc[df['Locality_code']== i]
        if df_M.empty:
            continue
        data_json1=getOdl_1h(i)
        datanorm1= pd.json_normalize(data_json1,"features")
        df1 = pd.DataFrame(datanorm1)
        if df1.empty:
            continue
        df1 = df1[['properties.id','properties.start_measure','properties.end_measure','properties.value']]
        df1.columns = ['Locality_code', 'Start_measure','End_measure','Value']
        #print(df1.info())
        data_json2=getPrecipitation_15min(i)
        datanorm2= pd.json_normalize(data_json2,"features")
        df2 = pd.DataFrame(datanorm2)
        if df2.empty:
            continue
        df2 = df2[['properties.id','properties.start_measure','properties.end_measure','properties.value']]
        df2.columns = ['Locality_code', 'Start_measure','End_measure','Value']
        #print(df2.info())

        df_7days = DataFramelastes7daysModel(df1,df2)
        #print(df_7days.head())
        
        x_test = df_7days[['Value_precipitation', 'Value_precipitationMinus2','Month']]
        y_prediction=[]
        y_real=[]
        #y_prediction=regr.predict(x_test)
        #print([ '%.3f' % elem for elem in y_prediction ])
        y_prediction=[]
        #y_prediction_precipitationMultiply2=[]
        #y_prediction_precipitationDivide2=[]
        for index in range(len(df_7days)):
            y_prediction.append((df_M['b0'])+(df_7days['Value_precipitation'][index])*df_M['b_Precipitation'] + (df_7days['Value_precipitationMinus2'][index])*df_M['b_PrecipitationMinus2'] + (df_7days['Month'][index])*df_M['b_Month'])
            #y_prediction_precipitationMultiply2.append((df_M['b0'])+(df_7days['Value_precipitation'][index]*2)*df_M['b_Precipitation'] + (df_7days['Value_precipitationMinus2'][index]*2)*df_M['b_PrecipitationMinus2'] + (df_7days['Month'][index])*df_M['b_Month'])
            #y_prediction_precipitationDivide2.append((df_M['b0'])+(df_7days['Value_precipitation'][index]*1/2)*df_M['b_Precipitation'] + (df_7days['Value_precipitationMinus2'][index]*1/2)*df_M['b_PrecipitationMinus2'] + (df_7days['Month'][index])*df_M['b_Month'])
        #print([ '%.3f' % elem for elem in y_prediction2 ])

        y_prediction=np.array(y_prediction)
        #y_prediction_precipitationMultiply2=np.array(y_prediction_precipitationMultiply2)
        #y_prediction_precipitationDivide2=np.array(y_prediction_precipitationDivide2)
        y_real = np.array(df_7days['Value_odl'])
        #print(df_7days['Value_odl'])
        #print (y_prediction)
        df_final = pd.DataFrame()
        df_final['Locality_code']= np.array(df_7days['Locality_code'])
        df_final['Start_measure']= np.array(df_7days.index)
        df_final['precipitation'] = np.array(df_7days['Value_precipitation'])
        df_final['y_ODL_real'] = y_real
        df_final['y_ODL_prediction'] = y_prediction
        #df_final['y_prediction_precipitationMultiply2'] = y_prediction_precipitationMultiply2
        #df_final['y_prediction_precipitationDivide2'] = y_prediction_precipitationDivide2
        #df_final['difference_real_Prediction']= ['%.10f' % elem for elem in y_real - y_prediction]

        pssql_table = "MultiLinearRegression_Test4"
        df_final.to_sql(name=pssql_table, con=connection, if_exists='append',index=False)
 
MultiLinearRegressionPrediction()