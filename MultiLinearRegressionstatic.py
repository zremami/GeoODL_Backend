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

    engine = db.create_engine('postgresql://postgres:123456@localhost:5432/geoODLdb')
    connection = engine.connect()
    metadata = db.MetaData()
    odls_precipitations = db.Table('odls_precipitations', metadata, autoload=True, autoload_with=engine)
    df = table_df = pd.read_sql_table( odls_precipitations, con=engine)

    data = read_csv("/home/raha/Raha/Thesis/Data/currently_active_odl_stations_selection.csv")
    # converting column data to list
    loc_Codes = data['locality_code'].tolist()
    for i in loc_Codes:
        df_locality= df.loc[df['Locality_code']== i]
        x = df_locality[['Value_precipitation', 'Value_odlPlus2']]
        y = df_locality['Value_odl']

        regr = linear_model.LinearRegression()
        regr.fit(x, y)

        print('Intercept: \n', regr.intercept_)
        print('Coefficients: \n', regr.coef_)

        # with statsmodels
        #X = sm.add_constant(X) # adding a constant
        
        model = sm.OLS(y, x).fit()
        #predictions = model.predict(X) 
        
        print_model = model.summary()
        print(print_model)

MultiLinearRegressionStaticModel()