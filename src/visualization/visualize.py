import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
sns.set(style="darkgrid")


class DisplayTicker():

    def __init__(self, ticker, name):

        self._ticker = ticker
        self._name = name    


    def graph_stock(self):
        """
        Graphs the Stock stock
        :param symbol: Stock Ticket Symbol
        :return: None
        """
        fig = plt.figure(figsize=(20,10))
        plt.xticks(rotation=45)
        plt.title(self._name, fontsize = 20)
        
        plt.xlabel("Date")
        plt.ylabel("Price")
        stock_open_price = pd.Series(self._ticker['Open'].to_numpy(), index=pd.date_range(self._ticker['Date'].iloc[0], periods=503, freq='D'))
        stock_close_price = pd.Series(self._ticker['Close'].to_numpy(), index=pd.date_range(self._ticker['Date'].iloc[0], periods=503, freq='D'))
        stock_open_price_ma = stock_open_price.rolling(15).mean()
        stock_open_price_mstd = stock_open_price.rolling(15).std()

        plt.plot(stock_open_price.index, stock_open_price, 'g', label = "Open Price")
        plt.plot(stock_open_price.index, stock_close_price, '--y', label = "Close Price")
        plt.plot(stock_open_price_ma.index, stock_open_price_ma , 'b', label = "15 Day MOV")
        plt.legend(loc="upper left")
        plt.fill_between(stock_open_price_mstd.index,
                        stock_open_price_ma - 2 * stock_open_price_mstd,
                        stock_open_price_ma + 2 * stock_open_price_mstd,
                        color='b',
                        alpha=0.2)
        plt.show()

    