def JSPRMLModel():
    from WFSRepository import getOdl_1h, getPrecipitation_15min
    import pandas as pd
    import numpy as np
    import sklearn 
    from sklearn.linear_model import LinearRegression

    data1json=getOdl_1h()
    data1norm= pd.json_normalize(data1json,"features")
    df1 = pd.DataFrame(data1norm)
    df1['properties.start'] = pd.to_datetime(df1['properties.start']).dt.tz_localize(None)
    df1 = df1.set_index(df1['properties.start'])
 
    # to_datetime() method converts string
    # format to a DateTime object
    #df1.index = pd.to_datetime(df1.index)
    
    # dates which are not in the sequence
    # are returned
    #pd.date_range(start = df.TS.min(), end = df.TS.max(), freq = 'D').difference(df.TS)
    missv=pd.date_range(start="2022-01-01 00:00:00", end="2022-12-23 06:00:00", freq = 'H').difference(df1.index)
    print(missv.sort_values(ascending=True))
    print(pd.DataFrame(missv).count())

    print(df1)
    #print(df1.sum())
    #print(df1.info())


    data2json=getPrecipitation_15min()
    data2norm= pd.json_normalize(data2json,"features")
    df2 = pd.DataFrame(data2norm)

    df2['properties.start_measure'] = pd.to_datetime(df2['properties.start_measure']).dt.tz_localize(None)
    df2['properties.end_measure'] = pd.to_datetime(df2['properties.end_measure']).dt.tz_localize(None)

    #print(df2.duplicated(subset=['properties.end_measure']))
    #print(df2.sum())
    #print(df2.info())

    df2 = df2.squeeze()
    df2.set_index('properties.start_measure', inplace=True)
    df2 = df2.resample('H').mean()

    print(df2)
    #print(df2.sum())
    #print(df2.info())

    #ss = pd.DataFrame(df2, columns = df2['properties.value'])
    PRValueLs = np.array(df2['properties.value'])
    OLValueLs = np.array(df1['properties.value'])
    print(PRValueLs)
    print(OLValueLs)

    df1['properties.valuePR'] = PRValueLs

    #df1.insert(loc=1, column="properties.value2",  value=ss)

    print(df1)

    combineODPR = df1[["properties.kenn","properties.start_measure", "properties.value","properties.valuePR"]]
    print(combineODPR)
    return combineODPR

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