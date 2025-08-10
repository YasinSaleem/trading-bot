# Algo Trading Bot

A modular Python-based prototype for algorithmic trading on NIFTY 50 stocks. This bot uses a combination of technical indicators (RSI and Moving Averages) to generate trading signals, backtests the strategy, and logs the results to Google Sheets. It also includes a basic Machine Learning component for predicting price movements.

## Features

*   **Data Fetching:** Fetches historical stock data using `yfinance`.
*   **Trading Strategy:** Implements a strategy based on Relative Strength Index (RSI) and Simple Moving Averages (SMA).
*   **Backtesting:** Simulates the trading strategy on historical data to evaluate performance.
*   **Portfolio Analytics:** Calculates key metrics like Profit & Loss (P&L) and Win Ratio.
*   **Google Sheets Integration:** Logs trades, P&L, and portfolio summaries to a Google Sheet for easy tracking.
*   **Machine Learning:** A simple ML model to predict stock price movements (up or down).
*   **Dummy Data:** Includes a dummy dataset for testing purposes, especially useful if `yfinance` has issues with Indian stock data.

## How it Works

The bot executes the following workflow:

1.  **Configuration:** Loads settings from a `.env` file and `config.py`.
2.  **Data Fetching:** For each ticker in `NIFTY50_TICKERS`, it fetches historical data from `yfinance` or the local dummy data file.
3.  **Signal Generation:** It calculates RSI and moving averages to generate `BUY` and `SELL` signals.
4.  **Backtesting:** It simulates trades based on the generated signals and calculates the performance.
5.  **Analytics:** It computes P&L, win ratio, and other metrics for each stock and for the overall portfolio.
6.  **Google Sheets Logging:** It logs all trades, P&L statements, and summary reports to a specified Google Sheet.
7.  **ML Prediction:** It trains a simple model on the historical data to predict future price movements and logs the predictions.

## Setup and Installation

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd algo-bot
    ```

2.  **Create a virtual environment and activate it:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install the dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set up Google Sheets API credentials:**
    *   Follow the instructions [here](https://docs.gspread.org/en/latest/oauth2.html) to create a service account and get your credentials JSON file.
    *   Rename the downloaded JSON file to `credentials.json` and place it in the root directory of the project.
    *   Share your Google Sheet with the `client_email` found in your `credentials.json` file.

5.  **Configure environment variables:**
    *   Create a `.env` file in the root directory. You can do this by copying the `.env.example` if one exists, or creating a new file.
    *   Add the following variables to your `.env` file:
        ```
        # Set to 1 to use dummy data, 0 to use yfinance
        USE_DUMMY_DATA=1

        # Date range for backtesting
        START_DATE=2024-01-01
        END_DATE=2024-07-01

        # Google Sheets configuration
        GOOGLE_SHEETS_CREDENTIALS=credentials.json
        GOOGLE_SHEET_NAME=AlgoBotTrades

        # Financial settings
        INITIAL_CAPITAL=100000

        # Strategy parameters
        RSI_PERIOD=14
        SHORT_WINDOW=50
        LONG_WINDOW=100
        ```

## Usage

To run the bot, execute the `main.py` script:

```bash
python main.py
```

The bot will then process the stocks listed in `config.py`, run the backtest, and log the results to your configured Google Sheet.

### Testing with Dummy Data

The `yfinance` library can sometimes be unreliable for fetching data for Indian stocks. To ensure you can test the bot's functionality without relying on `yfinance`, you can use the provided dummy data.

To use the dummy data, set the `USE_DUMMY_DATA` variable in your `.env` file to `1`:

```
USE_DUMMY_DATA=1
```

The bot will then use the `data/nifty50_dummy.json` file for backtesting instead of fetching live data. This allows you to test the entire workflow, from signal generation to Google Sheets logging, without any external data dependencies.

## Configuration

The main configuration for the bot is managed in two places:

*   **.env file:** For user-specific settings like API keys, date ranges, and initial capital.
*   **config.py:** For the list of stock tickers (`NIFTY50_TICKERS`) and other fixed parameters.

## Disclaimer

This project is for educational and demonstration purposes only. It is not financial advice. Trading stocks involves significant risk, and you should not use this bot for live trading without fully understanding the risks and the code.