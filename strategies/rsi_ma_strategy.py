
import pandas as pd
from utils.logger import get_logger

logger = get_logger(__name__)

def calculate_rsi(data: pd.DataFrame, period: int = 14) -> pd.Series:
    delta = data['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

def calculate_ma(data: pd.DataFrame, window: int) -> pd.Series:
    return data['Close'].rolling(window=window).mean()

def generate_signals(data: pd.DataFrame, rsi_period: int = 14, short_window: int = 50, long_window: int = 200) -> pd.DataFrame:
    data = data.copy()
    if len(data) < long_window:
        logger.warning(f"Data length ({len(data)}) is less than long window ({long_window}). Cannot generate signals.")
        data['Signal'] = 0
        return data
    data['RSI'] = calculate_rsi(data, period=rsi_period)
    data['Short_MA'] = calculate_ma(data, window=short_window)
    data['Long_MA'] = calculate_ma(data, window=long_window)
    data['Signal'] = 0
    logger.info(f"Generating signals for {data.index[0].date()} to {data.index[-1].date()}")
    # Buy: RSI < 30 and short_ma > long_ma
    for i in range(long_window, len(data)):
        rsi_value = data['RSI'].iloc[i]
        short_ma = data['Short_MA'].iloc[i]
        long_ma = data['Long_MA'].iloc[i]
        logger.info(f"Date: {data.index[i].date()}, RSI: {rsi_value:.2f}, Short MA: {short_ma:.2f}, Long MA: {long_ma:.2f}")
        if rsi_value < 30 and short_ma > long_ma:
            data.at[data.index[i], 'Signal'] = 1  # Buy
            logger.info(f"Buy signal on {data.index[i].date()} | Close: {data['Close'].iloc[i]:.2f}")
        # Sell: RSI > 70 or short_ma < long_ma
        elif rsi_value > 70 or short_ma < long_ma:
            data.at[data.index[i], 'Signal'] = -1  # Sell
            logger.info(f"Sell signal on {data.index[i].date()} | Close: {data['Close'].iloc[i]:.2f}")
    return data

def backtest_strategy(data: pd.DataFrame, initial_capital: float = 100000, rsi_period: int = 14, short_window: int = 50, long_window: int = 200) -> dict:
    if data is None or data.empty:
        logger.warning("Input data is empty. Skipping backtest.")
        return {
            'final_capital': initial_capital,
            'pnl': 0,
            'trades': [],
            'history': data
        }
    data = generate_signals(data, rsi_period=rsi_period, short_window=short_window, long_window=long_window)
    capital = initial_capital
    position = 0
    entry_price = 0
    trades = []
    for i, row in data.iterrows():
        # Ensure row['Signal'] is a scalar, not a Series
        signal = row['Signal'] if not isinstance(row['Signal'], pd.Series) else row['Signal'].item()
        if signal == 1 and position == 0:
            position = capital // row['Close']
            entry_price = row['Close']
            capital -= position * entry_price
            trades.append({'date': i, 'type': 'BUY', 'price': entry_price, 'shares': position})
            logger.info(f"Executed BUY: {position} shares at {entry_price:.2f} on {i.date()}")
        elif signal == -1 and position > 0:
            capital += position * row['Close']
            trades.append({'date': i, 'type': 'SELL', 'price': row['Close'], 'shares': position})
            logger.info(f"Executed SELL: {position} shares at {row['Close']:.2f} on {i.date()}")
            position = 0
    # If holding at the end, sell at last price
    if position > 0:
        capital += position * data['Close'].iloc[-1]
        trades.append({'date': data.index[-1], 'type': 'SELL', 'price': data['Close'].iloc[-1], 'shares': position})
        logger.info(f"Final SELL: {position} shares at {data['Close'].iloc[-1]:.2f} on {data.index[-1].date()}")
    pnl = capital - initial_capital
    return {
        'final_capital': capital,
        'pnl': pnl,
        'trades': trades,
        'history': data
    }
