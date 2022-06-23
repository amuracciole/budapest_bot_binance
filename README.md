# Binance Moon Bot
This is a bot programed in Python and the idea is to optimize SELL and BUY orders taking into account the moon state:
- **FULL MOON**: Buy BTC :full_moon:
- **NEW MOON**: Sell BTC :new_moon:

![Moon trading](https://github.com/amuracciole/moon_bot_binance/blob/main/picture.png)

:warning: **ALERT!: This is an academic task and NOT AN INVEST ADVISE** :warning:

## Keys :key:
Plese add you own kes and paths in config.py file
- API_KEY, API_SECRET -> Obtained in Binance web
- EMAIL_FROM -> Mail that sends the notifications
- EMAIL_TO -> Mail where notifications are received
- EMAIL_PASS -> This is not your email account password, is a "key" obtained in your email settings to allow you send messages from external API
- HISTORIC_PATH and LOGS_PATH -> Complete path that you save those files

## Email :email:
Allows you to send an email with a notification once bot make an operation. This is a second way to save a history

## Crontab :stopwatch:
You must include the following line in you crontab file to run the script every day at 4:00 AM (You can schedule as you wish)

0 4 * * * *project path*

## Test orders :exclamation:
This script will never buy or sell BTC because only run "test_order". In case you want to work with real operations, please comment test_order lines and delete "#" before "order_market_sell" and "order_market_buy" lines