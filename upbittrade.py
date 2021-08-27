import time
import pyupbit
import datetime


access = "Y"
secret = "x"

def buy_price(ticker):
    """변동성 돌파 전략으로 매수 목표가 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=2)
    buy_price = df.iloc[1]['open']
    return buy_price


'''
def sell_price(ticker):
    """변동성 돌파 전략으로 매수 목표가 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=2)
    sell_price = df.iloc[0]['close']
    return sell_price
'''


def get_start_time(ticker):
    """시작 시간 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=1)
    start_time = df.index[0]
    return start_time
    
def get_ma5(ticker):
    """15일 이동 평균선 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=6)
    ma5 = df['close'].rolling(5).mean().shift(1).iloc[-1]
    return ma5


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

'''
ma5 = get_ma5("KRW-BTC")
buyprice = buy_price("KRW-BTC")
krw = get_balance("KRW")
tickers = ("KRW-BTC", "KRW-ETH", "KRW-XRP", "KRW-HBAR", "KRW-DOT", "KRW-MBL", "KRW-LTC", "KRW-LINK",)


for ticker in tickers:
    print(get_ma5(ticker), buy_price(ticker), upbit.get_balance(ticker), upbit.get_balance("KRW"))


print(get_ma5("KRW-ETH"), buy_price("KRW-ETH"), upbit.get_balance("LINK"))
print(krw)
'''

# 자동매매 시작
i = 0
now = datetime.datetime.now()
start_time = get_start_time("KRW-BTC") + datetime.timedelta()
end_time = start_time + datetime.timedelta(seconds=60)

print(upbit.get_balance("KRW"))

while start_time < now < end_time and i <3:
    i = i + 1
    print(i)
    try:
        
        tickers = ("KRW-BTC", "KRW-ETH", "KRW-XRP", "KRW-HBAR", "KRW-DOT", "KRW-MBL", "KRW-LTC", "KRW-LINK", )
        for ticker in tickers:
            buyprice = buy_price(ticker)
            ma5 = get_ma5(ticker)
            ticker_balance = upbit.get_balance(ticker)
            krw = upbit.get_balance("KRW")
            print("check :", ticker)
            if buyprice > ma5:
                if krw > 5000 and upbit.get_balance(ticker) < 0.001:
                    upbit.buy_market_order(ticker, krw*0.2)
                    print("Buy complete:", ticker, krw*0.2)
            
            else:
                if ticker_balance > 0.001:
                    upbit.sell_market_order(ticker, ticker_balance)
                    print("Sell complete:", ticker, ticker_balance)
                time.sleep(1)
                
            print("checked :", ticker, ticker_balance, krw)
    except Exception as e:
        print(e)
        time.sleep(1)
print("autotrade end")
