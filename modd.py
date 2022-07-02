from ast import Or
from datetime import datetime
from openpyxl import load_workbook
import datetime
from symtable import Symbol
import ccxt 
import time
import datetime
from numpy import short
import pandas as pd
api_key = '6zHOZK1HIAidFdxoGxHR5GB85VOqCZ7VbbKXdBz8Ne6XfFUG4feKcPfVw15o0Ew1'
secret = 'PevYip6CONYhgYKdNTVnGjIYGS03hptq09jqUgsCUlLFlJJXJ7KcTXUyGmJmEVcl'
binance = ccxt.binance(config={
    'apiKey': api_key, 
    'secret': secret,
    'enableRateLimit': False,
    'options': {
        'defaultType': 'future'
    }
})
n = 0
coin_list_up = []
coin_list_down = []
markets = binance.load_markets()
for i in markets.keys():
    if 'USDT' in i: 
          n = n + 1  
    
Market= ["" for i in range(n)]
coin_list_up = [0 for i in range(n)]
coin_list_down = [0 for i in range(n)]
n = 0
for i in markets.keys():
       if 'USDT' in i: 
        Market[n] = i
        n = n + 1
def record():
 a = -1
 date = 0
 up_list = []
 num = 0
 while True:
  a = a - 1
  date = date + 1
  try:
   for i in Market:
    btc = binance.fetch_ohlcv(
         symbol=i,
         timeframe='1d', 
         since=None, 
         limit=10)
    df = pd.DataFrame(data=btc, columns=['datetime', 'open', 'high', 'low', 'close', 'volume'])
    df['datetime'] = pd.to_datetime(df['datetime'], unit='ms')
    df.set_index('datetime', inplace=True)
    yesterday = df.iloc[a - 1]
    today = df.iloc[a] 
    long_target = today['open'] + (yesterday['high'] - yesterday['low']) * 0.5
    if today['high'] >= long_target: #and long_target > today['open'] * 1.04:
     up_list.append(i)
   for i in up_list:
    btc = binance.fetch_ohlcv(
         symbol=i,
         timeframe='1d', 
         since=None, 
         limit=10)
    df = pd.DataFrame(data=btc, columns=['datetime', 'open', 'high', 'low', 'close', 'volume'])
    df['datetime'] = pd.to_datetime(df['datetime'], unit='ms')
    df.set_index('datetime', inplace=True)
    yesterday = df.iloc[a - 1]
    today = df.iloc[a] 
    long_target = today['open'] + (yesterday['high'] - yesterday['low']) * 0.5
    if today['close'] > long_target:
        coin_list_up[Market.index(i)] = coin_list_up[Market.index(i)] + 1
    else:
        coin_list_down[Market.index(i)] = coin_list_down[Market.index(i)] + 1
   num = num + 1
   time.sleep(0.5)
   up_list = []
  except Exception as e:
     
     return coin_list_up,coin_list_down    

