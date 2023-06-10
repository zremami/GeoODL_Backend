def MultiLinearRegressionModel():
    from DataFrameRepFly import JSPRMLModel
    import pandas as pd
    import numpy as np
    import sklearn 
    from sklearn.linear_model import LinearRegression
    import random
    import matplotlib.pyplot as plt
    from scipy import stats
    import statsmodels.api as sm
    from sklearn import linear_model

    df = JSPRMLModel()   

    X = df[['properties.value_precipitation', 'value_precipitationPlus2']]
    y = df['properties.value_odl']

    regr = LinearRegression()
    regr.fit(X, y)

    print('Intercept: \n', regr.intercept_)
    print('Coefficients: \n', regr.coef_)

    # with statsmodels
    X = sm.add_constant(X) # adding a constant
    
    model = sm.OLS(y, X).fit()
    predictions = model.predict(X) 
    
    print_model = model.summary()
    print(print_model)
    
MultiLinearRegressionModel()