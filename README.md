# quant_stock_simulation

## This is project tends to explore machine learning algorithm for stock trading

## how to use

```
from backtesting import *

my_stock_account = StockAccount(1000000) # deposit money

hist_price = read_csv('file_path')

trade_sim = TradeSim(hist_price, my_account)

trade_sim.back_testing( start_date, end_date, target_stocks, expected_prices)

trade_sim.account.check_stock_account(stock_market_prices)
```
