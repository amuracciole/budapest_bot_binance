#!/usr/bin/env python3

from symtable import Symbol
from binance.client import Client
import config
import dates
from datetime import date
import smtplib
from email.mime.text import MIMEText

client = Client(config.API_KEY, config.API_SECRET)

def get_balance():
    btc_balance = client.get_asset_balance(asset='BTC')
    busd_balance = client.get_asset_balance(asset='BUSD')
    #Convert balances to float
    btc_float = float(btc_balance["free"])
    busd_float = float(busd_balance["free"])
    return btc_float, busd_float

def get_price(side, date, quantity):
    current_prices = client.get_all_tickers()
    for coin in current_prices:
        if(coin["symbol"] == "BTCBUSD"):
            add_line_in_file(str(date) + "      " + str(side) + "       " + str(quantity) + "       " + str(coin["price"]))

def add_line_in_file(text):
    file_object = open(config.HISTORIC_PATH, 'a')
    file_object.write(str(text) + "\n")
    file_object.close()
    print("\n  DATE        OPERATION       BTC              PRICE        ")
    print(str(text))

def add_log(text):
    file_object = open(config.LOGS_PATH, 'a')
    file_object.write(str(text) + "\n")
    file_object.close()

def send_email(side, date, quantity):
    correo_origen = config.EMAIL_FROM
    clave = config.EMAIL_PASS
    correo_destino =config.EMAIL_TO

    if (side == "SELL"):
      msg = MIMEText("(" + str(date) + ") -  BOT " + str(side) + " " +  str(quantity) +  " BTC")
    elif (side == "BUY"):
      msg = MIMEText("(" + str(date) + ") -  BOT " + str(side) + " " +  str(quantity) + " BTC")
    msg['Subject'] = str(date) + ' --> BTC BOT Operation'
    msg['From'] = correo_origen
    msg['To'] = correo_destino

    server = smtplib.SMTP('smtp.gmail.com',587)
    server.starttls()
    server.login(correo_origen,clave)
    server.sendmail(correo_origen,correo_destino,msg.as_string())

    server.quit()

#CURRENT DATE
today = str(date.today())
print("\n**********************\n")
print("DATE:", today)
add_log(today)

#Get balance (before)
print("\nBALANCE (BEFORE):")
balances = get_balance()
print("BTC: " + str(balances[0]))
print("BUSD: " + str(balances[1]))
for x in dates.new_moon:
    if(today==x):
        #print("\nTODAY IS NEW MOON -- SELL!")
        before_quantity = str(round(balances[0],8))
        sell_order = client.create_test_order(symbol="BTCBUSD", side="SELL", type="MARKET", quantity=str(round(balances[0],5)))
        #sell_order = client.order_market_sell(symbol="BTCBUSD", quantity=str(round(balances[0],5)))
        if(sell_order == {}): 
            get_price("Sell", today, before_quantity)
            send_email("SELL", today, before_quantity)
        else:
            print("ALERT!! For some reason the sale could not be made")

for x in dates.full_moon:
    if(today==x):
        #print("\nTODAY IS FULL MOON -- BUY!")
        buy_order = client.create_test_order(symbol="BTCBUSD", side="BUY", type="MARKET", quantity=str(round(balances[1],5)))
        #buy_order = client.order_market_buy(symbol="BTCBUSD", quantity=str(round(get_balance[1],5)))
        if(buy_order == {}): 
            get_price("Buy", today, get_balance()[0])
            buy_btc = get_balance()
            buy_btc = str(buy_btc[0])
            send_email("BUY", today, buy_btc)
        else:
            print("ALERT!! For some reason the purchase could not be made")

#Get balances (after)
print("\nBALANCE (AFTER):")
balances_after = get_balance()
print("BTC: " + str(balances_after[0]))
print("BUSD: " + str(balances_after[1]))
print("\n**********************\n")