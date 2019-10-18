#!/usr/bin/env python3

from playsound import playsound
from gi.repository import Notify as notify
import time

class Alert():
    def __init__(self):
        self.mark_price = None

    def check_alert(self, symbol, price):
        if self.mark_price is None:
            self.mark_price = price
            return

        delta = 100.0 * (price - self.mark_price) / self.mark_price
        gain = 0.3 if symbol == 'btcusdt' else 1.0

        if symbol == 'btcusdt':
            if delta > 0.3:
                self.alert_sound('good')
            elif delta < -0.3:
                self.alert_sound('beep')

        if delta > gain or delta < -1 * gain:
            self.alert_notification(symbol, delta, price)

        self.mark_price = price

    def alert_notification(self, symbol, delta, price):
        date = time.strftime("%Y-%m-%d %H:%M:%S")
        price_label = f' ${price:n}'
        delta_label = f'{delta:n}' + ' %'
        notify.Notification.new(symbol + " " + price_label, delta_label + " on " + date, None).show()

    def alert_sound(self, sound):
        playsound(f'assets/alerts/{sound}.wav')
