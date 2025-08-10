
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

USE_DUMMY_DATA = bool(int(os.getenv('USE_DUMMY_DATA', '0')))

# List of NIFTY 50 stock tickers (example subset)
NIFTY50_TICKERS = [
    'RELIANCE.NS',
    'TCS.NS',
    'INFY.NS',
    'HDFCBANK.NS',
    'ICICIBANK.NS',
    'HINDUNILVR.NS',
    'SBIN.NS',
    'KOTAKBANK.NS',
    'LT.NS',
    'AXISBANK.NS'
    # Add more as needed

]

# Date range for backtesting
START_DATE = os.getenv('START_DATE', '2024-01-01')
END_DATE = os.getenv('END_DATE', '2024-07-01')

# Google Sheets config
GOOGLE_SHEETS_CREDENTIALS = os.getenv('GOOGLE_SHEETS_CREDENTIALS', 'credentials.json')
GOOGLE_SHEET_NAME = os.getenv('GOOGLE_SHEET_NAME', 'AlgoBotTrades')

# Initial capital for backtesting
INITIAL_CAPITAL = float(os.getenv('INITIAL_CAPITAL', 100000))

# RSI period for the strategy
RSI_PERIOD = int(os.getenv('RSI_PERIOD', 14))

# Moving average windows
SHORT_WINDOW = int(os.getenv('SHORT_WINDOW', 50))
LONG_WINDOW = int(os.getenv('LONG_WINDOW', 100))
