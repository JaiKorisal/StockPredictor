'use client'
import React, { useState, useEffect } from "react";
import { Line } from 'react-chartjs-2';

const StockInfoPage = () => {
  // State to store stock data
  const [stockName, setStockName] = useState(""); //i didnt see any declaration for either of these
  const [stockPrice, setStockPrice] = useState("");
  const [loading, setLoading] = useState(true);

  // Function to fetch stock data
  const fetchStockData = async () => {
    try {
      const symbol = "AAPL"; // Replace with the symbol of the stock you want to fetch
      const response = await fetch("https://query1.finance.yahoo.com/v7/finance/quote?symbols=${symbol}");
                                    //im pretty sure this has to be closed in quotation marks
      const data = await response.json();
      console.log('stdout:',response);
      if (data && data.quoteResponse && data.quoteResponse.result && data.quoteResponse.result.length > 0) {
        const stockInfo = data.quoteResponse.result[0];
        const stockName = stockInfo.longName;
        const stockPrice = stockInfo.regularMarketPrice;
        setStockName(stockName);
        setStockPrice(stockPrice);

      } else {
        setStockName("");
        setStockPrice("");
      }
      setLoading(false);
    } catch (error) {
      console.error("Error fetching stock data:", error);
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchStockData();
  }, []);

  // Sample data for chart (replace with actual data)
  const chartData = {
    labels: ["January", "February", "March", "April", "May", "June", "July"],
    datasets: [
      {
        label: 'Stock Price',
        data: [65, 59, 80, 81, 56, 55, 40], // Sample data
        fill: false,
        borderColor: 'rgb(75, 192, 192)',
        tension: 0.1
      }
    ]
  };

  return (
    <div>
      <h1>Stock Information</h1>
      {loading ? (
        <p>Loading...</p>
      ) : stockName ? (
        <div>
          <p>Stock Name: {stockName}</p>
          <p>Stock Price: {stockPrice}</p>
          {/* Display the chart */}
          <Line data={chartData} />
        </div>
      ) : (
        <p>No stock data available</p>
      )}
    </div>
  );
};

export default StockInfoPage;
