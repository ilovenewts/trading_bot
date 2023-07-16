import os

import ccxt
import pandas as pd


class Binance:
    api = None

    def __init__(self):
        access = os.getenv('ACCESS_KEY')
        secret = os.getenv('SECRET_KEY')

        self.api = ccxt.binance(config={
            'apiKey': access,
            'secret': secret,
            'enableRateLimit': True,
            'options': {
                'defaultType': 'future'
            }
        })

    def cal_target(self, symbol):
        btc = self.api.fetch_ohlcv(
            symbol=symbol,
            timeframe='1d',
            since=None,
            limit=10)

        df = pd.DataFrame(data=btc, columns=['datetime', 'open', 'high', 'low', 'close', 'volume'])
        df['datetime'] = pd.to_datetime(df['datetime'], unit='ms')
        df.set_index('datetime', inplace=True)

        yesterday = df.iloc[-2]
        today = df.iloc[-1]
        target = today['open'] + (yesterday['high'] - yesterday['low']) * 0.5
        return target

    def fetch_close(self, symbol):
        ticker = self.api.fetch_ticker(symbol)
        return ticker['last']
