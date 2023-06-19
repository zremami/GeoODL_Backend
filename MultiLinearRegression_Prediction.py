#This class was created to prediction and simulation and calculation for better data analysys
from pandas import *
import pandas as pd
import numpy as np
import sqlalchemy as db
from sqlalchemy.orm import Session
from WFSURLRepository7days import getOdl_1h,getPrecipitation_15min
from DataFrame7days import DataFrame7daysModel
import json
import statistics
from dtos import predictionDTO 
from datetime import datetime

def MultiLinearRegression_Prediction(locality_code,start,end, effect, effect2):

    #connect to database
    engine = db.create_engine('postgresql://postgres:123456@localhost:5432/geoODLdb')
    connection = engine.connect()
    metadata = db.MetaData()

    # get MultiLinearRegression_Train table from database
    MultiLinearRegression_Train = db.Table('PMultiLinearRegression_Trained', metadata, autoload=True, autoload_with=engine)
    table_df = pd.read_sql_table( MultiLinearRegression_Train, con=engine)

    # converting  MultiLinearRegression_Train table to dataframe
    df= pd.DataFrame(table_df)
    prediction = predictionDTO.predictionDTO()

    # MultiLinearRegression_Train dataframe with a given locality_code
    df_M= df.loc[df['Locality_code']== locality_code]

    # get 1h_odl 7days data test
    data_json1=getOdl_1h(locality_code,start,end)
    datanorm1= pd.json_normalize(data_json1,"features")
    df1 = pd.DataFrame(datanorm1)

    # check if it is empty
    if df1.empty:
        jsonResult = json.loads(prediction.toJSON())
        return jsonResult


    # change the name of the columns
    df1 = df1[['properties.id','properties.start','properties.end_measure','properties.value']]
    df1.columns = ['Locality_code', 'Start_measure','End_measure','Value']

    # get 15_min 7days data set
    data_json2=getPrecipitation_15min(locality_code,start,end)
    datanorm2= pd.json_normalize(data_json2,"features")
    df2 = pd.DataFrame(datanorm2)

    # check if it is empty
    if df2.empty:
        jsonResult = json.loads(prediction.toJSON())
        return jsonResult

    # change the name of the columns
    df2 = df2[['properties.id','properties.start_measure','properties.end_measure','properties.value']]
    df2.columns = ['Locality_code', 'Start_measure','End_measure','Value']

    # create the dataset resampled 15min and joined with 1h odl
    df_7days = DataFrame7daysModel(df1,df2)


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
            (df_M['b_Precipitation'] * df_7days['Value_precipitation'][index])*float(effect) + #b1x1
            (df_M['b_PrecipitationMinus2'] * df_7days['Value_precipitationMinus2'][index])*float(effect2)+ #b2x2
            (df_M[b_month_string] * 1) #b3x3
        )
        y_prediction.append(float("%.3f" % append_odl))


    y_real = np.array(df_7days['Value_odl'])
    
    df_7days['end_measure'] = list(map(lambda x: x / 1000000000, df_7days['End_measure'].values.astype(Int32Dtype)))

    df_final = pd.DataFrame()
    df_final['end_measure']= np.array(df_7days['end_measure'])
    df_final['precipitation'] = np.array(df_7days['Value_precipitation']).astype(float)
    df_final['odl_real'] = y_real
    df_final['odl_prediction'] = y_prediction

    # mean of prediction
    mean_y_predict = np.mean(y_prediction)
    # standard deviation of prediction
    STDV_y_predict= np.std(y_prediction)


    # calculation to test the hypothesys (increase in precipiation might lead increase in ODL)
    #sorted odl predicted ascending
    odl_predict_sorted = df_final.sort_values('odl_prediction', ascending=False)
    #pick top 10
    odl_predict_10head = odl_predict_sorted.head(10)
    # sort the new dataset
    odl_predict_10head_sorted = odl_predict_10head.sort_values('end_measure', ascending=True)

    true_hypo=[]
    false_hypo=[]
    for row in odl_predict_10head_sorted.index:
        if row == 0:
            continue
        # slop of real odl value
        slop_odl_real = df_final.loc[row,'odl_real'] - df_final.loc[row-1,'odl_real']
        # slop of predicted odl value
        slop_odl_prediction = df_final.loc[row,'odl_prediction'] - df_final.loc[row-1,'odl_prediction']
        # slop of precipiation value
        slop_precipitation = df_final.loc[row,'precipitation'] - df_final.loc[row-1,'precipitation']
        # save the timespan
        endMeasureTimestamp = odl_predict_10head.loc[row,'end_measure']

        # check if the hypothesis is true
        if slop_odl_real > 0 and  slop_odl_prediction >0 and slop_precipitation>0:
            true_hypo.append(endMeasureTimestamp)

        # check if hypothesys is false
        elif slop_odl_real < 0  and slop_odl_prediction > 0  and slop_precipitation>0:
            false_hypo.append(endMeasureTimestamp)


    # make it readble to convert to json
    result = df_final.to_dict('records')
    # collect properties to convert to json
    prediction.localityCode = locality_code
    prediction.localityName = df_M.loc[df_M.index[0],'Locality_name']
    prediction.stdPredictValue = 2*STDV_y_predict
    prediction.meanPredictValue = mean_y_predict
    prediction.result = result
    prediction.truePoints = true_hypo
    prediction.falsePoints = false_hypo

    # convert to jason
    jsonResult = json.loads(prediction.toJSON())

    return jsonResult