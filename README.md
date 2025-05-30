# Demand Forecasting Dashboard

## Introduction 📊

This repository contains the code for a **Demand Forecasting Dashboard**. The primary goal of this project is to provide a user-friendly interface for visualizing and predicting future demand for products or services. By leveraging historical data, this dashboard aims to help businesses make informed decisions regarding inventory management, resource allocation, and strategic planning.

The dashboard allows users to:
* Upload or connect to their sales/demand data.
* Perform exploratory data analysis on historical trends.
* Apply various forecasting models.
* Visualize predicted demand alongside historical data.
* Evaluate the accuracy of different forecasting models.

## Software Requirements 💻

To run, modify, or contribute to this project, you will need the following software:

* **Python:** The primary programming language used for this project. **Python 3.10 or higher** is generally recommended for compatibility with the listed libraries.
* **Git:** For version control, cloning the repository, and contributing to changes.
* **Required Python Libraries:** These can be found in the `requirements.txt` file and should be installed in your Python environment. They include:
    * `streamlit`: For creating and serving the interactive web dashboard.
    * `pandas`: Essential for data manipulation and analysis.
    * `numpy`: For numerical operations.
    * `matplotlib`: For generating static, animated, and interactive visualizations.
    * `statsmodels`: Used for time series analysis and statistical modeling.
    * `pmdarima`: For easy use of ARIMA and AutoARIMA models, simplifying time series forecasting.
    * `scikit-learn` (sklearn): Used for implementing machine learning models and utilities.

**To set up the environment, follow these steps:**

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/eugenia0804/DemandForecastingDashboard.git](https://github.com/eugenia0804/DemandForecastingDashboard.git)
    cd DemandForecastingDashboard
    ```

2.  **Create a virtual environment (recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3.  **Install dependencies:**
    With the `requirements.txt` file in the repository, you can install all necessary packages using:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Run the Streamlit application:**
    You would run it using:
    ```bash
    streamlit run app.py
    ```

## Project Origin and Acknowledgements

This project was adapted from the **[IEMS 394: Client Project Challenge](https://www.mccormick.northwestern.edu/industrial/academics/undergraduate/client-project-challenge/)** for our client **[C.R. Laurence](https://www.crlaurence.com/)**, conducted under the guidance of the **Northwestern University [Department of Industrial Engineering & Management Sciences](https://www.mccormick.northwestern.edu/industrial/)**.

Contributors to this project include my teammates [Dor Palkovic](https://www.linkedin.com/in/dorpalkovic/), [Tyler Tanaka-Wong](https://www.linkedin.com/in/tyler-tanaka-wong-17a4b5266/), and [Kevin Zhang](https://www.linkedin.com/in/kevinzhangkjz/). The development of this dashboard also benefited greatly from the insights of our advisor, **[Edward C. Malthouse](https://www.medill.northwestern.edu/directory/faculty/edward-c-malthouse.html)**, and the client-side representative involved in the original project. Their contributions were invaluable in shaping the direction and functionality of this tool.