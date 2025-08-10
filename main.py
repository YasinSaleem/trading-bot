
import sys
import pandas as pd
from data.fetcher import get_stock_data
from strategies.rsi_ma_strategy import backtest_strategy
from ml.predictor import prepare_features, train_and_evaluate
from sheets.google_sheets import get_gsheet_client, log_trade, update_summary, log_pnl, log_predictions
from analytics.portfolio import summarize_portfolio
from config import NIFTY50_TICKERS, START_DATE, END_DATE, INITIAL_CAPITAL, GOOGLE_SHEETS_CREDENTIALS, GOOGLE_SHEET_NAME, RSI_PERIOD, SHORT_WINDOW, LONG_WINDOW
from utils.logger import get_logger

logger = get_logger("main")

def main():
    logger.info("Starting Algo Trading Bot workflow...")
    all_trades = []
    all_pnls = []
    all_predictions = [] # New list to store all predictions
    sheet = None
    try:
        # Connect to Google Sheets
        sheet_client = get_gsheet_client(GOOGLE_SHEETS_CREDENTIALS)
        sheet = sheet_client.open(GOOGLE_SHEET_NAME)
    except Exception as e:
        logger.warning(f"Google Sheets not available: {e} (type: {type(e)})")
        import traceback
        logger.warning(traceback.format_exc())

    for ticker in NIFTY50_TICKERS:
        logger.info(f"Processing {ticker}")
        # Fetch data
        data = get_stock_data(ticker, START_DATE, END_DATE)
        if data.empty:
            logger.warning(f"No data for {ticker}, skipping.")
            continue
        # Backtest strategy
        result = backtest_strategy(data, initial_capital=INITIAL_CAPITAL, rsi_period=RSI_PERIOD, short_window=SHORT_WINDOW, long_window=LONG_WINDOW)
        trades = result['trades']
        if not trades:
            logger.warning(f"No trades for {ticker}, skipping analytics/logging.")
            continue
        all_trades.extend(trades)
        # Portfolio analytics
        summary, pnl_df = summarize_portfolio(trades, INITIAL_CAPITAL)
        all_pnls.append(pnl_df)
        # Log trades and analytics to Google Sheets
        if sheet:
            for trade in trades:
                log_trade(sheet, trade, tab_name=f"{ticker}_TradeLog")
            update_summary(sheet, summary, tab_name=f"{ticker}_Summary")
            log_pnl(sheet, pnl_df, tab_name=f"{ticker}_PnL")
        # ML prediction (bonus)
        try:
            features_df = prepare_features(data)
            _, acc_dt, preds_dt, X_test_dt, y_test_dt = train_and_evaluate(features_df, model_type='decision_tree')
            _, acc_lr, preds_lr, X_test_lr, y_test_lr = train_and_evaluate(features_df, model_type='logistic_regression')
            logger.info(f"{ticker} ML accuracy - DecisionTree: {acc_dt:.4f}, LogisticRegression: {acc_lr:.4f}")

            # Store predictions for logging
            for j in range(len(preds_dt)):
                all_predictions.append({
                    'Ticker': ticker,
                    'Date': X_test_dt.index[j].strftime('%Y-%m-%d'),
                    'Actual': int(y_test_dt.iloc[j]),
                    'Predicted': int(preds_dt[j])
                })
        except Exception as e:
            logger.warning(f"ML prediction failed for {ticker}: {e}")

    # Overall analytics
    if all_trades:
        overall_summary, overall_pnl_df = summarize_portfolio(all_trades, INITIAL_CAPITAL)
        logger.info(f"Overall Portfolio Summary: {overall_summary}")
        if sheet:
            update_summary(sheet, overall_summary, tab_name="Overall_Summary")
            log_pnl(sheet, overall_pnl_df, tab_name="Overall_PnL")
        
        # Log ML predictions
        if sheet and all_predictions:
            log_predictions(sheet, pd.DataFrame(all_predictions), tab_name="ML_Predictions")
    else:
        logger.warning("No trades generated for any ticker. Skipping overall analytics.")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        sys.exit(1)
