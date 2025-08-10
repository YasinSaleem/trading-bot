
import pandas as pd
import numpy as np
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from utils.logger import get_logger

logger = get_logger(__name__)

def calculate_rsi(data: pd.DataFrame, period: int = 14) -> pd.Series:
    delta = data['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

def calculate_macd(data: pd.DataFrame, fast: int = 12, slow: int = 26, signal: int = 9) -> pd.Series:
    ema_fast = data['Close'].ewm(span=fast, adjust=False).mean()
    ema_slow = data['Close'].ewm(span=slow, adjust=False).mean()
    macd = ema_fast - ema_slow
    signal_line = macd.ewm(span=signal, adjust=False).mean()
    return macd - signal_line

def prepare_features(data: pd.DataFrame) -> pd.DataFrame:
    data = data.copy()
    data['RSI'] = calculate_rsi(data)
    data['MACD'] = calculate_macd(data)
    data['Volume'] = data['Volume']
    # Target: 1 if next day's close > today's, else 0
    data['Target'] = (data['Close'].shift(-1) > data['Close']).astype(int)
    data = data.dropna()
    return data[['RSI', 'MACD', 'Volume', 'Target']]

def train_test_split(data: pd.DataFrame, test_size: float = 0.2):
    split = int(len(data) * (1 - test_size))
    train = data.iloc[:split]
    test = data.iloc[split:]
    return train, test

def train_and_evaluate(data: pd.DataFrame, model_type: str = 'decision_tree'):
    features = ['RSI', 'MACD', 'Volume']
    train, test = train_test_split(data)
    X_train, y_train = train[features], train['Target']
    X_test, y_test = test[features], test['Target']
    if model_type == 'decision_tree':
        model = DecisionTreeClassifier(random_state=42)
    else:
        model = LogisticRegression(max_iter=200)
    model.fit(X_train, y_train)
    preds = model.predict(X_test)
    acc = accuracy_score(y_test, preds)
    logger.info(f"{model_type} accuracy: {acc:.4f}")
    return model, acc, preds, X_test, y_test
