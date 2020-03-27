import pandas as pd
from pyalgotrade import strategy
from pyalgotrade.technical import ma, linreg
from pyalgotrade.dataseries import SequenceDataSeries


class BuildFeatures(strategy.BacktestingStrategy):
    def __init__(self, feed, instrument):
        strategy.BacktestingStrategy.__init__(self, feed)
        self.__instrument = instrument
        self.__sma = ma.SMA(feed[instrument].getAdjCloseDataSeries(), 15)
        self.__ema = ma.EMA(feed[instrument].getAdjCloseDataSeries(), 15)
        self.adj_close = feed[instrument].getAdjCloseDataSeries()
        self.adj_close_slope = linreg.Slope(feed[instrument].getAdjCloseDataSeries(), 15)
        self.cols = ["Date", "Ticker", "Adj Close", "Adj Close - SMA15", "Adj Close - EMA15"]
        self.features = pd.DataFrame(columns=self.cols)

    ### Buy/Sell Conditions (Labels)

    def stock_will_rise(self, days=1):
        return [1 if val > 0 else 0 for val in self._future_chg_adj_close(days)]

    def _future_chg_adj_close(self, days=1):
        future_change = [self.adj_close[idx + days] - close for idx, close
                         in enumerate(self.adj_close[:len(self.adj_close) - days])]
        return future_change

    def stock_up_by_pct(self, bars, pct, num_days):
        today = bars[self.__instrument].getAdj

    ### Signals (Features)

    def adj_close_diff_sma(self, bar):
        try:
            return bar.getAdjClose() - self.__sma[-1]
        except TypeError:
            return None

    def adj_close_diff_ema(self, bar):
        try:
            return bar.getAdjClose() - self.__ema[-1]
        except TypeError:
            return None

    ### Overrides (do the dataset building)

    def onBars(self, bars):
        bar = bars[self.__instrument]
        # build up this list of signal features
        technicals = pd.DataFrame([[
            bar.getDateTime(),
            self.__instrument,
            bar.getAdjClose(),
            self.adj_close_diff_sma(bar),
            self.adj_close_diff_ema(bar)
        ]],
            columns=self.cols)
        self.features = self.features.append(technicals, ignore_index=True)

    def onFinish(self, bars):
        self.labels = pd.DataFrame(self.stock_will_rise(), columns=["Label"])
        # to use this as a features set
        # return self.featuers, self.labels
        dataset = pd.concat([self.features, self.labels], axis=1)
        print(dataset.tail())
