#!/usr/bin/env python3

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
        file_object = open(config.NEXT_ORDER_PATH, 'a')
        file_object.write(str(text) + "\n")
        file_object.close()

    elif(file=="money"):
        file_object = open(config.MONEY_PATH, 'a')
        file_object.write(str(text) + "\n")
        file_object.close()

    elif(file=="ready_to_sell"):
        file_object = open(config.READY_TO_SELL_PATH, 'a')
        file_object.write(str(text) + "\n")
        file_object.close()
    
    elif(file=="coins"):
        file_object = open(config.COINS_PATH, 'a')
        file_object.write(str(text) + "\n")
        file_object.close()



###################
##    PROGRAM    ##
###################

next_order = read_last_value(config.NEXT_ORDER_PATH).replace("\n","")
money = read_last_value(config.MONEY_PATH).replace("\n","")
ready_to_sell = read_last_value(config.READY_TO_SELL_PATH).replace("\n","")
coins = read_last_value(config.COINS_PATH).replace("\n","")

print ("PARAMETERS: " + str(next_order) + ", " + str(money) + ", " + str(ready_to_sell))

#Current date
today = str(date.today())
#print("\n**********************\n")
print("DATE: " + today + "\n")
for x in dates.saturday:
    if(today==x):
        open_candles = getKlines("BTCBUSD", Client.KLINE_INTERVAL_1DAY, "31 day ago UTC", 1)
        close_candles = getKlines("BTCBUSD", Client.KLINE_INTERVAL_1DAY, "31 day ago UTC", 4)
        print("OPEN: " + str(open_candles) + "\n")
        print("CLOSE: " + str(close_candles) + "\n")
        print("CANDLES: " + str(get_klines_colours(open_candles, close_candles)) + "\n")

        max_open = max(open_candles)
        min_close = min(close_candles)

        print("MAX: " + max_open)
        print("MIN: " + min_close)

        range = float(max_open) - float(min_close)
        print("RANGE: " + str(range)+ "\n")

        green = float(min_close) + range/3
        print ("GREEN: " + str(green))

        red = float(max_open) - range/3
        print ("RED: " + str(red)+ "\n")

        close_last_kline = close_candles[29]
        print ("LAST CLOSE: " + close_last_kline + "\n")

        #GREEN ZONE
        if (float(close_last_kline) < float(green)):
            order = next_order
            coins=coins + float(order)/float(close_last_kline)
            print("\n....BUY " + str(float(order)/float(close_last_kline)) + " NEW COINS\n")
            qnt_buy = str(float(coins)/float(close_last_kline))[0:7]
            buy_order = client.create_test_order(symbol="BTCBUSD", side="BUY", type="MARKET", quantity=qnt_buy)        
            #buy_order = client.create_order(symbol="BTCBUSD", side="BUY", type="MARKET", quantity=qnt_buy)
            add_line_in_file(coins, "coins")
            add_line_in_file(10, "next_order")
            add_line_in_file(1, "ready_to_sell")
            add_line_in_file(str(float(money) - float(order)), "money")

        #RED ZONE
        elif (float(close_last_kline) > float(red)):
            if (ready_to_sell == "1"):
                money_new=float(coins)*float(close_last_kline)
                print("\n....SELL " + str(coins) + " coins and I receive: " + str(money_new) + " money\n")
                sell_order = client.create_test_order(symbol="BTCBUSD", side="SELL", type="MARKET", quantity=coins)
                #sell_order = client.create_order(symbol="BTCBUSD", side="SELL", type="MARKET", quantity=coins)
                total_money = money + money_new
                add_line_in_file(0, "coins")
                add_line_in_file(str(total_money), "money")
                add_line_in_file(20, "next_order")
                add_line_in_file(0, "ready_to_sell")
            else:
                print("....I SHOLUD SELL BUT I ALREDY SOLD IN THE PREVIOUS CICLE")
                next_order = int(next_order) + 10
                add_line_in_file(next_order, "next_order")

        #WHITE ZONE
        else:
            print("....WHITE ZONE. NO BUY OR SELL")
            next_order = int(next_order) + 10
            add_line_in_file(next_order, "next_order")