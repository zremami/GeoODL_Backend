from pandas import *
def MultiLinearRegressionStaticModel():
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

    engine = db.create_engine('postgresql://postgres:123456@localhost:5432/geoODLdb')
    connection = engine.connect()
    metadata = db.MetaData()
    odls_precipitations = db.Table('odls_precipitations', metadata, autoload=True, autoload_with=engine)
    df = table_df = pd.read_sql_table( odls_precipitations, con=engine)

    data = read_csv("/home/raha/Raha/Thesis/Data/currently_active_odl_stations_selection.csv")
    # converting column data to list
    df_M = pd.DataFrame()
    loc_Codes = data['locality_code'].tolist()
    for i in loc_Codes:
        df_M = pd.DataFrame()
        df_locality= df.loc[df['Locality_code']== i]
        if df_locality.empty:
            continue
        x = df_locality[['Value_precipitation', 'Value_precipitationMinus2','Month']]
        y = df_locality['Value_odl']

        regr = linear_model.LinearRegression()
        regr.fit(x, y)

        #model = LinearRegression(fit_intercept=False).fit(x, y)
        #print('R-s: \n', regr.score(x, y))
        #print('Intercept: \n', regr.intercept_.astype(float))
        #print('Coefficients: \n', regr.coef_)
        coefArray = np.array(regr.coef_)
        df_M['Locality_code']=[str(i)]
        df_M['R-squared']=[regr.score(x, y)]
        df_M['b0'] = [regr.intercept_.astype(float)]
        df_M['b_Precipitation']=[coefArray[0]]
        df_M['b_PrecipitationMinus2']=[coefArray[1]]
        df_M['b_Month']=[coefArray[2]]

        pssql_table = "MultiLinearRegression_Train"
        df_M.to_sql(name=pssql_table, con=connection, if_exists='append')
        #print(df_M.head())

        # with statsmodels
        x = sm.add_constant(x) # adding a constant
        
        model = sm.OLS(y, x).fit()
        
        print_model = model.summary()
        #print(print_model)

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
        if df2.empthy:
            continue
        df2 = df2[['properties.id','properties.start_measure','properties.end_measure','properties.value']]
        df2.columns = ['Locality_code', 'Start_measure','End_measure','Value']
        #print(df2.info())

        df_7days = DataFramelastes7daysModel(df1,df2)
        #print(df_7days.head())
        
        x_test = df_7days[['Value_precipitation', 'Value_precipitationMinus2','Month']]
        y_prediction=[]
        y_real=[]
        y_prediction=regr.predict(x_test)
        #print([ '%.3f' % elem for elem in y_prediction ])
        regr = linear_model.LinearRegression()
        y_prediction2=[]
        for index in range(len(df_7days)):
            y_prediction2.append(df_M['b0']+df_7days['Value_precipitation'][index]*df_M['b_Precipitation'] + df_7days['Value_precipitationMinus2'][index]*df_M['b_PrecipitationMinus2'] + + df_7days['Month'][index]*df_M['b_Month'])
        #print([ '%.3f' % elem for elem in y_prediction2 ])

        y_real = np.array(df_7days['Value_odl'])
        #print(df_7days['Value_odl'])
        #print (y_prediction)
        df_final = pd.DataFrame()
        df_final['Locality_code']= np.array(df_7days['Locality_code'])
        df_final['Start_measure']= np.array(df_7days.index)
        df_final['y_ODL_real'] = y_real
        df_final['y_ODL_prediction'] = [ '%.3f' % elem for elem in y_prediction ]
        df_final['difference_real_Prediction']= ['%.3f' % elem for elem in y_real - y_prediction]

        pssql_table = "MultiLinearRegression_Test"
        df_final.to_sql(name=pssql_table, con=connection, if_exists='append')
 
MultiLinearRegressionStaticModel()