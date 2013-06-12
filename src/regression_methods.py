import sklearn.cross_validation as cv
import sklearn.metrics as metrics

def evaluateModel(x,y,model,training_pct = 0.75):
    """ Takes in x and y data and a model to be trained in order, performs cross validation based on the specified percentage allocated to training, and returns the RMSE for the test data """

    x_train, x_test, y_train, y_test= cv.train_test_split(x,y, train_size=training_pct)
    fitted_model = model.fit(x_train, y_train)
    y_fitted = model.predict(x_test)
    rmse = (metrics.mean_squared_error(y_test, y_fitted))**0.5
    return rmse
