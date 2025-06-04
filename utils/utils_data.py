import pandas as pd
import numpy as np
import streamlit as st

@st.cache_data
def load_sales_data(file_path):
    """
    Load sales data from a CSV file and parse the ORDER_DATE column.
    Args:
        file_path (str): Path to the CSV file containing sales data.
    Returns:
        pd.DataFrame: DataFrame containing the sales data with ORDER_DATE parsed as datetime.
    """
    sales_df = pd.read_csv(file_path)
    sales_df['ORDER_DATE'] = pd.to_datetime(sales_df['ORDER_DATE'], errors='coerce')
    return sales_df

@st.cache_data
def filter_location(df, location_codes):
    """
    Filter the DataFrame to include only rows with specified location codes.
    Args:
        df (pd.DataFrame): DataFrame containing sales data.
        location_codes (list): List of location codes to filter by.
    Returns:
        pd.DataFrame: Filtered DataFrame containing only rows with specified location codes.
    """
    df = df.dropna(subset=['SHIPPING_PLANT'])
    df['SHIPPING_PLANT'] = df['SHIPPING_PLANT'].astype(int).astype(str)
    sales_df = df[df['SHIPPING_PLANT'].isin(location_codes)]  
    return sales_df

@st.cache_data
def filter_shipment_method(df, shipment_methods):
    """
    Filter the DataFrame to include only rows with specified shipment methods.  
    Args:
        df (pd.DataFrame): DataFrame containing sales data.
        shipment_methods (list): List of shipment methods to filter by.
    Returns:   
        pd.DataFrame: Filtered DataFrame containing only rows with specified shipment methods.
    """
    sales_df = df[df['SHIP_VIA_TYPE'].str.startswith(tuple(shipment_methods))]
    return sales_df

def calculate_adi_cv2(df, group_by_cols, quantity_or_sales='QUANTITY'):
    """
    Calculate Average Demand Interval (ADI) and Coefficient of Variation squared (CV2) for each product.
    Args:
        df (pd.DataFrame): DataFrame containing sales data.
        group_by_cols (list): List of columns to group by (e.g., ['PRODUCT']).
        quantity_or_sales (str): Column name to use for calculations ('QUANTITY' or 'TOTAL_SALES').
    Returns:
        pd.DataFrame: DataFrame containing ADI, CV2, and non-zero counts for each product.
    """

    adi = df.groupby(group_by_cols).apply(
        lambda x: len(x) / max((x[quantity_or_sales] > 0).sum(), 1)
    )
    cv2 = df.groupby(group_by_cols)[quantity_or_sales].apply(
        # lambda x: (x.std() / x.mean())**2 if x.mean() != 0 else 0
        lambda x: ((x.std(ddof=0) / x.mean())**2 if x.mean() != 0 else 0)
    ).fillna(0)

    non_zero_counts = df.groupby(group_by_cols)[quantity_or_sales].apply(lambda x: (x > 0).sum())
    return pd.DataFrame({
        'PRODUCT': adi.index.tolist(),
        'ADI': adi.values.flatten(),
        'CV2': cv2.values.flatten(),
        'NonZeroCount': non_zero_counts.values
    })

@st.cache_data
def determine_demand_type(_df, quantity_or_sales="QUANTITY"):
    """
    Determine the demand type for each product based on ADI and CV2.
    Args:
        df (pd.DataFrame): DataFrame containing sales data.
        quantity_or_sales (str): Column name to use for calculations ('QUANTITY' or 'TOTAL_SALES').
    Returns:
        dict: Dictionary mapping each product to its demand type.
    """
    adi_cv2_df = calculate_adi_cv2(_df, ['PRODUCT'], quantity_or_sales=quantity_or_sales)
    
    conditions = [
        (adi_cv2_df['NonZeroCount'] < 13),  # less than 10 non-zero sales entries → NA
        (adi_cv2_df['ADI'] <= 1.32) & (adi_cv2_df['CV2'] <= 0.49),
        (adi_cv2_df['ADI'] > 1.32)  & (adi_cv2_df['CV2'] <= 0.49),
        (adi_cv2_df['ADI'] <= 1.32) & (adi_cv2_df['CV2'] > 0.49),
        (adi_cv2_df['ADI'] > 1.32)  & (adi_cv2_df['CV2'] > 0.49)
    ]
    choices = ['NA', 'smooth', 'intermittent', 'erratic', 'lumpy']
    adi_cv2_df['Demand_Type'] = np.select(conditions, choices, default='unknown')
    return adi_cv2_df.set_index('PRODUCT')['Demand_Type'].to_dict()
    
@st.cache_data
def train_test_split(series, split_date, test_days=90):
    """
    Split a time series into training and testing sets based on a specified date.
    Args:
        series (pd.Series): Time series data indexed by date.
        split_date (str or datetime): Date to split the series into train and test sets.
        test_days (int): Number of days to include in the test set after the split date.
    Returns:
        tuple: Two pandas Series, the training set and the testing set.
    """
    train = series[series.index < split_date]
    test = series[series.index >= split_date]
    return train, test

@st.cache_data
def calculate_metrics(actual, forecast):
    """
    Calculate forecast accuracy metrics: RMSE, MAPE, Bias, and MAD.
    Args:
        actual (pd.Series): Actual values.
        forecast (pd.Series): Forecasted values.
    Returns:
        tuple: RMSE, MAPE, Bias, and MAD.
    """
    residuals = actual - forecast
    rmse = np.sqrt(np.mean(residuals ** 2))
    mape = np.mean(np.abs(residuals / actual.replace(0, np.nan))) * 100  # Avoid division by zero
    bias = residuals.mean()
    mad = np.mean(np.abs(residuals))
    return rmse, mape, bias, mad

@st.cache_data
def aggregate_weekly_sales(selected_sku, df, quantity_or_sales='QUANTITY'):
    """
    Aggregate sales data for a specific product on a weekly basis.
    Args:
        selected_sku (str): SKU of the product to filter.
        df (pd.DataFrame): DataFrame containing sales data.
        quantity_or_sales (str): Column name to use for aggregation ('QUANTITY' or 'TOTAL_SALES').
    Returns:
        pd.Series: Weekly aggregated sales data for the selected product.
    """
    product_df = df[df['PRODUCT'] == selected_sku].copy()
    product_df = product_df.dropna(subset=['ORDER_DATE'])
    product_df = product_df.set_index('ORDER_DATE').sort_index()

    product_weekly = product_df[quantity_or_sales].resample('W-MON').sum().fillna(0)
    return product_weekly

@st.cache_data
def calculate_forecasts(train, test, _model_options):
    """
    Calculate forecasts using different models and return the results.
    Args:
        train (pd.Series): Training data.
        test (pd.Series): Testing data.
        model_options (dict): Dictionary of model names and their corresponding functions.
    Returns:
        tuple: Dictionary of forecasts, RMSE, MAPE, Bias, and MAD for each model.
    """
    forecasts = {}
    rmse = {}
    mape = {}
    bias = {}
    mad = {}

    for model_name, model_func in _model_options.items():
        forecast_result = model_func(train, test)
        forecast = forecast_result[0] if isinstance(forecast_result, tuple) else forecast_result
        forecasts[model_name] = pd.Series(forecast, index=test.index)
        rmse[model_name], mape[model_name], bias[model_name], mad[model_name] = calculate_metrics(test, forecast)

    return forecasts, rmse, mape, bias, mad