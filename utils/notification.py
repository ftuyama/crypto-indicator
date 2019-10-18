#!/usr/bin/env python3

from playsound import playsound
from gi.repository import Notify as notify
import time

class Alert():
    def __init__(self):
        self.timer = 0
        self.mark_price = None
        self.last_price = None

    def check_alert(self, symbol, price):
        if self.last_price is None:
            self.last_price = price
            return

        delta = 100.0 * (price - self.last_price) / self.last_price
        gain = 0.3 if symbol == 'btcusdt' else 1.0

        self.custom_notification(price)

        if symbol == 'btcusdt':
            if delta > gain:
                self.alert_sound('good')
            elif delta < -1 * gain:
                self.alert_sound('beep')

        if delta > gain or delta < -1 * gain:
            self.alert_notification(symbol, delta, price)

        self.last_price = price

    def custom_notification(self, price):
        self.timer += 1
        if self.timer % 60 == 0:
            self.timer = 1

            if self.mark_price is None:
                self.mark_price = price
                return

            big_delta = 100.0 * (price - self.mark_price) / self.mark_price
            self.mark_price = price

            if big_delta > 0.9:
                self.alert_sound('YES')
            elif big_delta > 0.6:
                self.alert_sound('great')
            elif big_delta > 0.3:
                self.alert_sound('good')
            elif big_delta < -0.3:
                self.alert_sound('beep')
            elif big_delta < -0.6:
                self.alert_sound('alert')
            elif big_delta < -0.9:
                self.alert_sound('nuclear')

    def alert_notification(self, symbol, delta, price):
        date = time.strftime("%Y-%m-%d %H:%M:%S")
        price_label = f' ${price:n}'
        delta_label = f'{delta:n}' + ' %'
        notify.Notification.new(symbol + " " + price_label, delta_label + " on " + date, None).show()

    def alert_sound(self, sound):
        playsound(f'assets/alerts/{sound}.wav')
