import streamlit as st
# import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import yfinance as yf

# Define the Correction class
class Correction:
    plt.style.use("seaborn-v0_8")

    def __init__(self, symbol, sma_s=44, sma_l=200):
        self.symbol = symbol
        self.sma_s = sma_s
        self.sma_l = sma_l
        self.result = None
        self.data = self.get_ready_data()


    def get_ready_data(self):
        data = yf.download(self.symbol)
        data = pd.DataFrame(data)
        data = data.drop(columns=['Open', 'High', 'Low', 'Volume', 'Adj Close'])
        data['sma_s'] = data['Close'].rolling(self.sma_s).mean()
        data['sma_l'] = data['Close'].rolling(self.sma_l).mean()
        data['position'] = np.where(data['sma_s'] > data['sma_l'], 1, -1)
        data['change'] = data.Close.diff()
        data['gain'] = np.where(data.change > 0, data.change, 0)
        data['loss'] = np.where(data.change <= 0, data.change, 0)
        data['avg_gain'] = data['gain'].rolling(14).sum().div(14)
        data['avg_loss'] = data['loss'].rolling(14).sum().div(-14)
        data['rs'] = data['avg_gain'].div(data['avg_loss'])
        data['rsi'] = 100 - (100 / (1 + data['rs']))
        data.dropna(inplace=True)
        data['percent_k'] = ((data['Close'] - data['Close'].rolling(14).min()).div(data['Close'].rolling(14).max() - data['Close'].rolling(14).min())) * 100
        data['percent_d'] = data['percent_k'].rolling(3).mean()
        cond_2 = data['rsi'] < 20
        cond_3 = data['percent_k'] < 20
        cond_4 = data['percent_d'] < data['percent_k']
        cond_6 = data['rsi'] > 75
        cond_7 = data['percent_k'] > 80
        cond_8 = data['percent_d'] < data['percent_k']
        all_conditions_true = cond_2 & cond_3 & cond_4
        all_conditions_false = cond_6 & cond_7 & cond_8
        data['strategy_result'] = np.where(all_conditions_true, 1, np.where(all_conditions_false, -1, np.nan))
        data.dropna(inplace=True)
        self.result = data
        return data

    def plot_as_per(self, date_format_row_1=None, date_format_row_2=None, data_format_col=None, secondary_y=None):
        if data_format_col is None:
            data_format_col = []  # Default to empty list if not provided

        if not data_format_col:
            raise ValueError("data_format_col must contain at least one column to plot.")

        # Default for secondary_y if not provided
        secondary_y = secondary_y if secondary_y is not None else ['percent_k', 'percent_d']

        # Handle various cases for date filtering
        if date_format_row_1 is None and date_format_row_2 is None:
            filtered_data = self.data.loc[:, data_format_col]
        elif date_format_row_2 is None:
            filtered_data = self.data.loc[date_format_row_1:, data_format_col]
        else:
            filtered_data = self.data.loc[date_format_row_1:date_format_row_2, data_format_col]

        # Plot the filtered data with secondary_y columns
        fig, ax = plt.subplots(figsize=(18, 10))
        filtered_data.plot(
            ax=ax, fontsize=20, linewidth=2,
            secondary_y=secondary_y
        )
        plt.tight_layout()
        return fig

# Streamlit app implementation
def main():
    st.title("Stock Data Analysis")
    
    # Sidebar inputs
    st.sidebar.header("User Input")
    symbol = st.sidebar.text_input("Stock Symbol", value="AAPL")
    sma_s = st.sidebar.number_input("Short Moving Average (sma_s)", min_value=1, max_value=100, value=44)
    sma_l = st.sidebar.number_input("Long Moving Average (sma_l)", min_value=1, max_value=500, value=200)
    
    # Initialize the Correction class
    correction = Correction(symbol, sma_s, sma_l)

    # Display a subset of the data
    st.write("Stock data for:", symbol)
    st.dataframe(correction.result.head(10))  # Display the first 10 rows

    # Date range for plotting
    start_date = st.sidebar.date_input("Start Date", value=pd.to_datetime("2020-01-01"))
    end_date = st.sidebar.date_input("End Date", value=pd.to_datetime("2023-01-01"))

    # Columns to plot
    columns_to_plot = st.sidebar.multiselect("Columns to plot", options=correction.result.columns.tolist(), default=['Close', 'sma_s', 'sma_l'])
    
    # Plot data and show it in Streamlit
    st.header("Stock Data Visualization")
    if columns_to_plot:
        fig = correction.plot_as_per(
            date_format_row_1=start_date,
            date_format_row_2=end_date,
            data_format_col=columns_to_plot, secondary_y='strategy_result'
        )
        st.pyplot(fig)
    else:
        st.error("Please select at least one column to plot.")

if __name__ == "__main__":
    main()
