def LinearRegressionModel():
    from DataFrameRep import JSPRMLModel
    import pandas as pd
    import numpy as np
    import sklearn 
    from sklearn.linear_model import LinearRegression
    import random
    import matplotlib.pyplot as plt
    from scipy import stats
    import statsmodels.api as sm

    df = JSPRMLModel()   

    x= np.array(df['properties.value_precipitation'])
    y= np.array(df['properties.value_odl'])

    model = LinearRegression()
    model.fit(x.reshape((-1, 1)), y)

    model = LinearRegression().fit(x.reshape((-1, 1)), y)
    r_sq = model.score(x.reshape((-1, 1)), y)
    print(f"coefficient of determination: {r_sq}")

    x = sm.add_constant(x)

    #fit linear regression model
    model = sm.OLS(y, x).fit()

    #view model summary
    print(model.summary())

    """slope, intercept, r, p, std_err = stats.linregress(x, y)

    def myfunc(x):
        return slope * x + intercept

    mymodel = list(map(myfunc, x))

    plt.scatter(x, y)
    plt.figure()
    plt.plot(x, mymodel)
    plt.show(block=False)"""

LinearRegressionModel()