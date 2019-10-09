#!/usr/bin/env python3

# from api.api import Api
import json
import websocket
import os

currpath = os.path.dirname(os.path.realpath(__file__))

"""Websocket methods

    These methods manipulate websocket
"""
def on_message(ws, message):
    self = ws.father

    self.btc_price = int(float(json.loads(message)["data"]["c"]))
    self.mark_price = self.check_alert(self.btc_price, self.mark_price)

    # self.data.append(self.btc_price)
    # self.data = self.data[-120:]

    # icon = self.image_util.generate_icon(self.data)
    # self.indicator.set_icon(currpath + f"/../{icon}")
    self.indicator.set_label(' $' + f'{self.btc_price:n}', '')

def on_error(ws, error):
    print(error)

def on_close(ws):
    print("### closed websocket ###")

def on_open(ws):
    print("### open websocket ###")

class Websocket():
    def __init__(self):
        self.ws = None

    def start_ws(self, father):
        self.ws = websocket.WebSocketApp("wss://fstream.binance.com/stream?streams=btcusdt@miniTicker",
                                on_message = on_message,
                                on_error = on_error,
                                on_close = on_close)

        self.ws.on_open = on_open
        self.ws.father = father
        self.ws.father.btc_price = 1
        self.ws.father.mark_price = 1
        # ws.father.data = Api().binance_futures_history()

        self.ws.run_forever()

    def close_ws(self):
        if self.ws is not None:
            self.ws.close()
