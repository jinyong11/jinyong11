import time
import pyupbit
import datetime


access = ""
secret = ""

def buy_price(ticker):
    """변동성 돌파 전략으로 매수 목표가 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=2)
    buy_price = df.iloc[1]['open']
    return buy_price

print(buy_price("KRW-BTC"))


def get_start_time(ticker):
    """시작 시간 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=1)
    start_time = df.index[0]
    return start_time
    
print(get_start_time("KRW-BTC"))
    
def get_ma5(ticker):
    """5일 이동 평균선 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=6)
    ma5 = df['close'].rolling(5).mean().shift(1).iloc[-1]
    return ma5

print(get_ma5("KRW-ETH"))

def get_ma10(ticker):
    """10일 이동 평균선 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=11)
    ma10 = df['close'].rolling(10).mean().shift(1).iloc[-1]
    return ma10
    
print(get_ma10("KRW-ETH"))


def get_balance(ticker):
    """잔고 조회"""
    balances = upbit.get_balances()
    for b in balances:
        if b['currency'] == ticker:
            if b['balance'] is not None:
                return float(b['balance'])
            else:
                return 0
    return 0



def get_current_price(ticker):
    """현재가 조회"""
    return pyupbit.get_orderbook(tickers=ticker)[0]["orderbook_units"][0]["ask_price"]


# 로그인
upbit = pyupbit.Upbit(access, secret)
print("autotrade start")


# 자동매매 시작

while True:
    now = datetime.datetime.now()
    start_time = get_start_time("KRW-BTC") + datetime.timedelta(seconds=30)
    end_time = start_time + datetime.timedelta(seconds=90)
    tickers = ("KRW-ETH", "KRW-ADA", "KRW-BTC", "KRW-XRP", "KRW-DOT", "KRW-LINK", "KRW-CRO", "KRW-HBAR", "KRW-BTT", "KRW-THETA", "KRW-ONT", "KRW-ANKR")
    try:
        for ticker in tickers:
            buyprice = buy_price(ticker)
            ma5 = get_ma5(ticker)
            ma10 = get_ma10(ticker)
            ticker_balance = upbit.get_balance(ticker)
            current_price = get_current_price(ticker)
            krw = upbit.get_balance("KRW")
            print("check start:", ticker, ticker_balance, "/" ,"KRW:", krw)
            print(buyprice, ma5, ma10)
            if start_time < now < end_time:        
                print("check ma5, ma10:", ticker,ticker_balance, "/", "KRW:", krw)
                if buyprice > ma5 and ma5 >= ma10:
                    if krw > 500000 and upbit.get_balance(ticker) < 0.001:
                        upbit.buy_market_order(ticker, krw*0.2)
                        print("Buy complete:", ticker, krw*0.2)
                    else : 
                        print("already have one or not enought money")
                elif buyprice > ma5 and ma5 < ma10:
                    print("ma5 is lower than ma10")
                else:
                    if ticker_balance > 0.001:
                        upbit.sell_market_order(ticker, ticker_balance)
                        print("Sell complete:", ticker, ticker_balance)   
                print("checked ma5, ma10:", ticker, ticker_balance)
                time.sleep(0.2)

            elif end_time < now and ticker_balance > 0.001:
                    print(now, "monitoring overshoot & drop:", ticker, ticker_balance, "/" , ticker_balance*current_price)
                    if current_price > buyprice*1.25:
                        if ticker_balance*current_price > 450000:
                            upbit.sell_market_order(ticker, ticker_balance*0.5)
                            print("Sell complete by overshoot:", ticker, ticker_balance*0.5) 
                    elif current_price < buyprice*0.9:
                        if ticker_balance*current_price > 450000:
                            upbit.sell_market_order(ticker, ticker_balance*0.5)
                            print("Sell complete by drop:", ticker, ticker_balance*0.5)
                    print("checked overshoot&drop:", ticker, ticker_balance)
                    time.sleep(0.2)
            else:
                print(now, buyprice, current_price, "this is not trade time")
                time.sleep(0.2)
    except Exception as e:
        print(e)
        time.sleep(1)
