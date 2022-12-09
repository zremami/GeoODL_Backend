def JsonMLModel():
    from WFSRepository import getWFSData
    import pandas as pd
    from IPython.display import display

    datajson=getWFSData()
    datanorm= pd.json_normalize(datajson,"features")
    df = pd.DataFrame(datanorm)
    df['properties.start_measure'] = pd.to_datetime(df['properties.start_measure']).dt.tz_localize(None)
    df['properties.end_measure'] = pd.to_datetime(df['properties.start_measure']).dt.tz_localize(None)
    df = pd.DataFrame(df, columns=['properties.start_measure', 'properties.value','properties.end_measure'])
    display(df['properties.start_measure'].min())
    display(df['properties.start_measure'].max())
    #print(df['properties.start_measure'].loc['2022-11-27'].head(5))
    mask = (df['properties.start_measure']>= pd.Timestamp('2022-11-23')) & (df['properties.start_measure'] < pd.Timestamp('2022-11-24'))
    display(df.loc[mask])

    df.set_index('properties.start_measure', inplace=True)
    display(df.sort_index())
    print(type(df.index))
    display(df.at_time('12:05'))
    display(df.between_time('00:00','02:00'))
    display(df.sort_index().first('5B'))
    display(df.sort_index().last('1W'))

    #df[df['properties.value'] == 1].resample('D')['properties.value'].mean()
    print(df.groupby(df['properties.end_measure']))
    df.groupby(df['properties.end_measure']).resample('D')[df['properties.value']].max()
    print(df)

JsonMLModel()