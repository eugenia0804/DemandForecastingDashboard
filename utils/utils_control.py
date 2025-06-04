import streamlit as st


quantity_or_sales = st.sidebar.radio(
    "Select Quantity or Total Sales",
    options=["QUANTITY", "TOTAL_SALES"],
    index=0,
    key="quantity_or_sales_choice"
)

location_code = st.sidebar.multiselect(
    "Select Location Code",
    options=["2", "9", "15"],
    default=["2", "9", "15"],
    key="location_code_selection"
)

shipment_method = st.sidebar.multiselect(
    "Select Shipment Method",
    options=["WILL CALL", "UPS GROUND"],
    default=["WILL CALL", "UPS GROUND"],
    key="shipment_method_selection"
)
