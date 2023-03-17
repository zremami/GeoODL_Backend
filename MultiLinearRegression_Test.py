from pandas import *
import pandas as pd
import numpy as np
import sklearn 
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error as mae
import random
from scipy import stats
import statsmodels.api as sm
from sklearn import linear_model
import sqlalchemy as db
from models import ODL, precipitation
from sqlalchemy.orm import Session
from sqlalchemy import select
from WFSURLRepositoryLates7days import getOdl_1h,getPrecipitation_15min
from DataFrameRepLates7days import DataFramelastes7daysModel
from pathlib import Path
import json
import statistics
from dtos import predictionDTO 
from datetime import datetime

def MultiLinearRegression_Test(locality_code):

    #connect to database
    engine = db.create_engine('postgresql://postgres:123456@localhost:5432/geoODLdb')
    connection = engine.connect()
    metadata = db.MetaData()

    # get MultiLinearRegression_Train table from database
    MultiLinearRegression_Train = db.Table('MultiLinearRegression_Train', metadata, autoload=True, autoload_with=engine)
    table_df = pd.read_sql_table( MultiLinearRegression_Train, con=engine)

    # converting  MultiLinearRegression_Train table to dataframe
    df= pd.DataFrame(table_df)

    # MultiLinearRegression_Train dataframe with a given locality_code
    df_M= df.loc[df['Locality_code']== locality_code]

    # get 1h_odl 7days data test
    data_json1=getOdl_1h(locality_code)
    datanorm1= pd.json_normalize(data_json1,"features")
    df1 = pd.DataFrame(datanorm1)
    if df1.empty:
        return 0
    # change the name of the columns
    df1 = df1[['properties.id','properties.start_measure','properties.end_measure','properties.value']]
    df1.columns = ['Locality_code', 'Start_measure','End_measure','Value']
    #print(df1.info())

    # get 15_min 7days data set
    data_json2=getPrecipitation_15min(locality_code)
    datanorm2= pd.json_normalize(data_json2,"features")
    df2 = pd.DataFrame(datanorm2)

    if df2.empty:
        return 0

    # change the name of the columns
    df2 = df2[['properties.id','properties.start_measure','properties.end_measure','properties.value']]
    df2.columns = ['Locality_code', 'Start_measure','End_measure','Value']
    #print(df2.info())

    # create the dataset resampled 15min and joined with 1h odl
    df_7days = DataFramelastes7daysModel(df1,df2)

    #df_20days.groupby(pd.Grouper(freq='M'))
    #grouped = df_20days.groupby('Month') 

    # create another Month column to have unnummy month number as the original month column will be eliminated by being nummy
    df_7days['Month_'] = df_7days['End_measure'].dt.month
    # make the month column nummy
    df7_dummies = pd.get_dummies(df_7days,columns=['Month'])

    y_real=[]
    y_prediction=[]
    locality_name=[]

    # create a prediction dataframe by putting test data in to a fumula
    for index in range(len(df_7days)):
        b_month_string = 'b_Month' + str(df7_dummies['Month_'][index])
        append_odl = float(
            df_M['b0'] + #b0
            (df_M['b_Precipitation'] * df_7days['Value_precipitation'][index]) + #b1x1
            (df_M['b_PrecipitationMinus2'] * df_7days['Value_precipitationMinus2'][index]) + #b2x2
            (df_M[b_month_string] * 1) #b3x3
        )
        y_prediction.append(float("%.3f" % append_odl))


    y_real = np.array(df_7days['Value_odl'])
    meanAE = mae(y_real,y_prediction)
    
    df_7days['end_measure'] = list(map(lambda x: x / 1000000000, df_7days['End_measure'].values.astype(Int32Dtype)))
    #print(np.array(df_7days['End_measure']))
    # create final dataframe
    df_final = pd.DataFrame()
    #df_final['locality_code']= np.array(df_7days['Locality_code'])
    #df_final['Locality_name']= df_M['Locality_name']
    df_final['end_measure']= np.array(df_7days['end_measure'])
    df_final['precipitation'] = np.array(df_7days['Value_precipitation']).astype(float)
    df_final['odl_real'] = y_real
    df_final['odl_prediction'] = y_prediction
    df_final['difference_real_Prediction']= ['%.10f' % elem for elem in y_real - y_prediction]
    df_final['absolute_percent_error']= [elem for elem in (abs(y_real - y_prediction)  / abs(y_real)) * 100]

    mape = np.mean(df_final['absolute_percent_error'])

    y_prediction_evaluate=[]
    for index in range(len(y_real)):
        y_prediction_evaluate.append('out of range' if abs(y_real[index] - y_prediction[index]) > meanAE else 'in range')

    df_final['evaluate_prediction']= y_prediction_evaluate

    mean_y_real = np.mean(y_real)
    STDV_y_real= np.std(y_real)

    out_range_result = df_final[(df_final['evaluate_prediction'] == "out of range")] 

    odl_predict_sorted = df_final.sort_values('odl_prediction', ascending=False)
    odl_predict_10head = odl_predict_sorted.head(10)
    odl_predict_10head_sorted = odl_predict_10head.sort_values('end_measure', ascending=True)
    #print(odl_predict_10head)
    good_result=[]
    good_result_string=[]
    bad_result=[]
    bad_result_string=[]
    for row in odl_predict_10head_sorted.index:
        slop = df_final.loc[row,'odl_real'] - df_final.loc[row-1,'odl_real']
        endMeasureTimestamp = odl_predict_10head.loc[row,'end_measure']

        if slop > 0:
            good_result.append(endMeasureTimestamp)
            good_result_string.append(datetime.fromtimestamp(endMeasureTimestamp).strftime("%d-%m-%Y %H:%M:%S"))
        else:
            bad_result.append(endMeasureTimestamp)
            bad_result_string.append(datetime.fromtimestamp(endMeasureTimestamp).strftime("%d-%m-%Y %H:%M:%S"))


    #print("we can see in these days",good_result ,"the model works well")
    #print("we can see in these days",bad_result ,"the model works well")
    #print("we can see in these days",np.array(out_range_result['end_measure']) ,"the p)redicted valused do not match real")
    #odl_precipitation_Max = df_final['precipitation'].max()
    #df_predict_range = df_final[(df_final['precipitation'] >= odl_precipitation_median)]
    #print(df_predict_range[['odl_prediction','odl_real','end_measure','precipitation']])

    result = df_final.to_dict('records')

    #goodResultString = json.dumps(good_result)
    #badResultString = json.dumps(bad_result)
    #print(df_M.index[0])

    prediction = predictionDTO.predictionDTO()
    prediction.localityCode = locality_code
    prediction.localityName = df_M.loc[df_M.index[0],'Locality_name']
    prediction.stdRealValue = 2*STDV_y_real
    prediction.meanRealValue = mean_y_real
    prediction.mape = mape
    prediction.meanAbsoluteError = meanAE
    prediction.result = result
    prediction.goodPoints = good_result
    prediction.badPoints = bad_result

    message = ''
    message += 'This is a chart showing the real and predicted value of ODL and precipitation in the latest 7 days in {0}.'
    message += 'There is a boundary around the real value that can show you where the predicted values are not in a range of real values which means the model does not predict very accurately.'
    message += 'ALso by comparing the slope of predicted and real value we can see how well the model works. For example, in these points {1} you can see while the predicted values are increasing the actual values are decreasing which is not good.'
    message += 'On the other hand, you can see in these points {2} the model works well as the predicted values increasing the actual values are increasing too.'
    message += 'Here you may see that there is precipitation which can prove this hypothesis that the increase in ODL is because of an increase in precipitation.'
    message = message.format(prediction.localityName, ', '.join(bad_result_string), ', '.join(good_result_string))
    prediction.message = message

    #df_final['mae_evaluate']= ['%.10f' % elem for elem in meanAE - (y_prediction - y_real)]

    #pssql_table = "MultiLinearRegression_Test"
    #df_final.to_sql(name=pssql_table, con=connection, if_exists='append',index=False)
    #json.loads(result + goodResultString + badResultString)
    jsonResult = json.loads(prediction.toJSON())

    return jsonResult