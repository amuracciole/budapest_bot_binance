#!/usr/bin/env python3

#### BACKTESTING FR 1 YEAR ####

from symtable import Symbol
from binance.client import Client
import config
import dates
from datetime import date

client = Client(config.API_KEY, config.API_SECRET)

###################
##   FUNCTIONS   ##
###################
def getKlines(pair, interval, time, place):
    #place = 0 in open time
    #place = 1 in open
    #place = 2 in high
    #place = 3 in low
    #place = 4 is close
    #place = 5 in volume
    #place = 6 is close time
    open_klines = []
    klines = client.get_historical_klines(pair, interval, time)
    for x in klines:
        open_klines.append(x[place])
    open_klines.pop()
    return (open_klines)

def get_klines_colours(open, close):
    candles = []
    for i in range(0, 30):
        if(float(open[i]) > float(close[i])):
            candles.append("RED")
        else:
            candles.append("GREEN")
    return(candles)

def read_last_value(file):
    with open(file, 'r') as f:
        for line in f:
            pass
        last_line = line
    return(last_line)

def add_line_in_file(text, file):
    if(file=="next_order"):
        file_object = open(config.NEXT_ORDER_PATH_BACKTEST, 'a')
        file_object.write(str(text) + "\n")
        file_object.close()

    elif(file=="money"):
        file_object = open(config.MONEY_PATH_BACKTEST, 'a')
        file_object.write(str(text) + "\n")
        file_object.close()

    elif(file=="ready_to_sell"):
        file_object = open(config.READY_TO_SELL_PATH_BACKTEST, 'a')
        file_object.write(str(text) + "\n")
        file_object.close()
    
    elif(file=="coins"):
        file_object = open(config.COINS_PATH_BACKTEST, 'a')
        file_object.write(str(text) + "\n")
        file_object.close()

###################
##    PROGRAM    ##
###################

next_order = read_last_value(config.NEXT_ORDER_PATH_BACKTEST).replace("\n","")
money = read_last_value(config.MONEY_PATH_BACKTEST).replace("\n","")
ready_to_sell = read_last_value(config.READY_TO_SELL_PATH_BACKTEST).replace("\n","")

print ("PARAMETERS: " + str(next_order) + ", " + str(money) + ", " + str(ready_to_sell))

all_open_candles = getKlines("BTCBUSD", Client.KLINE_INTERVAL_1DAY, "365 day ago UTC", 1)
all_close_candles = getKlines("BTCBUSD", Client.KLINE_INTERVAL_1DAY, "365 day ago UTC", 4)

#print("OPEN: " + str(all_open_candles) + "\n")
#print("CLOSE: " + str(all_close_candles) + "\n")

x=30
cicle = 1
while x<365:
    open_candles=all_open_candles[x-30:x]
    close_candles=all_close_candles[x-30:x]
    #print("OPEN: " + str(open_candles) + "\n")
    #print("CLOSE: " + str(close_candles) + "\n")
    #print("CANDLES: " + str(get_klines_colours(open_candles, close_candles)) + "\n")

    max_open = max(open_candles)
    min_close = min(close_candles)

    #print("MAX: " + max_open)
    #print("MIN: " + min_close)

    range = float(max_open) - float(min_close)
    #print("RANGE: " + str(range)+ "\n")

    green = float(min_close) + range/3
    #print ("GREEN: " + str(green))

    red = float(max_open) - range/3
    #print ("RED: " + str(red)+ "\n")

    close_last_kline = close_candles[29]
    #print ("LAST CLOSE: " + close_last_kline + "\n")

    print("***********************************\n")
    print("CICLE: " + str(cicle))


    #GREEN ZONE
    if (float(close_last_kline) < float(green)):
        order = read_last_value(config.NEXT_ORDER_PATH_BACKTEST).replace("\n","")
        coins_before = read_last_value(config.COINS_PATH_BACKTEST).replace("\n","")
        coins=float(coins_before) + float(order)/float(close_last_kline)
        money = read_last_value(config.MONEY_PATH_BACKTEST).replace("\n","")
        
        print("BEFORE I HAVE:")
        print("Coins: " + str(coins_before))
        print("Money: " + str(money))
        print("Order: " + str(order))

        print("\n....BUY " + str(float(order)/float(close_last_kline)) + " NEW COINS\n")

        add_line_in_file(coins, "coins")
        add_line_in_file(10, "next_order")
        add_line_in_file(1, "ready_to_sell")
        add_line_in_file(str(float(money) - float(order)), "money")

        print("AFTER BUY I HAVE:")
        print("Coins: " + str(coins))
        print("Money: " + str(float(money) - float(order)))
        print("Order: " + str(10))

    #RED ZONE
    elif (float(close_last_kline) > float(red)):
        ready_to_sell = read_last_value(config.READY_TO_SELL_PATH_BACKTEST).replace("\n","")
        if (ready_to_sell == "1"):
            coins = read_last_value(config.COINS_PATH_BACKTEST).replace("\n","")
            money_before = read_last_value(config.MONEY_PATH_BACKTEST).replace("\n","")
            order = read_last_value(config.NEXT_ORDER_PATH_BACKTEST).replace("\n","")

            print("BEFORE I HAVE:")
            print("Coins: " + str(coins))
            print("Money: " + str(money_before))
            print("Order: " + str(order))

            money=float(coins)*float(close_last_kline)

            print("\n....SELL " + str(coins) + " coins and I receive: " + str(money) + " money\n")

            total_money = float(money) + float(money_before)

            add_line_in_file(0, "coins")
            add_line_in_file(str(total_money), "money")
            add_line_in_file(20, "next_order")
            add_line_in_file(0, "ready_to_sell")

            print("LUEGO DE LA VENTA TENGO:")
            print("Coins: " + str(0))
            print("Money: " + str(float(total_money)))
            print("Order: " + str(20))

        else:
            print("....I SHOLUD SELL BUT I ALREDY SOLD IN THE PREVIOUS CICLE")
            next_order = read_last_value(config.NEXT_ORDER_PATH_BACKTEST).replace("\n","")
            next_order = int(next_order) + 10
            coins = read_last_value(config.COINS_PATH_BACKTEST).replace("\n","")
            money = read_last_value(config.MONEY_PATH_BACKTEST).replace("\n","")

            add_line_in_file(next_order, "next_order")

            print("I HAVE:")
            print("Coins: " + str(coins))
            print("Money: " + str(money))
            print("Order: " + str(next_order))

    #WHITE ZONE
    else:
        print("....WHITE ZONE. NO BUY OR SELL")
        next_order = read_last_value(config.NEXT_ORDER_PATH_BACKTEST).replace("\n","")
        next_order = int(next_order) + 10
        coins = read_last_value(config.COINS_PATH_BACKTEST).replace("\n","")
        money = read_last_value(config.MONEY_PATH_BACKTEST).replace("\n","")
        
        add_line_in_file(next_order, "next_order")

        print("I HAVE:")
        print("Coins: " + str(coins))
        print("Money: " + str(money))
        print("Order: " + str(next_order))
    
    x=x+7
    cicle = cicle + 1
    print("\n***********************************")
