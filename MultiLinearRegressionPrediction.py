from pandas import *
def MultiLinearRegressionPrediction():
    from DataFrameRep import JSPRMLModel
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
    from modelURL import ODL, precipitation
    from sqlalchemy.orm import Session
    from sqlalchemy import select
    from WFSRepositoryLates7days import getOdl_1h,getPrecipitation_15min
    from DataFrameRepLates7days import DataFramelastes7daysModel
    from pathlib import Path  
    

    engine = db.create_engine('postgresql://postgres:123456@localhost:5432/geoODLdb')
    connection = engine.connect()
    metadata = db.MetaData()
    MultiLinearRegression_Train = db.Table('MultiLinearRegression_Train', metadata, autoload=True, autoload_with=engine)
    MultiLinearRegression_Test = db.Table('MultiLinearRegression_Test', metadata, autoload=True, autoload_with=engine)

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
        for index in range(len(df_7days)):
            y_prediction.append((df_M['b0'])+(df_7days['Value_precipitation'][index])*df_M['b_Precipitation'] + (df_7days['Value_precipitationMinus2'][index])*df_M['b_PrecipitationMinus2'] + (df_7days['Month'][index])*df_M['b_Month'])
        #print([ '%.3f' % elem for elem in y_prediction2 ])

        y_real = np.array(df_7days['Value_odl'])
        #print(df_7days['Value_odl'])
        #print (y_prediction)
        df_final = pd.DataFrame()
        df_final['Locality_code']= np.array(df_7days['Locality_code'])
        df_final['Start_measure']= np.array(df_7days.index)
        df_final['y_ODL_real'] = y_real
        df_final['y_ODL_prediction'] = np.array(y_prediction)
        #df_final['difference_real_Prediction']= ['%.3f' % elem for elem in y_real - y_prediction]

        filepath_test = Path('/home/raha/Raha/Thesis/Data/MultiLinearRegression_Test.csv')  
        df_final.to_csv(filepath_test)
 
MultiLinearRegressionPrediction()