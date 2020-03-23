# Premise

> Using ML can we predict the "adjustment" or "minor correction" points in the market activity of an Equity, ETF, or Sector based Index.

> Using Bollinger Bands, Moving Average Envelope (MAE) as the basis or control, can we introduce other attributes, features, even applying Autoencoder or PCA, LDA to refine, replace, eliminate, or combine features to improve the models for predictive capabilities.


## Method

### Data aquisition and choice
- Equity (1 or a 'few' symbols for period N)
- or, ETF representing a sector TBD
- or, an Sector Index TBD

### Feature selection
- Examine use of Autoencoders
- Examine use of GANS for Adverserial Training of competing NNs
- With exsiting or generated features, use Dimensonality Reduction via PCA or LDA for feature 
- Inversions, type of inversions, duration, magnitude, etc.


### Shampoo, Rinse, Repeat...
... 

## Reference information
### Listing of Technical Analysis indicators.

Fidelity has a nice technical analysis listing: https://www.fidelity.com/learning-center/trading-investing/technical-analysis/technical-indicator-guide/


### Feature ideas
	• Typical price vs closing price: https://www.fidelity.com/learning-center/trading-investing/technical-analysis/technical-indicator-guide/typical-price
	• ATR as indicator of volatility https://www.fidelity.com/learning-center/trading-investing/technical-analysis/technical-indicator-guide/atr
	• Chalkin volatiliyt: https://www.fidelity.com/learning-center/trading-investing/technical-analysis/technical-indicator-guide/volatility
	• Historical Volatility: https://www.fidelity.com/learning-center/trading-investing/technical-analysis/technical-indicator-guide/historical-volatility
	• Standard Deviation with different SMA periods (single moving avg) https://www.fidelity.com/learning-center/trading-investing/technical-analysis/technical-indicator-guide/standard-deviation
PE - but adjust the window -- a PE average: https://www.fidelity.com/learning-center/trading-investing/technical-analysis/technical-indicator-guide/pe-ratio