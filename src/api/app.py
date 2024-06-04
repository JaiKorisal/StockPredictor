from datetime import datetime, timedelta  # Import datetime module
from flask import Flask, jsonify, request
from RBFMinute import predict_stock_price
from loadLSTM_all_indicators import predict_lstm
from OpeningRBFPred import predict_stock_opening
import yfinance as yf


app = Flask(__name__)

#RBFMinute.py
@app.route('/api/predict-stock', methods=['GET'])
def predict_stock():
    symbol = request.args.get('symbol')
    if not symbol:
        return jsonify({"error": "No symbol provided"}), 400
    try:
        prediction = predict_stock_price(symbol)
        return jsonify(prediction)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

#OpeningRBFPred.py
@app.route('/api/predict-opening-rbf', methods=['GET'])
def predict_opening_rbf_route():
    symbol = request.args.get('symbol')
    if not symbol:
        return jsonify({"error": "No symbol provided"}), 400
    try:
        prediction = predict_stock_opening(symbol)
        return jsonify(prediction)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


#loadLSTM_all_indicators.py
@app.route('/api/predict-lstm', methods=['GET'])
def predict_lstm_route():
    symbol = request.args.get('symbol')
    if not symbol:
        return jsonify({"error": "No symbol provided"}), 400
    try:
        prediction = predict_lstm(symbol)
        return jsonify(prediction)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/get-historical-data', methods=['GET'])
def get_historical_data():
    symbol = request.args.get('symbol')
    if not symbol:
        return jsonify({"error": "No symbol provided"}), 400

    try:
        # Calculate date range for the last 5 days
        end_date = datetime.now()
        start_date = end_date - timedelta(days=50)

        # Fetch historical stock data
        data = yf.download(symbol, start=start_date.strftime('%Y-%m-%d'), end=end_date.strftime('%Y-%m-%d'))

        # Prepare the response data
        historical_data = {
            "labels": [date.strftime('%Y-%m-%d') for date in data.index],
            "stockPrices": data['Close'].tolist()
        }
        return jsonify(historical_data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5328)
