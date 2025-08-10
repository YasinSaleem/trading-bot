
import pandas as pd
from utils.logger import get_logger

logger = get_logger(__name__)

def calculate_pnl(trades: list) -> pd.DataFrame:
    """
    Calculate P&L for each trade and cumulative P&L.
    trades: list of dicts with 'type', 'price', 'shares', 'date'.
    Returns a DataFrame with trade details and P&L.
    """
    records = []
    position = 0
    entry_price = 0
    for trade in trades:
        if trade['type'] == 'BUY':
            position = trade['shares']
            entry_price = trade['price']
            records.append({**trade, 'pnl': 0})
        elif trade['type'] == 'SELL' and position > 0:
            pnl = (trade['price'] - entry_price) * position
            records.append({**trade, 'pnl': pnl})
            position = 0
    df = pd.DataFrame(records)
    df['cum_pnl'] = df['pnl'].cumsum()
    logger.info("Calculated P&L for trades.")
    return df

def calculate_win_ratio(trades: list) -> float:
    """
    Calculate win ratio from trade list.
    """
    wins = 0
    total = 0
    position = 0
    entry_price = 0
    for trade in trades:
        if trade['type'] == 'BUY':
            position = trade['shares']
            entry_price = trade['price']
        elif trade['type'] == 'SELL' and position > 0:
            pnl = (trade['price'] - entry_price) * position
            if pnl > 0:
                wins += 1
            total += 1
            position = 0
    win_ratio = wins / total if total > 0 else 0
    logger.info(f"Win ratio: {win_ratio:.2f}")
    return win_ratio

def summarize_portfolio(trades: list, initial_capital: float) -> dict:
    """
    Summarize portfolio analytics for reporting and Google Sheets logging.
    """
    pnl_df = calculate_pnl(trades)
    win_ratio = calculate_win_ratio(trades)
    final_capital = initial_capital + pnl_df['pnl'].sum() if not pnl_df.empty else initial_capital
    summary = {
        'Initial Capital': initial_capital,
        'Final Capital': final_capital,
        'Total PnL': final_capital - initial_capital,
        'Win Ratio': win_ratio,
        'Total Trades': len([t for t in trades if t['type'] == 'SELL'])
    }
    logger.info(f"Portfolio summary: {summary}")
    return summary, pnl_df
