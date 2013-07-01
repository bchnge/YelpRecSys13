import sklearn.cross_validation as cv
import sklearn.metrics as metrics
import pandas as pd
import numpy as np

def evaluateModel(x,y,model,training_pct = 0.75, randomstate=10):
    """ Takes in x and y data and a model to be trained in order, performs cross validation based on the specified percentage allocated to training, and returns the RMSE for the test data """

    x_train, x_test, y_train, y_test= cv.train_test_split(x,y, train_size=training_pct, random_state = randomstate)
    fitted_model = model.fit(x_train, y_train)
    y_fitted = model.predict(x_test)
    rmse = (metrics.mean_squared_error(y_test, y_fitted))**0.5
    return rmse
    
    
def evaluateModelAvg(x,y,models, training_pct = 0.75):
    """ average the predicted results of models, which is a list of regressors to produce the final estimated y"""
    x_train, x_test, y_train, y_test= cv.train_test_split(x,y, train_size=training_pct)
    outcome = pd.DataFrame()
    for model in models:
        fitted = model.fit(x_train, y_train)
        outcome[model] = pd.Series(model.predict(x_test))
    y_hat = outcome.mean(axis = 1).values
    rmse = (metrics.mean_squared_error(y_test, y_hat))**0.5
    return mse
