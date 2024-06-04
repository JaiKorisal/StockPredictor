'use client'

import { AiOutlineSearch } from 'react-icons/ai'
import Link from 'next/link'
import React, {FormEvent, useState} from 'react'
import {useRouter} from 'next/router'
import { Line } from 'react-chartjs-2';
import { Chart as ChartJS, CategoryScale, LinearScale, LineElement, PointElement, Tooltip, Legend } from 'chart.js';



interface PredictionResult {
  current_time: string;
  future_time: string;
  current_stock_price: number;
  predicted_percentage_change: number;
  predicted_stock_price_next_5M: number;
}

interface StockData {
  "Symbol": string[];
  "Prediction Date": string[];
  "Today Opening": number[];
  "Predicted Opening Price": number[];
}

interface LstmPrediction {
  Predicted_Opening_Price_LSTM: number;
}

ChartJS.register(CategoryScale, LinearScale, LineElement, PointElement, Tooltip, Legend);

const page = () => {
  const [predictionResult, setPredictionResult] = useState<PredictionResult | null>(null);
  const [stockData, setStockData] = useState<StockData | null>(null);
  const [lstmPrediction, setLstmPrediction] = useState<LstmPrediction | null>(null);
  const [stockSymbol, setStockSymbol] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [historicalData, setHistoricalData] = useState({ labels: [], stockPrices: [] });

  const [predictions, setPredictions] = useState({
    fiveMinutePrediction: null,
    nextDayOpeningPrediction: null,
    lstmPrediction: null
  });

  const fetchPredictions = async (symbol : string) => {
    try {
        const fiveMinute = await fetch(`/api/predict-stock?symbol=${symbol}`).then(res => res.json());
        const nextDayOpening = await fetch(`/api/predict-opening-rbf?symbol=${symbol}`).then(res => res.json());
        const lstm = await fetch(`/api/predict-lstm?symbol=${symbol}`).then(res => res.json());

        setPredictions({
            fiveMinutePrediction: fiveMinute,
            nextDayOpeningPrediction: nextDayOpening,
            lstmPrediction: lstm
        });
    } catch (error) {
        console.error('Error fetching prediction data:', error);
    }
  };

  const fetchHistoricalData = async (symbol: string): Promise<void> => {
    try {
      const response = await fetch(`/api/get-historical-data?symbol=${symbol}`);
      const data = await response.json();
      // Assuming data is structured with { labels: string[], stockPrices: number[] }
      setHistoricalData({
        labels: data.labels,
        stockPrices: data.stockPrices,
      });
    } catch (error) {
      console.error('Error fetching historical data:', error);
    }
  };

  const handleSearch = async (e: FormEvent) => {
    e.preventDefault();
    fetchHistoricalData(stockSymbol);
    fetchPredictions(stockSymbol);
    setLoading(true);
    setError(null);

    console.log('Prediction Result:', predictionResult);
    console.log('Stock Data:', stockData);
    console.log('LSTM Prediction:', lstmPrediction);
    try {
      const predictionResponse = await fetch(`/api/predict-stock?symbol=${stockSymbol}`);
      const stockDataResponse = await fetch(`/api/predict-opening-rbf?symbol=${stockSymbol}`);
      const lstmPredictionResponse = await fetch(`/api/predict-lstm?symbol=${stockSymbol}`);

      if (!predictionResponse.ok || !stockDataResponse.ok || !lstmPredictionResponse) {
        throw new Error('Failed to fetch prediction');
      }
      const predictionData = await predictionResponse.json();
      const stockData = await stockDataResponse.json();
      const lstmPrediction = await lstmPredictionResponse.json();

      setPredictionResult(predictionData);
      setStockData(stockData);
      setLstmPrediction(lstmPrediction);

    } catch (error) {
      console.error('Error fetching prediction:', error);
      setError('Failed to fetch prediction. Please try again.');
    } finally {
      setLoading(false);
    }
  };
  const data = {
    labels: [...historicalData.labels,'Next 5 Minutes', 'Next Day Opening RBF & SVM', 'LSTM Prediction'],
    datasets: [
      {
        label: 'Stock Price',
        data: historicalData.stockPrices,
        borderColor: 'rgb(75, 192, 192)',
        backgroundColor: 'rgba(75, 192, 192, 0.5)',
      },
      {
        label: 'Predictions',
        data: [
            ...new Array(historicalData.stockPrices.length).fill(NaN), // Fill with NaN up to predictions
            predictionResult?.predicted_stock_price_next_5M,
            stockData ? stockData["Predicted Opening Price"][0] : NaN,
            lstmPrediction ? lstmPrediction.Predicted_Opening_Price_LSTM : NaN
        ],
        borderColor: 'rgb(255, 99, 132)',
        backgroundColor: 'rgba(255, 99, 132, 0.5)',
        pointStyle: 'triangle',
        borderDash: [5, 5]
      }
    ]
  };



  return (
    <main className='flex min-h-screen flex-col items-center justify-between p-24'>
      <form className='flex flex-col items-center' onSubmit={handleSearch}>
        <div className='z-10 w-full max-w-5xl items-center justify-between font-mono text-sm lg:flex'>
          <Link className='font-mono font-bold' href='/search'>
            Settings
          </Link>
        </div>
        <div className={`mb-3 text-2xl font-bold text-center`}>
          <h1 className={`mb-3 text-2xl font-semibold`}>
            Pick a Stock
          </h1>
        </div>
        <div className='w-[500px] relative'>
          <input
              type='search'
              placeholder='Type Here'
              className='w-full p-4 rounded-full bg-slate-800 text-white'
              value={stockSymbol}
              onChange={(e) => setStockSymbol(e.target.value)}
          />
          <button type='submit' className='absolute right-1 top-1/2 -translate-y-1/2 p-4 bg-slate-400 rounded-full'>
            <AiOutlineSearch/>
          </button>
        </div>
        <div className={`mb-3 text-2xl font-bold text-center mt-10`}>
          <h1>Examples:</h1>
          <div className={`mb-3 text-2xl font-semibold text-center mt-3`}>
            <h2>TSLA</h2>
            <h2>BTC-USD</h2>
            <h2>NVDA</h2>
          </div>
        </div>

        {predictionResult && (
          <div className="border rounded-lg p-4 mb-8">
            <h1 className="mb-2 text-xl font-semibold">Prediction Result for the next 5 Minutes</h1>
            {loading && <p>Loading...</p>}
            {error && <p>{error}</p>}
            {predictionResult && (
                <div>
                  <p>Current Time: {predictionResult.current_time}</p>
                  <p>Time 5 Minutes Later: {predictionResult.future_time}</p>
                  <p>Current Stock Price: {predictionResult.current_stock_price}</p>
                  {predictionResult.predicted_percentage_change > 0 ? (
                      <p>Predicted: Price will go up in the next 5 minutes.</p>
                  ) : (
                      <p>Predicted: Price will go down in the next 5 minutes.</p>
                  )}
                  <p>Predicted Percentage Change for the next 5
                    minutes: {predictionResult.predicted_percentage_change.toFixed(4)}%</p>
                  <p>Predicted Stock Price in the next 5
                    minutes: {predictionResult.predicted_stock_price_next_5M.toFixed(4)}</p>
                </div>
            )}
          </div>
        )}

        {stockData && (
          <div className="border rounded-lg p-4 mb-8">
            <h1 className="mb-2 text-xl font-semibold">Prediction Result for tomorrow's opening (RBF & SVM)</h1>
            {stockData && (
                <div>
                  <p> Stock: {stockData["Symbol"]}</p>
                    <p>Prediction Date: {stockData["Prediction Date"] && stockData["Prediction Date"][0]}</p>
                    <p>Today's Opening Price: {stockData["Today Opening"] && stockData["Today Opening"][0]}</p>
                    <p>Predicted Opening Price
                      for {stockData["Prediction Date"] && stockData["Prediction Date"][0]}: {stockData["Predicted Opening Price"] && stockData["Predicted Opening Price"][0]}</p>
                </div>
            )}
          </div>
        )}

        {lstmPrediction && (
            <div className="border rounded-lg p-4 mb-8">
              <h1 className="mb-2 text-xl font-semibold">LSTM Prediction</h1>
              {lstmPrediction && (
              <div>
                <p>Predicted Opening Price : {lstmPrediction.Predicted_Opening_Price_LSTM}</p>
              </div>
              )}
            </div>
        )}

        {historicalData.labels.length > 0 && predictionResult && stockData && lstmPrediction &&  (
        <div style={{ width: '80%' }}>
          <Line data={data} />
        </div>
      )}


        <div className='mb-32 grid text-center lg:mb-0 lg:grid-cols-3 lg:text-left'>
          <a
              className='group rounded-lg border border-transparent px-5 py-4 transition-colors hover:border-gray-300 hover:bg-gray-100 hover:dark:border-neutral-700 hover:dark:bg-neutral-800/30'
              target='_blank'
              rel='noopener noreferrer'
          >
            <h2 className={`mb-3 text-2xl font-semibold`}>
              Search History<span>-&gt;</span>
              </h2>
              <p className={`m-0 max-w-[30ch] text-sm opacity-50`}>
                View your past questions here.
              </p>
            </a>
            <a
                href='/Dashboard'
                className='group rounded-lg border border-transparent px-5 py-4 transition-colors hover:border-gray-300 hover:bg-gray-100 hover:dark:border-neutral-700 hover:dark:bg-neutral-800/30'
                target='_blank'
                rel='noopener noreferrer'
            >
              <h2 className={`mb-3 text-2xl font-semibold`}>
                Dashboard{' '}
                <span
                    className='inline-block transition-transform group-hover:translate-x-1 motion-reduce:transform-none'>
                -&gt;
              </span>
              </h2>
              <p className={`m-0 max-w-[30ch] text-sm opacity-50`}>
                View the Previous Stock Predictions here.
              </p>
            </a>
            <a
                className='group rounded-lg border border-transparent px-5 py-4 transition-colors hover:border-gray-300 hover:dark:border-neutral-700 hover:dark:bg-neutral-800/30'
                target='_blank'
                rel='noopener noreferrer'
            >
              <h2 className={`mb-3 text-2xl font-semibold`}>
                Calendar{' '}
                <span
                    className='inline-block transition-transform group-hover:translate-x-1 motion-reduce:transform-none'>
                -&gt;
              </span>
              </h2>
              <p className={`m-0 max-w-[30ch] text-sm opacity-50`}>
                View what's coming up here.
              </p>
            </a>
          </div>
      </form>
    </main>
  );
};

export default page;