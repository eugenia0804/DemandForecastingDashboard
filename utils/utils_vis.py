import matplotlib.pyplot as plt

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