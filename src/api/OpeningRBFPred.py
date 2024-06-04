import pandas as pd
import pytz
import yfinance as yf
from ta.trend import EMAIndicator, SMAIndicator, MACD
from ta.volatility import BollingerBands
from ta.volume import MFIIndicator
from ta.momentum import RSIIndicator, AwesomeOscillatorIndicator, StochasticOscillator
from sklearn.model_selection import train_test_split
from sklearn.svm import SVR
from sklearn.preprocessing import StandardScaler
from datetime import datetime, timedelta
import os

def predict_stock_opening(symbol):
    # Fetch historical stock data
    symbol = symbol.upper()
    today_data = yf.Ticker(symbol).history(period='1d')
    start_date = '2010-01-01'
    end_date = datetime.now().strftime('%Y-%m-%d')

    stock_data = yf.download(symbol, start=start_date, end=end_date)

    # Calculate RSI
    rsi_period = 14
    stock_data['RSI'] = RSIIndicator(stock_data['Open'], window=rsi_period).rsi()

    # Calculate SMA
    sma_period = 20
    stock_data['SMA'] = SMAIndicator(stock_data['Open'], window=sma_period).sma_indicator()

    # Calculate Bollinger High Bands
    bollinger_period = 20
    stock_data['Bollinger_High'] = BollingerBands(stock_data['Open'], window=bollinger_period).bollinger_hband()

    # Calculate MFI
    mfi_period = 14
    stock_data['MFI'] = MFIIndicator(stock_data['High'], stock_data['Low'], stock_data['Close'], stock_data['Volume'], window=mfi_period).money_flow_index()

    # Calculate EMA
    ema_short_period = 12
    ema_long_period = 26
    stock_data['EMA_Short'] = EMAIndicator(stock_data['Open'], window=ema_short_period).ema_indicator()
    stock_data['EMA_Long'] = EMAIndicator(stock_data['Open'], window=ema_long_period).ema_indicator()

    # Calculate MACD
    macd = MACD(stock_data['Open'], window_slow=26, window_fast=12)
    stock_data['MACD'] = macd.macd()

    # Calculate Awesome Oscillator
    stock_data['Awesome_Oscillator'] = AwesomeOscillatorIndicator(stock_data['High'], stock_data['Low']).awesome_oscillator()

    # Calculate Stochastic Oscillator
    stock_data['Stochastic_Oscillator'] = StochasticOscillator(stock_data['High'], stock_data['Low'], stock_data['Close']).stoch()
    # Create binary labels for price movement (1: Up, 0: Down) in the next 24 hours
    stock_data['Price_Up_24H'] = (stock_data['Open'].shift(-1) > stock_data['Open']).astype(int)

    # Drop NaN values in the last row
    stock_data = stock_data.dropna()
    stock_data['Percentage_Change'] = stock_data['Open'].pct_change() * 100  # Percentage change from the previous day

    # Features used to predict percentage change
    features = stock_data[['RSI', 'MACD', 'MFI', 'Awesome_Oscillator', 'Stochastic_Oscillator']]
    target_percent = stock_data['Percentage_Change'].shift(-1).dropna()  # Drop NaN values

    # Ensure lengths match before splitting
    max_len = min(len(features), len(target_percent))
    X_train, X_test, y_train, y_test = train_test_split(features[:max_len], target_percent[:max_len], test_size=0.2, random_state=42)

    # Standardize features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    # SVR model for regression
    svr_model = SVR(kernel='rbf', C=1, gamma='scale')
    svr_model.fit(X_train_scaled, y_train)

    # Current stock price
    today_opening_price = today_data['Open'].iloc[0]

    # Predicted percentage change for the next 24 hours
    current_data = features.iloc[-1].values.reshape(1, -1)
    current_data_scaled = scaler.transform(current_data)
    predicted_percentage_change = svr_model.predict(current_data_scaled)[0]

    # Calculate tomorrow's date
    tomorrow_date = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')

    # Predicted stock price for tomorrow
    predicted_stock_price_tomorrow = today_opening_price * (1 + predicted_percentage_change / 100)

    print(f"\nSymbol: {symbol}")
    print(f"Current Stock Opening Price ({end_date}): {today_opening_price}")
    print(f"Predicted Percentage Change for Opening: {predicted_percentage_change:.4f}%")
    print(f"Predicted Stock Opening Price on {tomorrow_date}: {predicted_stock_price_tomorrow:.4f}")

    prediction_output = {
        'Symbol': [symbol],
        'Prediction Date': [tomorrow_date],
        'Today Opening':  [round(today_opening_price, 3)],
        'Predicted Opening Price': [round(predicted_stock_price_tomorrow, 3)],
    }

    return prediction_output

