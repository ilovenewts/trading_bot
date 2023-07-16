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
    long_target, short_target = binance.cal_target(symbol)
    usdt = binance.fetch_usdt_balance()
    op_mode = False
    position = {
        "type": None,
        "amount": 0
    }

    while True:
        now = datetime.now()

        if now.hour == 8 and now.minute == 50 and (0 <= now.second < 10):
            if op_mode and position['type'] is not None:
                exit_position(binance, symbol, position)
                op_mode = False  # stop enter until 9

        # update target price
        if now.hour == 9 and now.minute == 0 and (20 <= now.second < 30):
            long_target, short_target = binance.cal_target(symbol)
            usdt = binance.fetch_usdt_balance()
            op_mode = True
            time.sleep(10)

        close = binance.fetch_close(symbol)
        amount = binance.cal_amount(usdt, close)

        if op_mode and position['type'] is None:
            enter_position(binance, symbol, close, long_target, short_target, amount, position)

        print(now, close)
        time.sleep(1)


def enter_position(exchange, symbol, cur_price, long_target, short_target, amount, position):
    if cur_price > long_target:  # 현재가 > long 목표가
        position['type'] = 'long'
        position['amount'] = amount
        exchange.create_market_buy_order(symbol=symbol, amount=amount)
    elif cur_price < short_target:  # 현재가 < short 목표가
        position['type'] = 'short'
        position['amount'] = amount
        exchange.create_market_sell_order(symbol=symbol, amount=amount)


def exit_position(exchange, symbol, position):
    amount = position['amount']
    if position['type'] == 'long':
        exchange.create_market_sell_order(symbol=symbol, amount=amount)
        position['type'] = None
    elif position['type'] == 'short':
        exchange.create_market_buy_order(symbol=symbol, amount=amount)
        position['type'] = None


if __name__ == '__main__':
    main()
