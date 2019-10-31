#!/usr/bin/env python3

from playsound import playsound
import threading
import time
import gi
gi.require_version('Notify', '0.7')
from gi.repository import Notify as notify

class Alert():
    def __init__(self):
        self.timer = 0
        self.mark_price = None
        self.last_price = None
        self.last_symbol = None
        self.last_source = None

    def symbol_gain(self, symbol):
        if symbol == 'btcusdt':
            return 0.2
        elif symbol == 'dockusdt':
            return 1.0
        else:
            return 0.5

    def check_alert(self, source, symbol, price):
        if symbol != self.last_symbol or source != self.last_source:
            self.last_symbol = symbol
            self.last_source = source
            self.mark_price = None
            self.last_price = None
            return

        self.check_alert1(symbol, price)
        self.check_alert2(symbol, price)

    def check_alert1(self, symbol, price):
        if self.last_price is None:
            self.last_price = price
            return

        delta = 100.0 * (price - self.last_price) / self.last_price
        gain = self.symbol_gain(symbol)
        self.last_price = price

        if symbol == 'btcusdt':
            if delta > 2 * gain:
                self.alert_sound('great.mp3')
            elif delta > gain:
                self.alert_sound('good.wav')
            elif delta < -2 * gain:
                self.alert_sound('wrong.wav')
            elif delta < -1 * gain:
                self.alert_sound('beep.wav')

        if delta > gain or delta < -1 * gain:
            self.alert_notification(symbol, delta, price)

    def check_alert2(self, symbol, price):
        self.timer += 1
        if self.timer % 30 == 0:
            self.mark_price = price
            self.timer = 1

        if self.mark_price is None:
            self.mark_price = price
            return

        delta = 100.0 * (price - self.mark_price) / self.mark_price
        gain = self.symbol_gain(symbol)

        if delta > 3 * gain:
            self.alert_sound('YES.mp3')
        elif delta > 2 * gain:
            self.alert_sound('great.mp3')
        elif delta > 1 * gain:
            self.alert_sound('good.wav')
        elif delta < -3 * gain:
            self.alert_sound('nuclear.wav')
        elif delta < -2 * gain:
            self.alert_sound('alert.wav')
        elif delta < -1 * gain:
            self.alert_sound('beep.wav')
        else:
            return

        self.alert_notification(symbol, delta, price)
        self.mark_price = price

    def alert_notification(self, symbol, delta, price):
        date = time.strftime("%Y-%m-%d %H:%M:%S")
        price_label = f' ${price:n}'
        delta_label = f'{delta:n} %'
        notify.Notification.new(symbol.upper() + " " + price_label, delta_label + " on " + date, None).show()

    def alert_sound(self, sound):
        sound_thread = threading.Thread(target=playsound, args=[f'assets/alerts/{sound}'])
        sound_thread.start()
