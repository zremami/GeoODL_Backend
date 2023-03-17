def JSPRMLModel():
    from WFSOWSLibRepository import getOdl_1h, getPrecipitation_15min
    import pandas as pd
    import numpy as np
    import sklearn 
    from sklearn.linear_model import LinearRegression

    # get odl1hr data
    data1json=getOdl_1h()
    # serialize it to convert to data frame
    data1norm= pd.json_normalize(data1json,"features")
    #convert to data frame
    df1 = pd.DataFrame(data1norm)

    # conver to date to finde missing time stamp
    df1['properties.end_measure'] = pd.to_datetime(df1['properties.end_measure']).dt.tz_localize(None)
    df1['properties.start'] = pd.to_datetime(df1['properties.end_measure']).dt.tz_localize(None)
    df1 = df1.set_index(df1['properties.end_measure'])  

    # get 15min data
    data2json=getPrecipitation_15min()
    # serilize it to make it data farame
    data2norm= pd.json_normalize(data2json,"features")
    # convert to data farame
    df2 = pd.DataFrame(data2norm)

    # convert to datetime 
    df2['properties.start_measure'] = pd.to_datetime(df2['properties.start_measure']).dt.tz_localize(None)
    df2['properties.end_measure'] = pd.to_datetime(df2['properties.end_measure']).dt.tz_localize(None)


    # create a list to resample and agregate data
    df2 = df2.squeeze()
    df2.set_index('properties.end_measure', inplace=True)
    # resample it
    df2=df2.resample('H').mean()


    df3 = df1.join(df2, lsuffix='_odl', rsuffix='_precipitation', how='inner')

    print(df3)
    print(df3.info())

    # drop all rows with any NaN and NaT values
    df3 = df3.dropna()
    print(df3)

    #df4 = df3[df3["properties.start"].isin(pd.date_range(start='2021-01-01 01:00:00', end='2023-01-10 23:00:00', freq='1H'))]
    #df = pd.DataFrame({'date':pd.date_range(start='2020-11-03', end='2021-10-01')})

    value_odlPlus2List = []
    # i++ = (1,len(df3),2)
    for index in range(len(df3)):
        if index == len(df3)- 2:
            break
        plus2=index+2
        value_odlPlus2List.append(df3['properties.value_odl'][plus2])
        
    df3 = df3.iloc[:-2]
    #value_odlPlus2array = np.array(value_odlPlus2List)
    df3['value_precipitationPlus2'] = value_odlPlus2List

    df4 = df3[['properties.id', 'properties.value_odl', 'properties.value_precipitation', 'value_precipitationPlus2']]


    print(df4)

    return df4

    #df = pd.DataFrame(df, columns=['properties.start_measure', 'properties.value'])
    #display(df['properties.start_measure'].min())
    #display(df['properties.start_measure'].max())
    #print(df['properties.start_measure'].loc['2022-11-27'].head(5))
    #mask = (df['properties.start_measure']>= pd.Timestamp('2022-11-23')) & (df['properties.start_measure'] < pd.Timestamp('2022-11-24'))
    #display(df.loc[mask])


    '''df.set_index('properties.start_measure', inplace=True)
    display(df.sort_index())
    print(type(df.index))
    display(df.at_time('12:05'))
    display(df.between_time('00:00','02:00'))
    display(df.sort_index().first('5B'))
    display(df.sort_index().last('1W'))
    print(df['properties.value'])
    print(df)
    print(df.info())
    print(df.get(['properties.value']))
    df = pd.DataFrame(df)
    df.resample('D',on='properties.start_measure').mean()
    print(df)
    #df[df['properties.value'] == 1].resample('D')['properties.value'].mean()
    #print(df.groupby(df['properties.end_measure']))
    #df.groupby(df['properties.end_measure']).resample('D')[df['properties.value']].max()


    index = pd.date_range('2022-12-04', periods=9, freq='T')
    series = pd.Series(range(9), index=index)
    print(series)
    print(series.resample('3T').sum())


    print(df)'''