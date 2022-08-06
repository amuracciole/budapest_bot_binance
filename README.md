# Binance Budapest Bot
This bot connects to Binance and buys or sells taking into account the Budapest strategy, which consists of buying if the current price is in the green quadrant and selling if it is in the red quadrant.
The flag is formed taking into account the high and low prices of the last 30 days.  
- **RED ZONE**: Sell BTC. The current price is between the maximum (in the last 30 days) and 33% cheaper than the maximum. :red_circle:
- **WHITE ZONE**: No buy no sell :white_circle:
- **GREEN ZONE**: Buy BTC. The current price is between the minimum (in the last 30 days) and 33% more expensive than the minimum. :green_circle:

![Moon trading](https://github.com/amuracciole/budapest_bot_binance/blob/main/picture.png)

:warning: **ALERT!: This is an academic task and NOT AN INVEST ADVISE** :warning:

## Keys :key:
Plese add you own keys and paths in [config.py](https://github.com/amuracciole/budapest_bot_binance/blob/main/config.py) file
- API_KEY & API_SECRET -> Obtained in Binance web
- Full directory where the text files that store global variables will be located. There are 8 text files in total, 4 are for the production environment and the other 4 are for backtesting.

By default the variables should be initialized:
- "coins" -> Amount of BTC to start with.
- "money" -> Amount of stable coin BUSD to start with
- "next order" -> Variable defining the amount of BUSD to be used to buy BTC next time
- "ready to sell" -> Variable indicating whether it is possible to sell

As an example we start with 0, 1000, 10, 0 respectively.

## Backtesting :triangular_flag_on_post:
The [budapest_strategy_backtest.py](https://github.com/amuracciole/budapest_bot_binance/blob/main/budapest_strategy_backtest.py) file is used to backtest the script and see its profitability. By default it does backtesting from the daily candles of the last 365 days.

## Crontab :stopwatch:
You MUST include the following line in you crontab file to run the script every day at 4:00 AM (You can schedule as you wish)

0 4 * * * *project path*

## Test orders :exclamation:
This script will never buy or sell BTC because only run "test_order". In case you want to work with real operations, please comment test_order lines and delete "#" before "order_market_sell" and "order_market_buy" lines

[!["Buy Me A Coffee"](https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png)](https://www.buymeacoffee.com/amuracciole)