import streamlit as st

def location_code_control():
    selected_locations = st.sidebar.multiselect("Select Location Code", 
                           options=["2", "9", "15"], 
                           default=["2", "9", "15"], 
                           key="location_code_selection")
    return selected_locations

def shipment_method_control():
    selected_shipments = st.sidebar.multiselect("Select Shipment Method", 
                                                options=["WILL CALL", "UPS GROUND"], 
                                                default=["WILL CALL", "UPS GROUND"], 
                                                key="shipment_method_selection")
    return selected_shipments

def display_value_control():
    selected_display = st.sidebar.radio("Select Quantity or Total Sales", 
                                        options=["QUANTITY", "TOTAL_SALES"], 
                                        index=0, 
                                        key="quantity_or_sales_choice")
    return selected_display

def sku_control(sku_display_names):
    selected_sku = st.sidebar.selectbox("Select a SKU", 
                                        sku_display_names, 
                                        index=0, 
                                        key="sku_selection")
    return selected_sku

def split_date_control(min_date, max_date, default_date):
    selected_split_date = st.sidebar.slider("Select Train/Test Split Date:", 
                                            min_value=min_date, 
                                            max_value=max_date, 
                                            value=default_date, 
                                            format="YYYY-MM-DD", 
                                            key="split_date_slider")
    return selected_split_date

def model_control(model_display_names, best_model_name):
    selected_model = st.sidebar.radio("Select a Forecasting Model:", 
                                      model_display_names, 
                                      index=model_display_names.index(best_model_name + " (Best Model)"), 
                                      key="model_selection")
    return selected_model