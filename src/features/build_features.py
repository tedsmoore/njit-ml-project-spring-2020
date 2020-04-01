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

        # Signals (Features)
        self.sma = ma.SMA(feed[instrument].getAdjCloseDataSeries(), 15)
        self.sma_slope = linreg.Slope(self.sma, 7)
        self.sma_second_deriv = linreg.Slope(self.sma_slope, 3)
        self.ema = ma.EMA(feed[instrument].getAdjCloseDataSeries(), 15)
        self.ema_slope = linreg.Slope(self.ema, 7)
        self.adj_close = feed[instrument].getAdjCloseDataSeries()
        self.adj_close_slope = linreg.Slope(self.adj_close, 7)
        self.cols = ["Date",
                     "Ticker",
                     "Adj Close",
                     "Adj Close - Slope15",
                     "SMA15",
                     "Adj Close - SMA15",
                     "SMA15 - Slope15",
                     "SMA15 - Slope 15 - 2nd Deriv 3",
                     "Adj Close - EMA15"]
        self.features = pd.DataFrame(columns=self.cols)
        self.labels = None

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

    def price_will_rise(self, days=1):
        return [1 if val > 0 else 0 for val in self._future_chg_adj_close(days)]

    def sma_will_rise(self, days=15, sma_days=15):
        future_change = [None for _ in range(sma_days)]
        future_change.extend([1 if val > 0 else 0 for val in self._future_chg_sma(days)])
        return future_change

    def future_sma_higher_than_current_price(self, days=15, sma_days=15):
        # This metric is the most promising as far as an investment strategy
        return [1 if val > 0 else 0 for val in self._future_sma_v_price()]

    def _future_chg_adj_close(self, days=1):
        future_change = [self.adj_close[idx + days] - close for idx, close
                         in enumerate(self.adj_close[:len(self.adj_close) - days])]
        return future_change

    def _future_chg_sma(self, days=15, sma_days=15):
        future_change = [self.sma[idx + sma_days + days] - self.sma[idx + sma_days] for idx, _
                         in enumerate(self.sma[sma_days:len(self.sma) - days])]
        return future_change

    def _future_sma_v_price(self, days=15):
        future_change = [self.sma[idx + days] - close for idx, close
                        in enumerate(self.adj_close[:len(self.adj_close) - days])]
        return future_change

    def stock_up_by_pct(self, bars, pct, num_days):
        # work in progress
        today = bars[self.instrument].getAdj
        return None

    # Overrides (do the dataset building)

    def onStart(self):
        self.enterLong('MSFT', 100)

    def onBars(self, bars):
        bar = bars[self.instrument]
        # build up this list of signal features
        technicals = pd.DataFrame([[
            bar.getDateTime(),
            self.instrument,
            bar.getAdjClose(),
            self.adj_close_slope[-1],
            self.sma[-1],
            self.adj_close_diff_sma(bar),
            self.sma_slope[-1],
            self.sma_second_deriv[-1],
            self.adj_close_diff_ema(bar)
        ]],
            columns=self.cols)
        self.features = self.features.append(technicals, ignore_index=True)

    def onFinish(self, bars):
        self.labels = pd.DataFrame(zip(
            self.price_will_rise(),
            self.future_sma_higher_than_current_price()
        ),
            columns=[
                "1 Day Close",
                "15 Days SMA v Close"
            ])
        dataset = pd.concat([self.features, self.labels], axis=1)
        print(dataset.tail())


class CrystalBallStrategy(strategy.BacktestingStrategy):
    """
    A class to test (unrealistic) strategies based on future information fed in as future_signals
    :param future_signals: Array-like series of signals of the same length as the feed on which to trade
    """

    def __init__(self, feed, instrument, future_signals):
        strategy.BacktestingStrategy.__init__(self, feed)
        self.instrument = instrument
        self.future_signals = future_signals
        self.adj_close = feed[instrument].getAdjCloseDataSeries()

    def onStart(self):
        # self.enterLong('MSFT', 100)
        pass

    def onBars(self, bars):
        try:
            todays_signal = self.future_signals.iloc[len(self.adj_close) - 1]
            yesterdays_signal = self.future_signals.iloc[len(self.adj_close) - 2]
            if todays_signal > yesterdays_signal:
                self.enterLong(self.instrument, 100)
            elif todays_signal < yesterdays_signal:
                self.enterShort(self.instrument, 100)
        except IndexError:
            pass
