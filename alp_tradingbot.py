
# ======================
# IMPORTANT!!! README!!!

# DISCLAIMER:

# This software is meant as a developer's template to build actual trading bots, the goal of this software is to be a template framework between your bot and alpaca,
# forsaken the hours put into figuring out the syntax and basic logic of pull data and trading 
# this is 3rd party software unaffiliated with Alpaca

# DO NOT TRY TO USE THIS AS A FINISHED TRADING BOT, IT'S NOT !!
# The author is not responsible for any losses made through using this software !
# Trade at your own risk !
# ======================



import time
from datetime import datetime
import pytz
import yfinance as yf
import pandas as pd
import alpaca_trade_api as tradeapi

# ======================
# CONFIG
# ======================
API_KEY = "YOUR PUBLIC KEY" #replace these with your keys from Alpaca API
API_SECRET = "YOUR PRIVATE KEY"
BASE_URL = "https://paper-api.alpaca.markets"  # change to live if needed
SYMBOL = "AAPL" #replace this with the stock that you want to trade

#conditions and metrics, change to whatever you want in your trade logic
RISE_THRESHOLD = 0.002    # +0.2% rise in 5 min
STOP_LOSS = 0.02          # 2% stop loss
TAKE_PROFIT = 0.02        # 2% take profit
TRADE_DURATION = 300      # 5 minutes
EST = pytz.timezone("US/Eastern")
SLEEP_TIME = 60
QTY = 1

api = tradeapi.REST(API_KEY, API_SECRET, BASE_URL)

# ======================
# FUNCTIONS
# ======================
#check for open trading hours (make sure this matchs the official trading hours for your stock)
def market_open():
    now = datetime.now(EST)
    return (
        now.weekday() < 5 and
        (now.hour > 9 or (now.hour == 9 and now.minute >= 30)) and
        now.hour < 16
    )
#pulls recent data, to determine wether to buy or not, this is used as an example but for more accurate ways to pull data a subscription is needed with Alpaca or other data platforms. 
#!!For actual live trading do not use this way of pulling recent data as there may be data inaccuracies!!
def get_last_5min_closes(symbol):
    """
    Return the last two 5-min closes (previous, current) from Yahoo Finance,
    along with their timestamps in US/Eastern timezone.
    """
    df = yf.download(
        tickers=symbol,
        period="1d",
        interval="5m",
        progress=False,
        auto_adjust=False  # prevent warning
    )

    if len(df) < 2:
        return None, None, None, None

    # Last two rows
    last_two = df.tail(2).copy()

    # Convert UTC index to US/Eastern
    last_two.index = last_two.index.tz_convert("US/Eastern")

    prev_time = last_two.index[0]
    curr_time = last_two.index[1]
    prev_close = last_two["Close"].iloc[0].item()  # safe scalar extraction
    curr_close = last_two["Close"].iloc[1].item()

    return prev_time, prev_close, curr_time, curr_close


#place the order according to Alpaca's API
def place_order(trade_type, qty, symbol, current_price):
    entry_price = current_price
    stop_loss_price = round(entry_price * (1 - STOP_LOSS), 2)
    take_profit_price = round(entry_price * (1 + TAKE_PROFIT), 2)

    print(f"Entry: {entry_price:.2f}, Stop Loss: {stop_loss_price:.2f}, Take Profit: {take_profit_price:.2f}")

    order = api.submit_order(
        symbol=symbol,
        qty=qty,
        side=trade_type,
        type="market",
        time_in_force="day",
        order_class="bracket",
        stop_loss={"stop_price": stop_loss_price},
        take_profit={"limit_price": take_profit_price}
    )

    return entry_price, stop_loss_price, take_profit_price, order.id

#main function , change this to whatever trading logic you wish to use
def trade():
    print("🚀 Starting AAPL 5-min rise bot...")
    try:
        holding = False
        order_id = None
        entry_time = None
        entry_price = None

        while True:
            if market_open():
                now = datetime.now(EST)
                print(f"⏰ {now.strftime('%Y-%m-%d %H:%M:%S')} ET")

                try:
                    prev_time, prev_close, curr_time, curr_close = get_last_5min_closes(SYMBOL)

                    if prev_close is None or curr_close is None:
                        print("⚠️ Not enough data yet.")
                        time.sleep(SLEEP_TIME)
                        continue


                    rise_pct = (curr_close - prev_close) / prev_close
                    print(f"📊 [{prev_time.strftime('%Y-%m-%d %H:%M:%S %Z')}] "
                          f"Prev close: {prev_close:.2f} | "
                          f"[{curr_time.strftime('%Y-%m-%d %H:%M:%S %Z')}] "
                          f"Curr close: {curr_close:.2f} | Rise: {rise_pct:.3%}")

                    if not holding and rise_pct >= RISE_THRESHOLD:
                        print(f"📈 Rise {rise_pct:.2%} → BUY at {curr_close}")
                        entry_price, sl, tp, order_id = place_order("buy", QTY, SYMBOL, curr_close)
                        entry_time = now
                        holding = True

                    if holding:
                        elapsed = (now - entry_time).total_seconds()
                        if elapsed >= TRADE_DURATION:
                            print(f"⏹️ {TRADE_DURATION//60} min passed → force exit at {curr_close}")

                            # Cancel bracket
                            try:
                                api.cancel_order(order_id)
                                print("✅ Cancelled bracket order.")
                            except Exception as e:
                                print(f"⚠️ Failed to cancel bracket order: {e}")

                            # Close manually
                            api.submit_order(
                                symbol=SYMBOL,
                                qty=QTY,
                                side="sell",
                                type="market",
                                time_in_force="day"
                            )
                            holding = False

                except Exception as e:
                    print(f"⚠️ Error: {e}")

            else:
                print("🛑 Market closed — waiting...")

            time.sleep(SLEEP_TIME)

    except KeyboardInterrupt:
        print("🛑 Trading bot stopped manually.")


# ======================
# MAIN
# ======================
if __name__ == "__main__":
    trade()
