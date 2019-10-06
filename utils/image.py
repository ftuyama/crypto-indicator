#!/usr/bin/env python3

import random
import sys
from PIL import Image
from PIL import ImageDraw

class ImageUtil():
    def __init__(self, symbol):
        self.symbol = symbol

    def generate_icon(self, data):
        self.plot(data)
        return self.side_by_side(['assets/chart/chart.png', f'icons/{self.symbol}.png'])

    def plot(self, data):
        im = Image.new('RGBA', (128, 128), (0, 0, 0, 0))
        draw = ImageDraw.Draw(im)

        min_price = min(data)
        max_price = max(data)
        data = [128 - 128 * (data[t] - min_price) / max((max_price - min_price), 1) if t < len(data) else min_price for t in range(129)]

        points = [(t, data[t]) for t in range(129)]

        draw.polygon(points, fill='blue')
        im.save('assets/chart/chart.png')

    def side_by_side(self, imgs):
        images = [Image.open(path) for path in imgs]
        widths, heights = zip(*(i.size for i in images))

        total_width = sum(widths)
        max_height = max(heights)

        new_im = Image.new('RGBA', (total_width, max_height))

        x_offset = 0
        for im in images:
            new_im.paste(im, (x_offset, 0))
            x_offset += im.size[0]

        icon_name = f'assets/chart/icon{random.randint(1, 11)}.png'
        new_im.save(icon_name)

        return icon_name

# ImageUtil('btcf').generate_icon([8100, 8101, 8110, 8095, 8090, 8101, 8110, 8095, 8090, 8101, 8110, 8095, 8090, 8101, 8110, 8095, 8090, 8101, 8110, 8095, 8090, 8101, 8110, 8095, 8090, 8101, 8110, 8095, 8090, 8101, 8110, 8095, 8090, 8101, 8110, 8095, 8090, 8101, 8110, 8095, 8090, 8101, 8110, 8095, 8090, 8101, 8110, 8095, 8090, 8101, 8110, 8095, 8090, 8101, 8110, 8095, 8090, 8101, 8110, 8095, 8090, 8101, 8110, 8095, 8090, 8101, 8110, 8095, 8090, 8101, 8110, 8095, 8090])
