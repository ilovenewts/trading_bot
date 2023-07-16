import os
import time
from datetime import datetime

from dotenv import load_dotenv

from binance import Binance


def main():
    app: str = os.getenv('app')
    if app == 'development':
        load_dotenv()

    symbol = "BTC/USDT"
    binance = Binance()
    target = binance.cal_target(symbol)

    while True:
        now = datetime.now()

        if now.hour == 9 and now.minute == 0 and (20 <= now.second < 30):
            target = binance.cal_target(symbol)

        close = binance.fetch_close(symbol)
        print(symbol, now, close, target)
        time.sleep(1)


if __name__ == '__main__':
    main()
