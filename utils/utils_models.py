import pandas as pd
import numpy as np
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from statsmodels.tsa.statespace.sarimax import SARIMAX
from pmdarima import auto_arima
from sklearn.linear_model import BayesianRidge
from sklearn.ensemble import GradientBoostingRegressor

def forecast_sarima(train, test, order=(1, 1, 1), seasonal_order=(1, 1, 1, 13)):
    if len(train) < 2 * seasonal_order[3]:
        seasonal_order = (0, 0, 0, 0)  # Disable seasonality if too short
    model = SARIMAX(train, order=order, seasonal_order=seasonal_order,
                    enforce_stationarity=False, enforce_invertibility=False)
    fit = model.fit(disp=False)
    forecast = fit.forecast(steps=len(test)).clip(lower=0)
    return forecast.values, fit.params

def forecast_holt_winters(train, test):
    model = ExponentialSmoothing(train, trend="add", seasonal="add", seasonal_periods=13)
    fit = model.fit()
    forecast = fit.forecast(len(test)).clip(lower=0)
    return forecast.values, fit.model.params

def forecast_auto_arima(train, test):
    model = auto_arima(train, seasonal=False, stepwise=True, trace=False)
    forecast = model.predict(n_periods=len(test)).clip(lower=0)
    return forecast, model.get_params()

def forecast_bayesian(train, test, lags=13):
    forecast_horizon = len(test)
    X_train_list = [train.shift(i + 1) for i in range(lags)]
    X_train = pd.concat(X_train_list, axis=1)
    X_train.columns = [f'lag_{i+1}' for i in range(lags)]

    X_train = X_train.iloc[lags:]
    y_train_trimmed = train.iloc[lags:]

    model = BayesianRidge()
    model.fit(X_train.values, y_train_trimmed.values)

    predictions = []
    current_history = train.values[-lags:].tolist()

    for _ in range(forecast_horizon):
        current_features = np.array(current_history).reshape(1, -1)
        next_prediction = model.predict(current_features)[0]
        predictions.append(next_prediction)
        current_history.pop(0)
        current_history.append(next_prediction)

    return np.array(predictions), None

def forecast_gradient_boost(train: pd.Series, test: pd.Series, lags: int = 52, n_estimators: int = 300, learning_rate: float = 0.05, max_depth: int = 5):
    forecast_horizon = len(test)
    
    X_train_list = [train.shift(i + 1) for i in range(lags)]
    X_train = pd.concat(X_train_list, axis=1)
    X_train.columns = [f'lag_{i+1}' for i in range(lags)]

    X_train = X_train.iloc[lags:]
    y_train_trimmed = train.iloc[lags:]

    model = GradientBoostingRegressor(
        n_estimators=n_estimators,
        learning_rate=learning_rate,
        max_depth=max_depth,
        random_state=42
    )
    model.fit(X_train.values, y_train_trimmed.values)

    predictions = []
    current_history = train.values[-lags:].tolist()

    for _ in range(forecast_horizon):
        current_features = np.array(current_history).reshape(1, -1)
        next_prediction = model.predict(current_features)[0]
        predictions.append(next_prediction)
        current_history.pop(0)
        current_history.append(next_prediction)

    return np.array(predictions), model.get_params()