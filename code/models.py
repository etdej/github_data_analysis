import collections as col

from sklearn.linear_model import LassoCV, LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.ensemble import AdaBoostRegressor
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error


ModelResultSet = col.namedtuple(
    "ModelResultSet",
    ["model", "mae", "mse", "r2_outofsample", "r2_insample"]
)


def linearregression(train_x_func, train_y_func, test_x_func, test_y_func):
    regr = LinearRegression(normalize=True)
    regr.fit(train_x_func, train_y_func)
    y_pred_outofsample = regr.predict(test_x_func)
    y_pred_insample = regr.predict(train_x_func)
    mae = mean_absolute_error(test_y_func, y_pred_outofsample)
    mse = mean_squared_error(test_y_func, y_pred_outofsample)
    r2_outofsample = r2_score(test_y_func, y_pred_outofsample)
    r2_insample = r2_score(train_y_func, y_pred_insample)
    return ModelResultSet(regr, mae, mse, r2_outofsample, r2_insample)


def lassocv(train_x_func, train_y_func, test_x_func, test_y_func):
    lassocv = LassoCV(normalize=True)
    lassocv.fit(train_x_func, train_y_func)
    y_pred_outofsample = lassocv.predict(test_x_func)
    y_pred_insample = lassocv.predict(train_x_func)
    mae = mean_absolute_error(test_y_func, y_pred_outofsample)
    mse = mean_squared_error(test_y_func, y_pred_outofsample)
    r2_outofsample = r2_score(test_y_func, y_pred_outofsample)
    r2_insample = r2_score(train_y_func, y_pred_insample)
    return ModelResultSet(lassocv, mae, mse, r2_outofsample, r2_insample)


def randomforest(train_x, train_y, test_x, test_y):
    rfr = RandomForestRegressor()
    rfr.fit(train_x, train_y)
    y_pred_outofsample = rfr.predict(test_x)
    y_pred_insample = rfr.predict(train_x)
    mae = mean_absolute_error(test_y, y_pred_outofsample)
    mse = mean_squared_error(test_y, y_pred_outofsample)
    r2_outofsample = r2_score(test_y, y_pred_outofsample)
    r2_insample = r2_score(train_y, y_pred_insample)
    return ModelResultSet(rfr, mae, mse, r2_outofsample, r2_insample)


def adaboost(train_x, train_y, test_x, test_y):
    ada = AdaBoostRegressor()
    ada.fit(train_x, train_y)
    y_pred_outofsample = ada.predict(test_x)
    y_pred_insample = ada.predict(train_x)
    mae = mean_absolute_error(test_y, y_pred_outofsample)
    mse = mean_squared_error(test_y, y_pred_outofsample)
    r2_outofsample = r2_score(test_y, y_pred_outofsample)
    r2_insample = r2_score(train_y, y_pred_insample)
    return ModelResultSet(ada, mae, mse, r2_outofsample, r2_insample)


def gradientboosting(train_x, train_y, test_x, test_y):
    gbr = GradientBoostingRegressor()
    gbr.fit(train_x, train_y)
    y_pred_outofsample = gbr.predict(test_x)
    y_pred_insample = gbr.predict(train_x)
    mae = mean_absolute_error(test_y, y_pred_outofsample)
    mse = mean_squared_error(test_y, y_pred_outofsample)
    r2_outofsample = r2_score(test_y, y_pred_outofsample)
    r2_insample = r2_score(train_y, y_pred_insample)
    return ModelResultSet(gbr, mae, mse, r2_outofsample, r2_insample)


ModelsDict = col.OrderedDict()
ModelsDict["LinearRegression"] = linearregression
ModelsDict["LassoCV"] = lassocv
ModelsDict["RandomForest"] = randomforest
ModelsDict["GradientBoosting"] = gradientboosting


def run_all(train_x, train_y, test_x, test_y, models_dict=ModelsDict):
    results_dict = col.OrderedDict()
    for func_name, func in models_dict.items():
        results_dict[func_name] = func(train_x, train_y, test_x, test_y)
    return results_dict
