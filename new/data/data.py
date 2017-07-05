from pandas_datareader.data import DataReader
from sklearn.preprocessing import minmax_scale
import numpy as np
import pickle


class StockDataHelper:
    def __init__(self, stocks=['AAPL', 'MSFT','GOOG', 'AMZN', 'CSCO', 'INTC', 'VZ', 'V', 'T', 'ORCL', # technology
                               'BRK.B', 'JPM', 'GS', 'WFC', 'BAC', 'C', 'USB', 'GS', 'CB', 'MS', 'AXP', # finance
                               'JNJ', 'PFE', 'MRK', 'UNH', 'AMGN', 'BMY', 'GILD', # health care
                               'XOM', 'CVX', 'COP', 'EOG', 'OXY', 'HAL', 'KMI', 'PXD', # energy
                               'GE', 'MMM', 'BA', 'HON', 'UNP', 'UTX', 'UPS', 'CAT', 'GD', # industry
                              ], start_date='2012-01-01', end_date='2017-07-01', n_past=30, batch_size=128):
        self.stocks = stocks
        self.start_date = start_date
        self.end_date = end_date
        self.n_past = n_past
        self.batch_size = batch_size


    def encode(self, num):
        return 1 if num > 0 else 0


    def load_data(self):
        X = []
        Y = []
        for stock in self.stocks:
            x, y = [], []
            print('Downloading {} stock prices'.format(stock))
            prices = DataReader(stock, 'google', self.start_date, self.end_date)['Close'].values
            print('Processing {} stock prices'.format(stock))
            for i in range(0, len(prices)-self.n_past-1):
                x.append(minmax_scale(prices[i : i+self.n_past]))
                y.append( self.encode(prices[i+self.n_past] - prices[i+self.n_past-1]) )
            X.append(x)
            Y.append(y)
        return np.array(X).reshape([-1, 30]), np.array(Y).reshape([-1])


    def save_to_disk(self):
        X, y = self.load_data()
        print('Saving to disk: ', X.shape, y.shape)
        with open('./xy.pkl', 'wb') as o:
            pickle.dump((X, y), o, pickle.HIGHEST_PROTOCOL)


    def load_from_disk(self):
        with open('./xy.pkl', 'rb') as i:
            return pickle.load(i)
# end class