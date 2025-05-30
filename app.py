import streamlit as st
import pandas as pd
from datetime import timedelta
from utils.utils_data import *
from utils.utils_models import *
from utils.utils_vis import *
from utils.utils_css import *

# Load the data
DATA_PATH = "masked_sales_df.csv"
sales_df = load_sales_data(DATA_PATH)

# All available models to select from
model_options = {
    "Auto ARIMA": forecast_auto_arima,
    "Seasonal ARIMA": forecast_sarima,
    "Holt-Winters": forecast_holt_winters,
    "Bayesian Regression": forecast_bayesian,
    "Gradient Boosting": forecast_gradient_boost
}
# Set up the Streamlit app
st.markdown(style, unsafe_allow_html=True)
st.title("Demand Forecasting Dashboard")

# Sidebar UI for better layout
st.sidebar.header("Controls")

## ADD singole choicce control of QUANTITY VS TOTAL_SALES
quantity_or_sales = st.sidebar.radio(
    "Select Quantity or Total Sales",
    options=["QUANTITY", "TOTAL_SALES"],
    index=0
)

# Add location code selection
location_code = st.sidebar.multiselect(
    "Select Location Code",
    options=["2", "9", "15"],
    default=["2", "9", "15"]
)

sales_df = filter_location(sales_df, location_code)

# Add shipment type selection
shipment_method = st.sidebar.multiselect(
    "Select Shipment Method",
    options=["WILL CALL", "UPS GROUND"],
    default=["WILL CALL", "UPS GROUND"],
)
sales_df = filter_shipment_method(sales_df, shipment_method)

# SKU selection
sku_list = sales_df['PRODUCT'].unique()
demand_type_info = determine_demand_type(sales_df, quantity_or_sales=quantity_or_sales)

# Add (demand type) to SKU names
sku_display_names, sku_name_mapping = get_display_name(type="sku", name_list=sku_list, demand_type_info=demand_type_info)
selected_display = st.sidebar.selectbox("Select a SKU", sku_display_names)
selected_sku = sku_name_mapping[selected_display]

# Display product information
product_category, product_description = get_product_info(sales_df, selected_sku)
st.subheader("Product Information")
st.markdown(f"**SKU:** {selected_sku} &nbsp;&nbsp;&nbsp; **Product Category:** {product_category}", unsafe_allow_html=True)
st.markdown(f"**Description:** {product_description}")

# Prepare data for selected SKU
product_weekly = aggregate_weekly_sales(selected_sku, sales_df, quantity_or_sales=quantity_or_sales)

# Add date slider for split point selection
min_date, max_date, default_date = get_split_dates(product_weekly)
split_date = st.sidebar.slider(
    "Select Train/Test Split Date:",
    min_value=min_date,
    max_value=max_date,
    value=default_date,
    format="YYYY-MM-DD"
)
# Split data
train, test = train_test_split(product_weekly, split_date=split_date)

# Check if the product has enough sales records at the selected locations
if (train != 0).sum() < 13:
    st.warning("This product does not enough sales record at this location! Please select more locations or choose later split date.")
    st.stop()

# Calculate forecasts and MAPE for all models (cached)
forecasts, rmse, mape, bias, mad = calculate_forecasts(train, test, model_options)
# Find the best model based on MAPE
best_model_name = min(mape, key=mape.get)
best_model_forecast = forecasts[best_model_name]

# Add "(Best Model)" to display names
model_display_names, model_name_mapping = get_display_name( type="model", name_list=model_options, best_model_name=best_model_name)
selected_display_name = st.sidebar.radio(
        "Select a Forecasting Model:",
        model_display_names,
        index=model_display_names.index(best_model_name + " (Best Model)")
    )
selected_model_name = model_name_mapping[selected_display_name]
selected_model = model_options[model_name_mapping[selected_display_name]]

# Plot forecast vs actual curve
forecast_days = ((max_date + timedelta(days=30)).date() - split_date.date()).days
st.subheader("Forecast Results Visualization")
st.markdown(f"**Number of days to forecast:** {str(forecast_days)}")
forecast_data = forecasts[selected_model_name]
fig = get_forecast_result_fig(train, test, forecast_data, selected_model_name, selected_sku)
st.pyplot(fig)

# Forecast accuracy metrics
st.subheader(f"Forecast Accuracy Metrics for product {selected_sku}")

metrics_df = pd.DataFrame({
    "Model": list(rmse.keys()),
    "RMSE": [rmse[m] for m in rmse],
    "MAPE (%)": [mape[m] for m in mape],
    "Bias": [bias[m] for m in bias],
    "MAD": [mad[m] for m in mad]
})
styled_df = get_styled_metrics_df(metrics_df, selected_model_name)
st.dataframe(styled_df, use_container_width=True, hide_index=True)

# Forecast results table (Actual vs Forecast)
st.subheader(f"Forecasting Results Table for product {selected_sku}")
results_sales_df = get_result_table(test, forecasts, selected_model_name)
st.dataframe(results_sales_df)