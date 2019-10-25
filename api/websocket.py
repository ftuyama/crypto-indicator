#!/usr/bin/env python3

# from api.api import Api
import json
import websocket
import os

currpath = os.path.dirname(os.path.realpath(__file__))

class Websocket():
    def __init__(self):
        self.ws = None

    def start_ws(self, father):
        self.ws = websocket.WebSocketApp("wss://fstream.binance.com/stream?streams=btcusdt@miniTicker",
                                on_message = lambda ws, msg: self.on_message(ws, msg),
                                on_error = lambda ws, error: self.on_error(ws, error),
                                on_open = lambda ws: self.on_open(ws),
                                on_close = lambda ws: self.on_close(ws))

        # self.data = Api().binance_futures_history()
        self.father = father
        self.ws.run_forever()

    def close_ws(self):
        if self.ws is not None:
            self.ws.close()

    """Websocket methods

        These methods manipulate websocket
    """
    def on_message(self, ws, message):
        self = self.father
        self.btc_price = int(float(json.loads(message)["data"]["c"]))
        self.alert.check_alert(self.symbol, self.btc_price)

        # self.data.append(self.btc_price)
        # self.data = self.data[-120:]

        # icon = self.image_util.generate_icon(self.data)
        # self.indicator.set_icon(currpath + f"/../{icon}")
        self.indicator.set_label(f' ${self.btc_price:n}', '')

    def on_error(self, ws, error):
        print(error)

    def on_close(self, ws):
        print("### closed websocket ###")

    def on_open(self, ws):
        print("### open websocket ###")
