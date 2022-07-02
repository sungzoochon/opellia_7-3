from os import curdir
from symtable import Symbol
import ccxt 
import time
import datetime
from numpy import short
import pandas as pd
import modd
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
def cal_target(self,coin,origin):
   try: 
    btc = binance.fetch_ohlcv(
        symbol=coin,
        timeframe='1d', 
        since=None, 
        limit=10)
    df = pd.DataFrame(data=btc, columns=['datetime', 'open', 'high', 'low', 'close', 'volume'])
    df['datetime'] = pd.to_datetime(df['datetime'], unit='ms')
    df.set_index('datetime', inplace=True)
    yesterday = df.iloc[-2]
    today = df.iloc[-1]
    long_target = today['open'] + (yesterday['high'] - yesterday['low']) * 0.5
    if origin == 'long':
     return long_target
    if origin == 'short':
     return yesterday['volume'] 
    if origin == False:
     return today['open']
   except Exception as e:
     print(e,"3")
def cal_amount(usdt_balance, cur_price):
   try: 
    amount = ((usdt_balance * 1000000)/cur_price) / 1000000
    return amount 
   except Exception as e:
     None
amount_list = []
type = []
cur_price_list = []
average = 0
def enter_position(exchange, coin, cur_price,long_target, coin_amount, position,bought_coin):
   if position['type'] == 'long': 
    if (long_target * 1.01 >=cur_price >= long_target): 
        coin2 = coin.replace("/","")
        binance.fapiPrivate_post_leverage({  
            'symbol': coin2,  
            'leverage': position['leverege'],  
        })
        exchange.create_market_buy_order(
            symbol= coin, 
            amount= coin_amount * position['leverege'],             
            params={'type': 'future'})
        cur_price_list.append(cur_price)
        amount_list.append(coin_amount * position['leverege'])
        bought_coin.append(coin)
        type.append(position['type'])  
        if len(bought_coin) != 10:
         print('[',len(bought_coin),']'," ",'\033[32m',"지구 롱",coin,'\033[0m',a * "_",round(usdt2,3))
        else:
         print('[',len(bought_coin),']','\033[32m',"지구 롱",coin,'\033[0m',a * "_",round(usdt2,3),c * " ",now.hour)
   if position['type'] == 'short': 
    if long_target * 1.01 >= cur_price >= long_target: 
        coin2 = coin.replace("/","")
        binance.fapiPrivate_post_leverage({  
            'symbol': coin2,  
            'leverage': position['leverege'],  
        })
        exchange.create_market_sell_order(
            symbol= coin, 
            amount= coin_amount * position['leverege'],             
            params={'type': 'future'})
        cur_price_list.append(cur_price)
        bought_coin.append(coin)  
        type.append(position['type'])  
        amount_list.append(coin_amount * position['leverege'])
        if len(bought_coin) != 10:
         print('[',len(bought_coin),']'," ",'\033[32m',"지구 숏",coin,'\033[0m',a * "_",round(usdt2,3),c * " ",now.hour)
        else:
         print('[',len(bought_coin),']','\033[32m',"지구 숏",coin,'\033[0m',a * "_",round(usdt2,3))
def exit_position(exchange,i):
   try: 
    coin = bought_coin[i]
    if type[i] == 'short':
        exchange.create_market_buy_order(symbol=coin, amount=amount_list[i])
    if type[i] == 'long': 
        exchange.create_market_sell_order(symbol=coin, amount=amount_list[i])
    del(amount_list[i])
    del(bought_coin[i])
    del(cur_price_list[i])
    del(type[i])
   except Exception as e:
      up_average = 10
coin = ""
start = False
markets = binance.load_markets() 
long_target = [0 for i in markets.keys()]
short_target = [0 for i in markets.keys()]
position = {"leverege":50,"type":""} 
bought_coin = []
m =0
k = 0
once = 0
op_mode = True
up_average = 10
while True: 
  try:
    now = datetime.datetime.now()                     
    if now.minute == 0 or once == 1:
     markets = binance.load_markets()  
     n = 0
     origin = False
     for i in markets.keys():
      if 'USDT' in i: 
          n = n + 1  
     Market= ["" for i in range(n)]
     n = 0
     for i in markets.keys():
       if 'USDT' in i: 
        Market[n] = i
        n = n + 1
    if m < len(Market):                                               
        coin = Market[m]
        if (now.hour == 9 and now.minute == 00 and op_mode == True) or once == 1:
            if op_mode:
                print("수익:",usdt2-usdt, "총 금액:",usdt2)
                for a in range(len(bought_coin)):
                 if amount_list[a] != 0: 
                  exit_position(binance,a,)
                n = 0
                markets = binance.load_markets()
                for i in markets.keys():
                    if 'USDT' in i: 
                        n = n + 1  
                Market= ["" for i in range(n)]
                n = 0
                for i in markets.keys():
                    if 'USDT' in i: 
                        Market[n] = i
                        n = n + 1
                op_mode = False
                bought_coin = []
                cur_price_list = []
                type = []
                amount_list = []
                start = False
                long_target = [0 for i in markets.keys()]
        if start == False and (now.hour == 9 or once == 1):               
            start = True
            once = 0
            balance = binance.fetch_balance()        
            usdt = balance['total']['USDT']
            coin_list_up,coin_list_down = modd.record()
            print("가즈아")
        if start:
         if long_target[m]  == 0:
          long = 'long'
          long_target[m] = cal_target(binance,coin,long)
         op_mode = True
         ticker = binance.fetch_ticker(coin)
         cur_price = ticker['last']              
         if op_mode and len(bought_coin) < round(up_average) and coin not in bought_coin: 
            amount = cal_amount(usdt/round(up_average), cur_price)
            a = 16 - len(coin)
            b = 15 - len(str(usdt))
            c = 11 - len(str(cur_price))
            try:
             if coin_list_up[Market.index(coin)] > coin_list_down[Market.index(coin)]:
                position['type'] = 'long'
             else:
                position['type'] = 'short'
            except Exception as e:
             position['type'] = 'short'
            enter_position(binance, coin, cur_price,long_target[m],amount, position,bought_coin)
         if op_mode and len(bought_coin) >= 1:
          for i in range(len(bought_coin)):
           if amount_list[i] != 0:   
            ticker = binance.fetch_ticker(bought_coin[i])
            cur_price = ticker['last']
            if type[i] == 'long':
                if cur_price <= (cur_price_list[i] * 0.96):
                   exit_position(binance, i)
                   print("돔황차")
                   print(usdt)
                if cur_price >= (cur_price_list[i] * 1.06):
                   exit_position(binance, i) 
                   print("익절")
                   print(usdt)
            if type[i] == 'short':
                if cur_price >= (cur_price_list[i] * 1.04):
                   exit_position(binance ,i)
                   print("돔황차")
                   print(usdt)
                if cur_price <= (cur_price_list[i] * 0.94):
                   exit_position(binance, i) 
                   print("익절")
                   print(usdt)
            time.sleep(0.1)   
         balance = binance.fetch_balance()        
         usdt2 = balance['total']['USDT']   
         if (usdt2 >= (usdt * 1.5)) or (usdt2 <= (usdt * 0.7)):
            start = False
            if op_mode:
                for a in range(len(bought_coin)): 
                    exit_position(binance,a)
                    print("끝")
                    bought_coin = []
                    cur_price_list = []
                    type = []
                    amount_list = []
                    start = False   
        time.sleep(0.1)
        m = m + 1
    else:
        m = 0
  except Exception as e:
      m = m + 1 
