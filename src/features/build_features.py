import pandas as pd
from pyalgotrade import strategy
from pyalgotrade.technical import ma, linreg


class BuildFeatures(strategy.BacktestingStrategy):
    """
    Construct features (and labels for training) of stock market indicators from daily CSV files
    using various stock analysis techniques

    Example usage:
    b = BuildFeatures()
    X, y = b.run()
    """

    def __init__(self, feed, instrument):
        strategy.BacktestingStrategy.__init__(self, feed)
        self.instrument = instrument
        self.sma = ma.SMA(feed[instrument].getAdjCloseDataSeries(), 15)
        self.ema = ma.EMA(feed[instrument].getAdjCloseDataSeries(), 15)
        self.adj_close = feed[instrument].getAdjCloseDataSeries()
        self.adj_close_slope = linreg.Slope(feed[instrument].getAdjCloseDataSeries(), 15)
        self.cols = ["Date", "Ticker", "Adj Close", "SMA15", "Adj Close - SMA15", "Adj Close - EMA15"]
        self.features = pd.DataFrame(columns=self.cols)

    # Signals (Features)

    def adj_close_diff_sma(self, bar):
        try:
            return bar.getAdjClose() - self.sma[-1]
        except TypeError:
            return None

    def adj_close_diff_ema(self, bar):
        try:
            return bar.getAdjClose() - self.ema[-1]
        except TypeError:
            return None

    # Buy/Sell Conditions (Labels)

    def stock_will_rise(self, days=1):
        return [1 if val > 0 else 0 for val in self._future_chg_adj_close(days)]

    def sma_will_rise(self, days=15, sma_days=15):
        future_change = [None for _ in range(sma_days)]
        future_change.extend([1 if val > 0 else 0 for val in self._future_chg_sma(days)])
        return future_change

    def _future_chg_adj_close(self, days=1):
        future_change = [self.adj_close[idx + days] - close for idx, close
                         in enumerate(self.adj_close[:len(self.adj_close) - days])]
        return future_change

    def _future_chg_sma(self, days=15, sma_days=15):
        future_change = [self.sma[idx + sma_days + days] - self.sma[idx + sma_days] for idx, _
                         in enumerate(self.sma[sma_days:len(self.sma) - days])]
        return future_change

    def stock_up_by_pct(self, bars, pct, num_days):
        # work in progress
        today = bars[self.instrument].getAdj
        return None

    # Overrides (do the dataset building)

    def onBars(self, bars):
        bar = bars[self.instrument]
        # build up this list of signal features
        technicals = pd.DataFrame([[
            bar.getDateTime(),
            self.instrument,
            bar.getAdjClose(),
            self.sma[-1],
            self.adj_close_diff_sma(bar),
            self.adj_close_diff_ema(bar)
        ]],
            columns=self.cols)
        self.features = self.features.append(technicals, ignore_index=True)

    def onFinish(self, bars):
        labels = pd.DataFrame(self.sma_will_rise(), columns=["Label"])
        dataset = pd.concat([self.features, labels], axis=1)
        print(dataset.tail())
        return self.features, labels
