## StockPredictor
StockPredictor is a comprehensive stock market prediction platform leveraging advanced machine learning algorithms to forecast market prices across various time ranges, enabling users to make informed investment decisions.

Architecture: 

- Frontend: ReactJS
- Backend: Next.js server
- API Integrations: Alpha Vantage, Yahoo Finance, Coin Market Cap
- Machine Learning Models: LSTM, RBF, SVM
- Libraries & Tools: Python, Keras, scikit-learn, Jupyter
  
Features: 

- LSTM Model: Predicts the opening price of the next day using indicators such as Exponential Moving Averages, Bollinger Bands, Simple Moving Averages, Stochastic Oscillator, and Average True Range.
- RBF & SVM Models: Predict the opening prices for the next day and next 5 minutes using indicators like RSI, MACD, Stochastic Oscillator, Awesome Oscillator, and Money Fund Index.
  
API Data Sources:

- Yahoo Finance API: Used for RBF & SVM models.
- Alpha Vantage API: Used for LSTM model.
  
Technological Advancements:

- LSTM models address the vanishing gradient problem in RNNs using forget logic gates for long-term information retention.
- Sentiment analysis and sector-specific training experiments highlight the challenges and ongoing research in enhancing prediction accuracy.


This is a [Next.js](https://nextjs.org/) project bootstrapped with [`create-next-app`](https://github.com/vercel/next.js/tree/canary/packages/create-next-app).

## Getting Started

First, run the development server:

```bash
npm run dev
# or
yarn dev
# or
pnpm dev
```

Open [http://localhost:3000](http://localhost:3000) with your browser to see the result.

You can start editing the page by modifying `app/page.txt`. The page auto-updates as you edit the file.

This project uses [`next/font`](https://nextjs.org/docs/basic-features/font-optimization) to automatically optimize and load Inter, a custom Google Font.
