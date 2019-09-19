#!/usr/bin/env python3

import subprocess
import os
import signal
import gi
import time
import requests
import locale
locale.setlocale(locale.LC_ALL, '')
gi.require_version('Gtk', '3.0')
gi.require_version('AppIndicator3', '0.1')
gi.require_version('Notify', '0.7')
from gi.repository import Gtk, AppIndicator3, GObject
from gi.repository import Notify as notify
from threading import Thread
currpath = os.path.dirname(os.path.realpath(__file__))

coins = ['btc', 'eth', 'ae', 'link', 'eos', 'ht', 'dock', 'egt']

class Indicator():
    def __init__(self):
        self.symbol = 'btcusdt'
        self.app = 'update_setting'
        self.path = currpath
        self.indicator = AppIndicator3.Indicator.new(
            self.app, currpath + "/icons/btc.png",
            AppIndicator3.IndicatorCategory.SYSTEM_SERVICES)
        self.indicator.set_status(AppIndicator3.IndicatorStatus.ACTIVE)
        self.indicator.set_menu(self.create_menu())
        # the thread:
        self.update = Thread(target=self.background_monitor)
        # daemonize the thread to make the indicator stopable
        self.update.setDaemon(True)
        self.update.start()
        notify.init(self.app)

    def create_menu(self):
        self.menu = Gtk.Menu()

        for coin in coins:
            item = Gtk.MenuItem(coin.upper() + '/USDT')
            item.connect('activate', self.select_coin)
            self.menu.append(item)

        # quit
        item_quit = Gtk.MenuItem('Quit')
        sep = Gtk.SeparatorMenuItem()
        self.menu.append(sep)
        item_quit.connect('activate', self.stop)
        self.menu.append(item_quit)
        self.menu.show_all()
        return self.menu

    def select_coin(self, item):
        coin = item.get_label().split('/')[0].lower()
        self.symbol = coin + 'usdt'
        self.indicator.set_icon(currpath + "/icons/" + coin + ".png")

    def background_monitor(self):
        btc_price = self.huobi_btc_price()
        mark_price = btc_price

        while True:
            change = ''
            last_price = btc_price
            btc_price = self.huobi_btc_price() or last_price

            mark_price = self.check_alert(btc_price, mark_price)

            self.indicator.set_label(' $' + f'{btc_price:n}' + change, '')
            time.sleep(1)

    def check_alert(self, price, mark_price):
        delta = 100.0 * (price - mark_price) / mark_price
        gain = 1.0 if self.symbol == 'egtusdt' else 0.1

        if delta > gain or delta < -1 * gain:
            self.alert(delta, price)
            return price

        return mark_price

    def alert(self, delta, price):
        price_label = ' $' + f'{price:n}'
        delta_label = f'{delta:n}' + ' %'
        notify.Notification.new(self.symbol + " " + price_label, delta_label, None).show()

    def blockchain_btc_price(self):
        try:
            r = requests.get('https://blockchain.info/ticker')
            return r.json()['USD']['last']
        except Exception as e:
            return None

    def huobi_btc_price(self):
        try:
            r = requests.get('https://api.huobi.pro/market/detail/merged?symbol=' + self.symbol)

            if self.symbol == 'btcusdt':
                return round(r.json()['tick']['close'])
            else:
                return r.json()['tick']['close']
        except Exception as e:
            return None

    def binance_btc_avg_price(self):
        try:
            r = requests.get('https://api.binance.com/api/v1/klines?symbol=' + self.symbol.upper() + 'USDT&interval=1m&limit=1')
            return int(r.json()[0][4].split('.')[0])
        except Exception as e:
            return None

    def run_script(self, widget, script):
        subprocess.Popen(["/bin/bash", "-c", script])

    def stop(self, source):
        Gtk.main_quit()


Indicator()
signal.signal(signal.SIGINT, signal.SIG_DFL)
Gtk.main()
