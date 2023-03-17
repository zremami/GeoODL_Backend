from pandas import *
def MultiLinearRegressionTrain():
    import pandas as pd
    import numpy as np
    import sklearn 
    from sklearn.linear_model import LinearRegression
    import random
    from scipy import stats
    import statsmodels.api as sm
    from sklearn import linear_model
    import pandas as pd
    import sqlalchemy as db
    from sqlalchemy.orm import Session
    from sqlalchemy import select
    from WFSURLRepositoryLates7days import getOdl_1h,getPrecipitation_15min
    from DataFrameRepLates7days import DataFramelastes7daysModel

    engine = db.create_engine('postgresql://postgres:123456@localhost:5432/geoODLdb')
    connection = engine.connect()
    metadata = db.MetaData()
    odls_precipitations = db.Table('odls_precipitations', metadata, autoload=True, autoload_with=engine)

    table_df =pd.read_sql_table( odls_precipitations, con=engine)
    sondenstandorte = read_csv("/home/raha/Raha/Thesis/Data/odl_sondenstandorte.csv")
    df_sondenstandorte= pd.DataFrame(sondenstandorte)
    data = read_csv("/home/raha/Raha/Thesis/Data/currently_active_odl_stations_selection.csv")
    # converting column data to list
    loc_Codes = data['locality_code'].tolist()
    for i in loc_Codes:
        df_M = pd.DataFrame()
        df_locality= table_df.loc[table_df['Locality_code']== i]
        df_sondenstandorte_l_code = df_sondenstandorte.loc[df_sondenstandorte['locality_code']== i]
        #df_merge = df_locality.set_index('Locality_code').join(dfCoordinate.set_index('locality_code'))
        if df_locality.empty:
            continue
        df_dummies = pd.get_dummies(df_locality,columns=['Month'])

        #df_dummies[['Month_1','Month_2','Month_3','Month_4','Month_5','Month_6','Month_7','Month_8','Month_9','Month_10','Month_11','Month_12']] = df_dummies[['Month_1','Month_2','Month_3','Month_4','Month_5','Month_6','Month_7','Month_8','Month_9','Month_10','Month_11','Month_12']].astype(int)
        #df_new = pd.concat([df_locality, df_dummies], axis=1)
        #df_dummies = df_dummies[['Locality_code','Value_odl','Value_precipitation', 'Value_precipitationMinus2','Month_1','Month_2','Month_3','Month_4','Month_5','Month_6','Month_7','Month_8','Month_9','Month_10','Month_11','Month_12']]


        #print(df_new)
        x = df_dummies[['Value_precipitation', 'Value_precipitationMinus2','Month_1','Month_2','Month_3','Month_4','Month_5','Month_6','Month_7','Month_8','Month_9','Month_10','Month_11','Month_12']]
        y = df_dummies['Value_odl']

        x.columns = x.columns.astype(str)

        regr = linear_model.LinearRegression()
        model=regr.fit(x, y)

        #model = LinearRegression(fit_intercept=False).fit(x, y)
        #print('R-s: \n', model.score(x, y))
        #print('Intercept: \n', model.intercept_)
        #print('Coefficients: \n', np.array(model.coef_))
        coefArray = np.array(model.coef_.astype(float))
        df_M['Locality_code']=[str(i)]
        df_M['Locality_name']=np.array(df_sondenstandorte_l_code['locality_name'])
        df_M['R_squared']=[model.score(x, y)]
        x = sm.add_constant(x) # adding a constant       
        model2 = sm.OLS(y, x).fit()
        df_M['R_squared_adjusted']=[model2.rsquared_adj]
        df_M['b0'] = [model.intercept_.astype(float)]
        df_M['b_Precipitation']=[coefArray[0]]
        df_M['b_PrecipitationMinus2']=[coefArray[1]]
        df_M['b_Month1']=[coefArray[2]]
        df_M['b_Month2']=[coefArray[3]]
        df_M['b_Month3']=[coefArray[4]]
        df_M['b_Month4']=[coefArray[5]]
        df_M['b_Month5']=[coefArray[6]]
        df_M['b_Month6']=[coefArray[7]]
        df_M['b_Month7']=[coefArray[8]]
        df_M['b_Month8']=[coefArray[9]]
        df_M['b_Month9']=[coefArray[10]]
        df_M['b_Month10']=[coefArray[11]]
        df_M['b_Month11']=[coefArray[12]]
        df_M['b_Month12']=[coefArray[13]]
        df_M['latitude']=np.array(df_sondenstandorte_l_code['latitude'])
        df_M['longitude']=np.array(df_sondenstandorte_l_code['longitude'])
        
        #print(df_M.head())
        pssql_table = "MultiLinearRegression_Train"
        df_M.to_sql(name=pssql_table, con=connection, if_exists='append',index=False)
        #print(df_M.head())

        #print(model2.summary())
 
MultiLinearRegressionTrain()