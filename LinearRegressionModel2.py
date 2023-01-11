import numpy as np
import matplotlib.pyplot as plt
from DataFrameRep import JSPRMLModel
from sklearn.model_selection import train_test_split
  
def estimate_coef(x, y):

    # number of observations/points
    n = np.size(x)
  
    # mean of x and y vector
    m_x = np.mean(x)
    m_y = np.mean(y)
  
    # calculating cross-deviation and deviation about x
    SS_xy = np.sum(y*x) - n*m_y*m_x
    SS_xx = np.sum(x*x) - n*m_x*m_x
  
    # calculating regression coefficients
    b_1 = SS_xy / SS_xx
    b_0 = m_y - b_1*m_x
  
    return (b_0, b_1)
  
def plot_regression_line(x, y, b):
    # plotting the actual points as scatter plot
    plt.scatter(x, y, color = "m",
               marker = "o", s = 30)
  
    # predicted response vector
    y_pred = b[0] + b[1]*x
  
    # plotting the regression line
    plt.plot(x, y_pred, color = "g")
  
    # putting labels
    plt.xlabel('x')
    plt.ylabel('y')
  
    # function to show plot
    plt.show()
  
def main():

    df = JSPRMLModel()

    #train_data = df[:42]
    #test_data = df[126:]

    x= np.array(df['properties.valuePR'])
    y= np.array(df['properties.value'])

    X_train, X_test, y_train, y_test = train_test_split(x,y,test_size=1/3,random_state=0)
    # observations / data
    #x = np.array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
    #y = np.array([1, 3, 2, 5, 7, 8, 8, 9, 10, 12])
  
    # estimating coefficients
    b = estimate_coef(X_train, y_train)
    print("Estimated coefficients:\nb_0 = {}  \
          \nb_1 = {}".format(b[0], b[1]))
  
    # plotting regression line
    plot_regression_line(X_train, y_train, b)
  
if __name__ == "__main__":
    main()