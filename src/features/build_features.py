
import numpy as np
import ta


class StockTechnicals:
    """
    A class for creating technical indicators of stocks as features and labels from various strategies for training
    Machine Learning models
    :param data: A pandas dataframe of a daily stock ticker data
    Usage:
    a = StockTechnicals(data)
    X = a.features
    y = a.price_will_rise()
    """

    def __init__(self, data):
        self.data = data
        self._features = ta.add_all_ta_features(
            self.data,
            open="Open",
            high="High",
            low="Low",
            close="Close",
            volume="Volume"
        )

    @property
    def features(self):
        return self._features.drop(
            columns=[
                "Date",
                "Open",
                "High",
                "Low",
                "Close",
                "Adj Close",
                "Volume",
                'trend_psar_up',
                'trend_psar_down',
                'trend_psar']
        ).dropna()

    # Can add more derived metrics here
    # e.g. slopes, cross-overs
    def add_slopes(self, metrics=(), days=()):
        if not metrics:
            metrics = list(self.features)
        for m in metrics:
            for d in days:
                self._features[f"{m}_{d}_day_slope"] = self._features.apply(self._add_slope, metric=m, days=d, axis=1)

    def _add_slope(self, row, metric, days=3):
        if row.name < days + 1:
            return None
        x = np.arange(days)
        A = np.vstack([x, np.ones(len(x))]).T
        y = self._features.loc[row.name - days:row.name - 1, metric].values
        slope, _ = np.linalg.lstsq(A, y)[0]
        return slope

    # Possible Strategy labels

    def price_will_rise(self, days=1):
        return np.array(self.features.apply(self._price_will_rise, days=days, axis=1))

    def _price_will_rise(self, row, days=1):
        try:
            if self.data.loc[row.name + days, 'Adj Close'] > self.data.loc[row.name, 'Adj Close']:
                return 1
            return 0
        except KeyError:
            return None

    def future_sma_higher_than_current_price(self, days=7):
        # This metric is the most promising as far as an investment strategy
        return np.array(self.features.apply(self._future_sma_v_price, days=days, axis=1))

    def _future_sma_v_price(self, row, days=7):
        try:
            future_sma = np.mean([self.data.loc[row.name + day + 1, 'Adj Close'] for day in range(days)])
        except KeyError:
            return None

        try:
            if future_sma > self.data.loc[row.name, 'Adj Close']:
                return 1
            return 0
        except KeyError:
            return None
