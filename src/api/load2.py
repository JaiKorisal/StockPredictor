import os
import sys
import pandas as pd
import datetime as dt
import matplotlib.pyplot as plt
import numpy as np
import urllib.request, json
import ta
from ta.utils import dropna
from sklearn.preprocessing import MinMaxScaler
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.optimizers import Adam
from tensorflow.keras import layers
from keras.models import Sequential
from keras.models import load_model
from keras.layers import Dense, LSTM


def predict_lstm(symbol):
    loaded_model = tf.keras.models.load_model(
        'C:\\Users\\Jai Korisal\\PycharmProjects\\StockPrediction\\WebApp\\src\\api\\b.keras')
    parameter = str(sys.argv[1])
    # print ('Enter the stock ticker')
    # ticker = input()
    ticker = parameter
    # print ('Enter technical indicator')
    # TI = input()
    api_key: str = 'xxxxxxxxxxxxxxxx'
    url_string = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={}&apikey={}'.format(ticker,
                                                                                                           api_key)
    file_to_save = 'stock-%s.csv' % ticker

    with urllib.request.urlopen(url_string) as url:
        data = json.loads(url.read().decode())
        data = data['Time Series (Daily)']
        df = pd.DataFrame(columns=['Date', 'Low', 'High', 'Close', 'Open'])
        for k, v in data.items():
            date = dt.datetime.strptime(k, '%Y-%m-%d')
            data_row = [date.date(), float(v['3. low']), float(v['2. high']), float(v['4. close']), float(v['1. open'])]
            df.loc[-1, :] = data_row
            df.index = df.index + 1
    print('saved to %s' % file_to_save)
    df.to_csv(file_to_save)
    print(type(df['Date'].values))
    df = df.loc[df['Date'] > dt.date(2023, 1, 1)]

    df.dropna()  # clean out any missing or bad values
    df = df[::-1]
    rsi_period = 14
    # df['RSI'] = ta.momentum.RSIIndicator (df['Close'], window = rsi_period).rsi()
    ema_short_period = 12
    ema_long_period = 26
    df['EMA_Short'] = ta.trend.EMAIndicator(df['Close'], window=ema_short_period).ema_indicator()
    df['EMA_Long'] = ta.trend.EMAIndicator(df['Close'], window=ema_long_period).ema_indicator()
    df['BBMavg'] = ta.volatility.BollingerBands(close=df['Close'], window=20, window_dev=2).bollinger_mavg()
    # df['ROC'] = ta.momentum.roc (df['Close'])      #no longer considered useful
    # df['PPO'] = ta.momentum.ppo (df['Close'])      #same with this
    df['SMA'] = ta.trend.SMAIndicator(df['Close'], window=20).sma_indicator()
    df['Stochastic'] = ta.momentum.StochasticOscillator(df['Close'], df['High'], df['Low']).stoch()
    df['ATR'] = ta.volatility.AverageTrueRange(df['High'], df['Low'], df['Close']).average_true_range()

    indicators = ['Close', 'EMA_Short', 'EMA_Long', 'BBMavg', 'SMA', 'Stochastic', 'ATR']
    result = []

    for term in indicators:
        data = df.filter([term])
        dataset = data.values
        training_data_len = len(dataset) - 1
        scaler = MinMaxScaler(feature_range=(0, 1))
        scaled_data = scaler.fit_transform(dataset)
        train_data = scaled_data[0:int(training_data_len), :]
        x_train = []
        y_train = []

        for i in range(1, len(train_data)):
            x_train.append(train_data[i - 1:i, 0])
            y_train.append(train_data[i, 0])

        x_train, y_train = np.array(x_train), np.array(y_train)
        x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))

        test_data = scaled_data[training_data_len:, :]
        x_test = []
        y_test = dataset[training_data_len:, :]
        x_test.append(test_data[:i, 0])

        x_test = np.array(x_test)
        x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1))
        predictions = loaded_model.predict(x_test)
        predictions = scaler.inverse_transform(predictions)
        rmse = np.sqrt(np.mean(((predictions - y_test) ** 2)))
        train = data[:training_data_len]
        valid = data[training_data_len:]
        valid['Predictions'] = predictions
        result.append(valid)

    ##print ("Accuracy of all indicators")
    ##print ("__________________________")
    nextPrice = df.filter(['Open'])
    nextPrice = nextPrice.values
    nextPrice = nextPrice[-1]
    ##print ("Opening next price: %f" % (nextPrice))

    for x in result:
        if x.columns[0] == 'ATR':
            y = x['Predictions'].values + nextPrice[-1]
            ##print(x.columns[0], "=", y)
            if y > nextPrice:
                pass
                ##print((nextPrice / y) * 100, "%")
            else:
                pass
                ##print((y / nextPrice) * 100, "%")
        elif x.columns[0] == 'Stochastic':
            y = nextPrice[-1] - x['Predictions'].values
            ##print(x.columns[0], "=", y)
            if y > nextPrice:
                pass
                ##print((nextPrice / y) * 100, "%")
            else:
                pass
                ##print((y / nextPrice) * 100, "%")
        else:
            pass
            ##print (x.columns[0], "=", x['Predictions'].values)
            ##print ((x['Predictions'].values / nextPrice) * 100, "%")

    ##plt.figure (figsize = (16, 6))                                    #basic plot that puts the predicted price next to real price
    ##plt.title ('LSTM model')
    ##plt.xlabel ('Day #', fontsize = 16)
    ##plt.ylabel ('Price', fontsize = 16)
    ##plt.plot (df['Open'], marker = '.', markersize = 4)
    ##for y in result:
    ##    if y.columns[0] == 'ATR':
    ##        plt.plot (y['Predictions'] + nextPrice[-1], marker = '.', markersize = 4)
    ##    elif y.columns[0] == 'Stochastic':
    ##        plt.plot (nextPrice[-1] - y['Predictions'], marker = '.', markersize = 4)
    ##    else:
    ##        plt.plot (y['Predictions'], marker = '.', markersize = 4)
    ##plt.legend (['Train', 'Only close', 'EMA_Short', 'EMA_Long', 'BBMavg', 'SMA', 'Stochastic', 'ATR'], loc = 'lower right')
    ##plt.show()
    var = 0
    symbol = sys.argv[1]  # You can pass the symbol as a command-line argument
    prediction = predict_lstm(symbol)
    print("{:0.2f}".format(prediction))

    return prediction



