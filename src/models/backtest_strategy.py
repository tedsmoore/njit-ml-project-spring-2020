from pyalgotrade import strategy


class TradeHoldStrategy(strategy.BacktestingStrategy):
    """
    A class to test strategies based on a feed of signals (1's and 0's)
    The strategy buys on next 1 and holds until next 0, when it sells and repeats.
    :param future_signals: numpy array of signals of the same length as the feed on which to trade
    """

    def __init__(self, feed, instrument, future_signals, verbose=False):
        strategy.BacktestingStrategy.__init__(self, feed)
        self.instrument = instrument
        self.future_signals = future_signals
        self.adj_close = feed[instrument].getAdjCloseDataSeries()
        self.day = 0
        self.position = None
        self.verbose = verbose

    def onBars(self, bars):
        try:
            todays_signal = self.future_signals[self.day]
            if self.day == 0:
                yesterdays_signal = 0
            else:
                yesterdays_signal = self.future_signals[self.day - 1]

            if todays_signal > yesterdays_signal:
                self.position = self.enterLong(self.instrument, 100)
            elif todays_signal < yesterdays_signal:
                self.position.exitMarket()
        except IndexError:
            pass
        self.day += 1

    def onEnterOk(self, position):
        if self.verbose:
            exec_info = position.getEntryOrder().getExecutionInfo()
            self.info("BUY at $%.2f" % (exec_info.getPrice()))

    def onExitOk(self, position):
        if self.verbose:
            exec_info = position.getExitOrder().getExecutionInfo()
            self.info("SELL at $%.2f" % (exec_info.getPrice()))
        self.position = None


