import time
import pyupbit
import datetime
import requests

access = "fFR4uDrNrrIAaxcEgzBKpfQ8bytKpxep1o5psPhH"
secret = "3FNmMlFrn9g2K8fIzp9esFnAhUq4CHhbJJ3rtWze"
myToken = "xoxb-your-token"

def get_target_price(ticker, k):
    """변동성 돌파 전략으로 매수 목표가 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=2)
    target_price = df.iloc[0]['close'] + (df.iloc[0]['high'] - df.iloc[0]['low']) * k
    return target_price

def get_start_time(ticker):
    """시작 시간 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=1)
    start_time = df.index[0]
    return start_time

def get_ma20(ticker):
    """20(60분)틱 이동 평균선 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="minute", count=60)
    ma20 = df['close'].rolling(20).mean().iloc[-1]
    return ma20

def get_balance(coin):
    """잔고 조회"""
    balances = upbit.get_balances()
    for b in balances:
        if b['currency'] == coin:
            if b['balance'] is not None:
                return float(b['balance'])
            else:
                return 0

def get_current_price(ticker):
    """현재가 조회"""
    return pyupbit.get_orderbook(tickers=ticker)[0]["orderbook_units"][0]["ask_price"]

# 로그인
upbit = pyupbit.Upbit(access, secret)
print("autotrade start")

while True:
    try:
        now = datetime.datetime.now()
        start_time = get_start_time("KRW-XRP")
        end_time = start_time + datetime.timedelta(days=1)

        if start_time < now < end_time - datetime.timedelta(seconds=10):
            target_price = get_target_price("KRW-XRP", 0.2)
            ma20 = get_ma20("KRW-XRP")
            current_price = get_current_price("KRW-XRP")
            if target_price < current_price and ma20 < current_price:
                krw = get_balance("KRW")
                if krw > 5000:
                    buy_result = upbit.buy_market_order("KRW-XRP", krw*0.9995)
                    post_message(myToken,"#crypto", "XRP buy : " +str(buy_result))
        else:
            XRP = get_balance("XRP")
            if XRP > 3:
                sell_result = upbit.sell_market_order("KRW-XRP", XRP*0.9995)
                post_message(myToken,"#crypto", "XRP buy : " +str(sell_result))
        time.sleep(1)
    except Exception as e:
        print(e)
        post_message(myToken,"#crypto", e)
        time.sleep(1)