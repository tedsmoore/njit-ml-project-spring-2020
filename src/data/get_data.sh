#!/usr/bin/env bash

# URL encoded ^GSPC -- %5EGSPC"
PARMS="?period1=1206835200&period2=1585612800&interval=1d&events=history"

# declare an array called array and define 3 vales
TICKERS=( "%5EGSPC" "MSFT" "AAPL" "GOOG" "AMZN")
for I in "${TICKERS[@]}"
do
	curl -v "https://query1.finance.yahoo.com/v7/finance/download/${I}${PARMS}" -o "./.data/${I}.csv"
done

