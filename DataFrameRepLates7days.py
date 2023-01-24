from pandas import *
from WFSRepository import getOdl_1h, getPrecipitation_15min
from precipitationsRepository import getAllprecipitations
from odlsRepository import getAllOdls
import pandas as pd
import pandas as pd
import pandas as pd
import numpy as np
import sqlalchemy as db
def DataFramelastes7daysModel(df1,df2):
    
    # convert to datetime 
    df1['Start_measure'] = pd.to_datetime(df1['Start_measure']).dt.tz_localize(None)
    df1['End_measure'] = pd.to_datetime(df1['End_measure']).dt.tz_localize(None)
    df1['Value'] = df1['Value'].astype(float)

    # create a list to resample and agregate data
    df1 = df1.squeeze()
    df1.set_index('Start_measure', inplace=True)


    # convert to datetime 
    df2['Start_measure'] = pd.to_datetime(df2['Start_measure']).dt.tz_localize(None)
    df2['End_measure'] = pd.to_datetime(df2['End_measure']).dt.tz_localize(None)
    df2['Value'] = df2['Value'].astype(float)


    # create a list to resample and agregate data
    df2 = df2.squeeze()
    df2.set_index('Start_measure', inplace=True)
    # resample it
    
    df2=df2.resample('H')['Value'].mean()
    #print(df2_locality_code.head())

    df3 = df1.join(df2, lsuffix='_odl', rsuffix='_precipitation', how='inner')
    #print(df3)

    # drop all rows with any NaN and NaT values
    df3 = df3.dropna()
    print(df3)

    value_precipitationMinus2List = []
    # i++ = (1,len(df3),2)
    for index in range(len(df3)):
        #if index == len(df3)- 2:
            #break
        if index == 0 or index == 1 or index == 2:
            continue
        mines2=index-2
        value_precipitationMinus2List.append(df3['Value_precipitation'][mines2])
        
    df3 = df3.iloc[:-3]
    #value_odlPlus2array = np.array(value_odlPlus2List)
    df3['Value_precipitationMinus2'] = np.array(value_precipitationMinus2List)
    df3['Month'] = df3['End_measure'].dt.month 

    return df3

