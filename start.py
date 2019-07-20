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
from gi.repository import Gtk, AppIndicator3, GObject
from threading import Thread
currpath = os.path.dirname(os.path.realpath(__file__))


class Indicator():
    def __init__(self):
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

    def create_menu(self):
        self.menu = Gtk.Menu()
        # quit
        item_quit = Gtk.MenuItem('Quit')
        sep = Gtk.SeparatorMenuItem()
        self.menu.append(sep)
        item_quit.connect('activate', self.stop)
        self.menu.append(item_quit)
        self.menu.show_all()
        return self.menu

    def background_monitor(self):
        price = ''
        btc_price = 0

        while True:
            change = ''
            last_price = btc_price
            btc_price = self.binance_btc_avg_price()

            if last_price > 0:
                if btc_price > last_price:
                    change = ' +'
                elif btc_price < last_price:
                    change = ' -'

            self.indicator.set_label(' $' + f'{btc_price:n}' + change, '')
            time.sleep(5)

    def binance_btc_avg_price(self):
        try:
            r = requests.get('https://api.binance.com/api/v3/avgPrice?symbol=BTCUSDT')
            return int(r.json()['price'].split('.')[0])
        except:
            return False

    def run_script(self, widget, script):
        subprocess.Popen(["/bin/bash", "-c", script])

    def stop(self, source):
        Gtk.main_quit()


Indicator()
signal.signal(signal.SIGINT, signal.SIG_DFL)
Gtk.main()