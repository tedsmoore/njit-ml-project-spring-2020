from pyalgotrade import strategy


class TradeHoldStrategy(strategy.BacktestingStrategy):
    """
    A class to test strategies based on a feed of signals (1's and 0's)
    The strategy buys on next 1 and holds until next 0, when it sells and repeats.
    :param future_signals: numpy array of signals of the same length as the feed on which to trade
    """

    def __init__(self, feed, instrument, future_signals, seed_trade=False):
        strategy.BacktestingStrategy.__init__(self, feed)
        self.instrument = instrument
        self.future_signals = future_signals
        self.adj_close = feed[instrument].getAdjCloseDataSeries()
        self.day = 0
        self.seed_trade = seed_trade
        self.position = None

    def onStart(self):
        if self.seed_trade:
            self.position = self.enterLong(self.instrument, 100)

    def onBars(self, bars):
        try:
            todays_signal = self.future_signals[self.day]
            yesterdays_signal = self.future_signals[self.day - 1]
            if todays_signal > yesterdays_signal:
                self.position = self.enterLong(self.instrument, 100, True)
            elif todays_signal < yesterdays_signal:
                self.position.exitMarket()
        except IndexError:
            pass
        self.day += 1

    def onEnterOk(self, position):
        execInfo = position.getEntryOrder().getExecutionInfo()
        self.info("BUY at $%.2f" % (execInfo.getPrice()))

    def onExitOk(self, position):
        execInfo = position.getExitOrder().getExecutionInfo()
        self.info("SELL at $%.2f" % (execInfo.getPrice()))
        self.position = None
