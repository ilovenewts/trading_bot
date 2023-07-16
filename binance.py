import os
from math import floor

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
            limit=10
        )

        df = pd.DataFrame(data=btc, columns=['datetime', 'open', 'high', 'low', 'close', 'volume'])
        df['datetime'] = pd.to_datetime(df['datetime'], unit='ms')
        df.set_index('datetime', inplace=True)

        yesterday = df.iloc[-2]
        today = df.iloc[-1]
        long_target = today['open'] + (yesterday['high'] - yesterday['low']) * 0.5
        short_target = today['open'] - (yesterday['high'] - yesterday['low']) * 0.5
        return long_target, short_target

    def fetch_close(self, symbol):
        ticker = self.api.fetch_ticker(symbol)
        return ticker['last']

    def fetch_usdt_balance(self):
        balance = self.api.fetch_balance()
        return balance['total']['USDT']

    def cal_amount(self, usdt_balance, cur_price):
        portion = 0.1
        usdt_trade = usdt_balance * portion
        amount = floor((usdt_trade * 1000000) / cur_price) / 1000000
        return amount
