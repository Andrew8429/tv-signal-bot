# signal_bot.py

import time
import os
from tradingview_ta import TA_Handler, Interval
from telegram_utils import send_telegram_message

# Asset Screener and Exchange Settings
coin_screeners = {
    "BTCUSDT": "crypto",
    "SOLUSDT": "crypto",
    "SUIUSDT": "crypto",
    "HYPEUSDT": "crypto",
    "ARBUSDT": "crypto",
    "FETUSDT": "crypto",
    "TAOUSDT": "crypto",
    "XAUUSD": "cfd",     # Gold
    "EURUSD": "forex"    # Euro
}

coin_exchanges = {
    "BTCUSDT": "BINANCE",
    "SOLUSDT": "BINANCE",
    "SUIUSDT": "BINANCE",
    "HYPEUSDT": "BINANCE",
    "ARBUSDT": "BINANCE",
    "FETUSDT": "BINANCE",
    "TAOUSDT": "BINANCE",
    "XAUUSD": "OANDA",    # CFDs
    "EURUSD": "FX_IDC"    # Forex
}

coins = list(coin_screeners.keys())

def check_signals():
    for coin in coins:
        try:
            screener = coin_screeners.get(coin, "crypto")
            exchange = coin_exchanges.get(coin, "BINANCE")

            handler = TA_Handler(
                symbol=coin,
                exchange=exchange,
                screener=screener,
                interval=Interval.INTERVAL_5_MINUTES
            )

            analysis = handler.get_analysis()
            recommendation = analysis.summary["RECOMMENDATION"]

            print(f"[{coin}] Recommendation: {recommendation}")

            if recommendation in ["BUY", "STRONG_BUY", "SELL", "STRONG_SELL"]:
                message = f"""
📈 <b>Signal for {coin}</b>
Exchange: <b>{exchange}</b>
Recommendation: <b>{recommendation}</b>
"""
                send_telegram_message(message.strip())

        except Exception as e:
            print(f"🚨 Error checking {coin}: {e}")

if __name__ == "__main__":
    print("🚀 TradingView Signal Bot Started...")
    while True:
        check_signals()
        time.sleep(300)  # 5 minutes delay
