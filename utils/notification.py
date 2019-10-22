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

    def check_alert(self, symbol, price):
        if symbol != self.last_symbol:
            self.last_symbol = symbol
            self.mark_price = None
            self.last_price = None

        if self.last_price is None:
            self.last_price = price
            return

        delta = 100.0 * (price - self.last_price) / self.last_price
        gain = 0.2 if symbol == 'btcusdt' else 0.5
        super_gain = 0.35 if symbol == 'btcusdt' else 1.0
        self.last_price = price

        self.custom_notification(price)

        if symbol == 'btcusdt':
            if delta > super_gain:
                self.alert_sound('great.mp3')
            elif delta > gain:
                self.alert_sound('good.wav')
            elif delta < -1 * super_gain:
                self.alert_sound('wrong.wav')
            elif delta < -1 * gain:
                self.alert_sound('beep.wav')

        if delta > gain or delta < -1 * gain:
            self.alert_notification(symbol, delta, price)

    def custom_notification(self, price):
        self.timer += 1
        if self.timer % 30 == 0:
            self.mark_price = price
            self.timer = 1

        if self.mark_price is None:
            self.mark_price = price
            return

        big_delta = 100.0 * (price - self.mark_price) / self.mark_price

        if big_delta > 0.9:
            self.alert_sound('YES.mp3')
        elif big_delta > 0.5:
            self.alert_sound('great.mp3')
        elif big_delta > 0.25:
            self.alert_sound('good.wav')
        elif big_delta < -0.9:
            self.alert_sound('nuclear.wav')
        elif big_delta < -0.5:
            self.alert_sound('alert.wav')
        elif big_delta < -0.25:
            self.alert_sound('beep.wav')
        else:
            return

        self.mark_price = price

    def alert_notification(self, symbol, delta, price):
        date = time.strftime("%Y-%m-%d %H:%M:%S")
        price_label = f' ${price:n}'
        delta_label = f'{delta:n}' + ' %'
        notify.Notification.new(symbol + " " + price_label, delta_label + " on " + date, None).show()

    def alert_sound(self, sound):
        sound_thread = threading.Thread(target=playsound, args=[f'assets/alerts/{sound}'])
        sound_thread.start()
