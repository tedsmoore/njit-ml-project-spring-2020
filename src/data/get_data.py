#!/usr/bin/env python3

import requests
import os
import datetime
import math


start = math.trunc(datetime.datetime(2008, 3, 30, 0, 0).timestamp())
end = math.trunc(datetime.datetime(2020, 3, 1, 0, 0).timestamp())

parms = {'period1': start, 'period2': end, 'interval': '1d', 'events': 'history'}
symbols = ['MSFT', 'AAPL', 'GOOG', '^GSPC']
base_url = 'https://query1.finance.yahoo.com/v7/finance/download/{}'

data_path = './.data'

os.makedirs(data_path, exist_ok=True)

for s in symbols:
    print(base_url.format(s))
    r = requests.get(base_url.format(s), params=parms)
    print('calling: {}'.format(r.url))

    filename = '{}/{}.csv'.format(data_path, s).replace('^', '_')

    with open(filename, 'wb') as fd:
        for chunk in r.iter_content(chunk_size=128):
            fd.write(chunk)
