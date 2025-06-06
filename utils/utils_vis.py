import matplotlib.pyplot as plt
import streamlit as st
import pandas as pd
import numpy as np

def get_display_name(type, name_list, best_model_name=None, demand_type_info=None):
    """ 
    Generate display names and mappings for models or SKUs.
    Args:
        type (str): Type of names to generate ('model' or 'sku').
        name_list (dict): Dictionary of names to display.
        best_model_name (str, optional): Name of the best model to highlight.
        demand_type_info (dict, optional): Dictionary mapping SKUs to their demand types.
    Returns:
        tuple: A tuple containing a list of display names and a mapping dictionary.
    """
    if type == "model":
        display_names = [
        name + " (Best Model)" if name == best_model_name else name
        for name in name_list.keys()
        ]
        name_mapping = dict(zip(display_names, name_list.keys())) 
    elif type == "sku":
        display_names = [
            f"{sku} ({demand_type_info.get(sku, 'Unknown')})"
            for sku in name_list
        ]
        name_mapping = dict(zip(display_names, name_list)) 
    return display_names, name_mapping

def get_result_table(test, forecasts, selected_model_name):
    """
    Generate a DataFrame comparing actual values and forecasted values.
    Args:
        test (pd.Series): Actual test data.
        forecasts (dict): Dictionary of forecasts from different models.
        selected_model_name (str): Name of the selected model.
    Returns:
        pd.DataFrame: DataFrame containing actual values, forecasted values, percentage error, and absolute error.
    """
    forecast_values = pd.to_numeric(forecasts[selected_model_name], errors='coerce')
    test_numeric = pd.to_numeric(test, errors='coerce')
    test = test_numeric.fillna(0)
    results_df = pd.DataFrame({
            'Actual Value': test.round(3),
            'Forecast Value': forecast_values.round(3)
             })
    pct_error = (abs(results_df['Forecast Value'] - results_df['Actual Value']) / results_df['Actual Value'].replace(0, pd.NA)) * 100
    pct_error = pct_error.fillna(np.nan)
    results_df['Percentage Error (%)'] = pct_error.astype(float).round(3)
    results_df['Absolute Error'] = (results_df['Forecast Value'] - results_df['Actual Value']).round(3)
    results_df.index = results_df.index.strftime('%Y-%m-%d')
    return results_df

@st.cache_data
def get_product_info(df, selected_sku):
    """
    Retrieve product category and description for a given SKU.
    Args:
        df (pd.DataFrame): DataFrame containing product information.
        selected_sku (str): SKU of the product to retrieve information for.
    Returns:
        tuple: Product category and description.
    """
    info = df[df['PRODUCT'] == selected_sku].iloc[0]
    category = info.get('PROD_CAT', 'N/A')
    description = info.get('PRODUCT_DESCRIPTION', 'No description available.')
    return category, description

@st.cache_data
def get_split_dates(product_weekly):
    """
    Determine the minimum, maximum, and default dates for the date slider.
    Args:
        product_weekly (pd.Series): Weekly aggregated sales data for a product.
    Returns:
        tuple: Minimum date, maximum date, and default date for the date slider.
    """
    # min_date = max(product_weekly.index.min().to_pydatetime(), pd.to_datetime("2024-06-01").to_pydatetime())
    min_date = (product_weekly.index.max() - pd.Timedelta(days=365)).to_pydatetime() 
    max_date = product_weekly.index.max().to_pydatetime() 
    default_date = (product_weekly.index.max() - pd.Timedelta(days=90)).to_pydatetime() 
    return min_date, max_date, default_date

def get_forecast_result_fig(train, test, forecast_data, selected_model_name, selected_sku):
    """
    Generate a plot showing the forecast results for the selected model.
    Args:
        train (pd.Series): Training data.
        test (pd.Series): Actual test data.
        forecasts (dict): Dictionary of forecasts from different models.
        selected_model_name (str): Name of the selected model.
        selected_sku (str): SKU of the product being analyzed.
    Returns:
        matplotlib.figure.Figure: Figure object containing the plot.
    """
    fig, ax = plt.subplots(figsize=(14, 6))
    train.plot(ax=ax, label='Train', marker='o')
    test.plot(ax=ax, label='Actual', marker='o', color='#65a87b', alpha=0.7)
    forecast_data.plot(ax=ax, label='Forecast', linestyle='--', marker='o', color='#ff6303')
    ax.set_title(f"{selected_model_name} Forecast for PRODUCT {selected_sku}", fontsize=16)
    ax.set_xlabel("Date", fontsize=14)
    ax.set_ylabel("Total Value", fontsize=14)
    ax.legend()
    ax.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()
    return fig

def highlight_selected(row, selected_model_name):
    """
    Highlight the row corresponding to the selected model in the DataFrame.
    Args:
        row (pd.Series): A row from the DataFrame.
        selected_model_name (str): Name of the selected model.
    Returns:
        list: List of styles for the row.
    """
    if row["Model"] == selected_model_name:
        return ['background-color: #cce5ff; font-weight: bold; color: #003366'] * len(row)
    else:
        return [''] * len(row)
    
def get_styled_metrics_df(df, selected_model_name):
    """
    Generate a styled DataFrame for forecast accuracy metrics.
    Args:
        df (pd.DataFrame): DataFrame containing forecast accuracy metrics.
        selected_model_name (str): Name of the selected model.
    Returns:
        pd.io.formats.style.Styler: Styled DataFrame.
    """
    styled = (
        df.style
        .apply(highlight_selected, axis=1, args=(selected_model_name,))
        .format({
            "RMSE": "{:.2f}",
            "MAPE (%)": "{:.2f}",
            "Bias": "{:.2f}",
            "MAD": "{:.2f}"
        })
        .set_table_styles([
            {'selector': 'th', 'props': [('font-weight', 'bold')]}
        ])

    )
    return styled


def print_seperation_line():
    if "prev_control_values" not in st.session_state:
        st.session_state.prev_control_values = {}

    current_control_values = {
        "quantity_or_sales_choice": st.session_state["quantity_or_sales_choice"],
        "location_code_selection": st.session_state["location_code_selection"],
        "shipment_method_selection": st.session_state["shipment_method_selection"],
        "split_date_slider": st.session_state["split_date_slider"],
        "sku_selection": st.session_state["sku_selection"],
        "model_selection": st.session_state["model_selection"]
    }
    if current_control_values != st.session_state.prev_control_values:
        print("-" * 60)  # This prints to terminal
        st.write("---")  # This shows a visual separator in the app
        st.session_state.prev_control_values = current_control_values.copy()