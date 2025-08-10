
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from utils.logger import get_logger
import pandas as pd
import numpy as np
import time

logger = get_logger(__name__)

def convert_numpy_types(data):
    if isinstance(data, dict):
        return {k: convert_numpy_types(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [convert_numpy_types(i) for i in data]
    elif isinstance(data, np.integer):
        return int(data)
    elif isinstance(data, np.floating):
        return float(data)
    elif isinstance(data, np.ndarray):
        return data.tolist()
    elif isinstance(data, pd.Timestamp):
        return data.strftime('%Y-%m-%d %H:%M:%S')
    return data

# Set up the Google Sheets API client
def get_gsheet_client(creds_path: str = 'credentials.json'):
    scope = [
        'https://spreadsheets.google.com/feeds',
        'https://www.googleapis.com/auth/drive',
    ]
    creds = ServiceAccountCredentials.from_json_keyfile_name(creds_path, scope)
    client = gspread.authorize(creds)
    return client

def log_trade(sheet, trade_data: dict, tab_name: str = 'Trade Log'):
    """
    Append a trade record to the Trade Log tab.
    trade_data: dict with keys like date, type, price, shares, etc.
    """
    try:
        worksheet = sheet.worksheet(tab_name)
    except gspread.exceptions.WorksheetNotFound:
        worksheet = sheet.add_worksheet(title=tab_name, rows="1000", cols="10")
        worksheet.append_row(list(trade_data.keys()))
    
    trade_data = convert_numpy_types(trade_data)

    try:
        worksheet.append_row(list(trade_data.values()))
        logger.info(f"Logged trade: {trade_data}")
        time.sleep(1)
    except Exception as e:
        logger.error(f"Failed to log trade to {tab_name}: {e}")
        import traceback
        logger.error(traceback.format_exc())


def update_summary(sheet, summary_data: dict, tab_name: str = 'Summary'):
    """
    Update summary stats (P&L, win ratio, etc.) in the Summary tab.
    summary_data: dict with summary stats.
    """
    try:
        worksheet = sheet.worksheet(tab_name)
    except gspread.exceptions.WorksheetNotFound:
        worksheet = sheet.add_worksheet(title=tab_name, rows="100", cols="10")

    summary_data = convert_numpy_types(summary_data)

    try:
        worksheet.clear()
        worksheet.append_row(list(summary_data.keys()))
        worksheet.append_row(list(summary_data.values()))
        logger.info(f"Updated summary: {summary_data}")
        time.sleep(1)
    except Exception as e:
        logger.error(f"Failed to update summary in {tab_name}: {e}")
        import traceback
        logger.error(traceback.format_exc())


def log_pnl(sheet, pnl_data: pd.DataFrame, tab_name: str = 'PnL'):
    """
    Log P&L history to the PnL tab.
    pnl_data: pandas DataFrame with P&L history.
    """
    try:
        worksheet = sheet.worksheet(tab_name)
    except gspread.exceptions.WorksheetNotFound:
        worksheet = sheet.add_worksheet(title=tab_name, rows="1000", cols="10")
    
    pnl_data = pnl_data.copy()
    if 'date' in pnl_data.columns:
        pnl_data['date'] = pnl_data['date'].dt.strftime('%Y-%m-%d %H:%M:%S')

    try:
        worksheet.clear()
        worksheet.append_row(pnl_data.columns.tolist())
        for row in pnl_data.values.tolist():
            worksheet.append_row(row)
            time.sleep(1)
        logger.info(f"Logged PnL data to {tab_name} tab.")
    except Exception as e:
        logger.error(f"Failed to log PnL data to {tab_name}: {e}")
        import traceback
        logger.error(traceback.format_exc())

def log_predictions(sheet, predictions_df: pd.DataFrame, tab_name: str = 'ML_Predictions'):
    """
    Log ML predictions to the ML_Predictions tab.
    predictions_df: pandas DataFrame with ML predictions.
    """
    try:
        worksheet = sheet.worksheet(tab_name)
    except gspread.exceptions.WorksheetNotFound:
        worksheet = sheet.add_worksheet(title=tab_name, rows="1000", cols="10")
    
    try:
        worksheet.clear()
        worksheet.append_row(predictions_df.columns.tolist())
        for row in predictions_df.values.tolist():
            worksheet.append_row(row)
            time.sleep(1)
        logger.info(f"Logged ML predictions to {tab_name} tab.")
    except Exception as e:
        logger.error(f"Failed to log ML predictions to {tab_name}: {e}")
        import traceback
        logger.error(traceback.format_exc())
