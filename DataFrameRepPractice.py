def JSPRMLModel():
    from WFSRepository import getOdl_1h, getPrecipitation_15min
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
    print(df1.sum())
    print(df1.info())

    # conver to date to finde missing time stamp
    df1['properties.start'] = pd.to_datetime(df1['properties.start']).dt.tz_localize(None)

    df1 = df1.set_index(df1['properties.start'])
    


    # dates which are not in the sequence are returned
    missv=pd.date_range(start="2022-01-01 00:00:00", end="2022-12-23 06:00:00", freq = 'H').difference(df1.index)
    #print(missv.sort_values(ascending=True))
    print(pd.DataFrame(missv).count())
    missv = np.array(pd.to_datetime(missv.sort_values(ascending=True)))
    print(missv)
    print(df1)
    #print(df1.sum())
    #print(df1.info())

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
    df2.set_index('properties.start_measure', inplace=True)
    # resample it
    df2 = df2.resample('H').mean()

    df2.index.join(df2.index)

    print(df2)


    # drop timestamp which are missed in 1hr data frame
    df2 = df2.drop(missv)

    # find null values
    isnulldf2 = df2[df2['properties.value'].isnull()]
    # get time stamp which are null
    isnulldf2list = np.array(pd.to_datetime(isnulldf2.index))
    # drop the rows in both data frames which are null in 15 min data frame
    df2 = df2.drop(isnulldf2list)
    df1 = df1.drop(isnulldf2list)


    PRValueLs = np.array(df2['properties.value'])
    OLValueLs = np.array(df1['properties.value'])
    kenn = np.array(df1['properties.id'])


    df1['properties.valuePR'] = PRValueLs
    print(df1)

    combineODPR = d = {'Kenn': kenn, 'PRValueLs': PRValueLs, 'OLValueLs': OLValueLs}
    fcombineODPR = pd.DataFrame(data=combineODPR)
    print(fcombineODPR)
    return fcombineODPR

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