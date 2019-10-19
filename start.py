#!/usr/bin/env python3

import subprocess
import os
import signal
import gi
import time
import locale

from api.api import Api
from api.websocket import Websocket
from utils.image import ImageUtil
from utils.notification import Alert

locale.setlocale(locale.LC_ALL, '')
gi.require_version('Gtk', '3.0')
gi.require_version('AppIndicator3', '0.1')
gi.require_version('Notify', '0.7')

from gi.repository import Gtk, AppIndicator3
from gi.repository import Notify as notify
from threading import Thread

currpath = os.path.dirname(os.path.realpath(__file__))

coins = ['btc', 'eth', 'ae', 'link', 'eos', 'ht', 'dock', 'egt']
sources = ['Binance Futures', 'Binance', 'Huobi', 'Blockchain']

class Indicator():
    def __init__(self):
        self.api = Api()
        self.websocket = Websocket()
        self.image_util = ImageUtil("btcf")

        self.last_source = None
        self.update = None
        self.source = sources[0]
        self.symbol = 'btcusdt'
        self.app = 'update_setting'
        self.alert = Alert()

        self.path = currpath
        self.indicator = AppIndicator3.Indicator.new(
            self.app, currpath + "/icons/btc.png",
            AppIndicator3.IndicatorCategory.SYSTEM_SERVICES)
        self.indicator.set_status(AppIndicator3.IndicatorStatus.ACTIVE)
        self.create_menu()

        self.start_source()

        notify.init(self.app)

    def start_source(self):
        if self.source == self.last_source:
            return

        self.last_source = self.source
        self.websocket.close_ws()

        if self.source == 'Binance Futures':
            self.indicator.set_icon(currpath + "/icons/btcf.png")
            self.update = Thread(target=self.websocket.start_ws, args=[self])
            self.update.start()
        else:
            self.update = Thread(target=self.background_monitor)
            self.update.setDaemon(True)
            self.update.start()

    """Menu methods

        These methods handle menu interaction
    """
    def create_menu(self):
        self.menu = Gtk.Menu()

        group = []
        for source in sources:
            item = Gtk.RadioMenuItem.new_with_label(group, source)
            group = item.get_group()
            item.connect('activate', self.select_source)
            self.menu.append(item)

        self.menu.append(Gtk.SeparatorMenuItem())

        group = []
        for coin in coins:
            item = Gtk.RadioMenuItem.new_with_label(group, coin.upper() + '/USDT')
            group = item.get_group()
            item.connect('activate', self.select_coin)
            self.menu.append(item)

        # quit
        item_quit = Gtk.MenuItem('Quit')
        sep = Gtk.SeparatorMenuItem()
        self.menu.append(sep)
        item_quit.connect('activate', self.stop)
        self.menu.append(item_quit)
        self.menu.show_all()

        self.indicator.set_menu(self.menu)

        return self.menu

    def select_source(self, item):
        source = item.get_label()
        self.source = source
        self.start_source()

    def select_coin(self, item):
        coin = item.get_label().split('/')[0].lower()
        self.symbol = coin + 'usdt'
        self.indicator.set_icon(currpath + "/icons/" + coin + ".png")

    """Core methods

        These methods do a lot of stuff
    """
    def get_monitor(self):
        if self.source == 'Binance':
            return self.api.binance_symbol_avg_price
        elif self.source == 'Huobi':
            return self.api.huobi_symbol_price
        elif self.source == 'Blockchain':
            return self.api.blockchain_btc_price
        else:
            return self.api.blockchain_btc_price

    def background_monitor(self):
        print(f"### start {self.source} monitor ###")

        monitor = self.get_monitor()
        source = self.source

        while source == self.source and monitor is not None:
            symbol_price = monitor(self.symbol)
            self.alert.check_alert(self.symbol, symbol_price)

            self.indicator.set_label(f' ${symbol_price:n}', '')
            time.sleep(1)

    def stop(self, _arg):
        self.websocket.close_ws()
        Gtk.main_quit()


Indicator()
signal.signal(signal.SIGINT, signal.SIG_DFL)
Gtk.main()
