
def PreproccessingModel():
    from WFSOWSLibRepository import getOdl_1h, getPrecipitation_15min
    import pandas as pd
    import numpy as np
    from IPython.display import display
    from tabulate import tabulate
    from matplotlib import pyplot as plt


    data1 = getOdl_1h()
    #data2 = getPrecipitation_15min()
    datanorm1= pd.json_normalize(data1,"features")
    df1=pd.DataFrame(datanorm1)
    print(df1.sum())
    print(df1.info())
    print(df1.describe())
    print(df1[['geometry.type','geometry.coordinates','properties.id','properties.locality_name','properties.start','properties.end_measure']].describe())
    print(df1[['properties.unit','properties.value_e','properties.nuclide','properties.duration','properties.dom','properties.source','properties.network_id']].describe())
    display(df1[['geometry.type','geometry.coordinates','properties.id','properties.locality_name']].head())
    display(df1[['properties.start','properties.end_measure','properties.unit','properties.value']].head())

    #,'properties.unit','properties.value_e','properties.value','properties.nuclide','properties.duration','properties.dom','properties.source','properties.network_id'
    #print(tabulate(df1[['geometry.type','geometry.coordinates','properties.id','properties.locality_name','properties.start','properties.end_measure','properties.value']].head(), headers = 'keys', tablefmt = 'psql'))


    df1['properties.end_measure'] = pd.to_datetime(df1['properties.end_measure']).dt.tz_localize(None)
    df1['properties.start'] = pd.to_datetime(df1['properties.end_measure']).dt.tz_localize(None)
    df1 = df1.set_index(df1['properties.end_measure'])
    df1=df1.resample('D').mean()
    df1.plot()
    plt.savefig('filename.jpg')
    plt.show()

PreproccessingModel()