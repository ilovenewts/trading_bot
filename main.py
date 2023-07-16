import os
import time
from datetime import datetime

import ccxt
from dotenv import load_dotenv


def main():
    app: str = os.getenv('app')
    if app == 'development':
        load_dotenv()
    access = os.getenv('ACCESS_KEY')
    secret = os.getenv('SECRET_KEY')

    binance = ccxt.binance(config={
        'apiKey': access,
        'secret': secret,
        'enableRateLimit': True,
        'options': {
            'defaultType': 'future'
        }
    })

    symbol = "BTC/USDT"

    while True:
        btc = binance.fetch_ticker(symbol)
        now = datetime.now()
        print(now, btc['last'])
        time.sleep(1)


if __name__ == '__main__':
    main()
