import pandas as pd
import yfinance as yf
from ta.trend import EMAIndicator, SMAIndicator
from ta.volatility import BollingerBands
from ta.volume import MFIIndicator
from ta.momentum import RSIIndicator
from sklearn.model_selection import train_test_split
from sklearn.svm import SVR
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from datetime import datetime, timedelta



def predict_stock_price(symbol):
    # Fetch historical stock data
    #symbol = 'TSLA'
    start_date = '2024-02-01'
    end_date = datetime.now().strftime('%Y-%m-%d')

    # Get current stock price using yfinance
    symbol = symbol.upper()
    ticker = yf.Ticker(symbol)
    current_stock_price = ticker.history(period='1d')['Close'].iloc[-1]

    # Fetch historical stock data for technical indicators
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
    stock_data['MFI'] = MFIIndicator(stock_data['High'], stock_data['Low'], stock_data['Close'], stock_data['Volume'],
                                     window=mfi_period).money_flow_index()

    # Create binary labels for price movement (1: Up, 0: Down) in the next 5 minutes
    prediction_window_minutes = 5
    stock_data['Price_Up_5M'] = (
                stock_data['Open'].shift(-int(prediction_window_minutes / 5)) > stock_data['Open']).astype(int)

    # Drop NaN values in the last row
    stock_data.dropna(inplace=True)
    stock_data['Percentage_Change'] = stock_data[
                                          'Open'].pct_change() * 100  # Percentage change from the previous 5 minutes

    # Features used to predict percentage change
    features = stock_data[['RSI', 'Bollinger_High', 'MFI']]
    target_percent = stock_data['Percentage_Change'].shift(-1).dropna()  # Drop NaN values

    # Ensure lengths match before splitting
    max_len = min(len(features), len(target_percent))
    X_train, X_test, y_train, y_test = train_test_split(features[:max_len], target_percent[:max_len], test_size=0.2,
                                                        random_state=42)

    # Standardize features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    # SVR model for regression
    svr_model = SVR(kernel='rbf', C=1, gamma='scale')
    svr_model.fit(X_train_scaled, y_train)

    # Random Forest model
    rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
    rf_model.fit(X_train_scaled, y_train)

    # Predicted percentage change for the next 5 minutes
    current_data = features.iloc[-1].values.reshape(1, -1)
    current_data_scaled = scaler.transform(current_data)
    predicted_percentage_change_svr = svr_model.predict(current_data_scaled)[0]
    predicted_percentage_change_rf = rf_model.predict(current_data_scaled)[0]

    # Combine predictions using stacking ensemble
    predicted_percentage_change_ensemble = (predicted_percentage_change_svr + predicted_percentage_change_rf) / 2

    # Current time
    current_time = datetime.now().strftime('%H:%M:%S')

    # Calculate time 5 minutes later
    future_time = (datetime.now() + timedelta(minutes=5)).strftime('%H:%M:%S')

    # Predicted percentage change for the next 5 minutes
    current_data = features.iloc[-1].values.reshape(1, -1)
    current_data_scaled = scaler.transform(current_data)
    predicted_percentage_change = svr_model.predict(current_data_scaled)[0]

    # Predicted stock price for the next 5 minutes
    predicted_stock_price_next_5M = current_stock_price * (1 + predicted_percentage_change_ensemble / 100)

    # Print current stock price and prediction
    print(f"Current Time: {current_time}")
    print(f"Time 5 Minutes Later: {future_time}")
    print(f"Current Stock Price ({datetime.now()}): {current_stock_price}")
    if predicted_percentage_change > 0:
        print(f"Predicted: Price will go up in the next {prediction_window_minutes} minutes.")
    else:
        print(f"Predicted: Price will go down in the next {prediction_window_minutes} minutes.")
    print(
        f"Predicted Percentage Change for the next {prediction_window_minutes} minutes: {predicted_percentage_change:.4f}%")
    print(f"Predicted Stock Price in the next {prediction_window_minutes} minutes: {predicted_stock_price_next_5M:.4f}")

    result = {
        "current_time": current_time,
        "future_time": future_time,
        "current_stock_price": current_stock_price,
        "predicted_percentage_change": predicted_percentage_change,
        "predicted_stock_price_next_5M": predicted_stock_price_next_5M
    }

    return result
