#!/usr/bin/env python3

import json
import websocket

"""Websocket methods

    These methods manipulate websocket
"""
def on_message(ws, message):
    self = ws.father

    self.btc_price = int(float(json.loads(message)["data"]["c"]))

    self.mark_price = self.check_alert(self.btc_price, self.mark_price)

    self.indicator.set_label(' $' + f'{self.btc_price:n}', '')

def on_error(ws, error):
    print(error)

def on_close(ws):
    print("### closed websocket ###")

def on_open(ws):
    print("### open websocket ###")

class Websocket():
    def start_ws(self, father):
        ws = websocket.WebSocketApp("wss://fstream.binance.com/stream?streams=btcusdt@miniTicker",
                                on_message = on_message,
                                on_error = on_error,
                                on_close = on_close)

        ws.on_open = on_open
        ws.father = father
        ws.father.btc_price = 1
        ws.father.mark_price = 1

        ws.run_forever()
