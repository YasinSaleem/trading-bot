



import yfinance as yf
import pandas as pd
import json
import os
from utils.logger import get_logger
from config import USE_DUMMY_DATA

logger = get_logger(__name__)

def get_stock_data(ticker: str, start_date: str, end_date: str, interval: str = '1d') -> pd.DataFrame:
    """
    Fetch historical or intraday stock data from yfinance or dummy JSON if USE_DUMMY_DATA is set.
    """
    if USE_DUMMY_DATA:
        try:
            dummy_path = os.path.join(os.path.dirname(__file__), 'nifty50_dummy.json')
            with open(dummy_path, 'r') as f:
                dummy_data = json.load(f)
            if ticker not in dummy_data:
                logger.warning(f"No dummy data found for {ticker}.")
                return pd.DataFrame()
            df = pd.DataFrame(dummy_data[ticker])
            df['Date'] = pd.to_datetime(df['Date'])
            df = df[(df['Date'] >= pd.to_datetime(start_date)) & (df['Date'] <= pd.to_datetime(end_date))]
            df.set_index('Date', inplace=True)
            return df
        except Exception as e:
            logger.error(f"Error loading dummy data for {ticker}: {e}")
            return pd.DataFrame()
    else:
        try:
            logger.info(f"Fetching data for {ticker} from {start_date} to {end_date} (interval: {interval})")
            data = yf.download(ticker, start=start_date, end=end_date, interval=interval, progress=False)
            if data.empty:
                logger.warning(f"No data found for {ticker} in the given date range.")
            return data
        except Exception as e:
            logger.error(f"Error fetching data for {ticker}: {e}")
            return pd.DataFrame()
