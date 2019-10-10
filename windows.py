from pystray import Icon as icon, Menu as menu, MenuItem as item
from PIL import Image, ImageDraw, ImageFont
from threading import Thread

state = False

def create_image():
    # Generate an image and draw a pattern
    image = Image.open('icons/btcf.png')

    return image

def create_text():
    # Generate an image and draw a pattern
    image = Image.new('RGBA', (255, 255), (0, 0, 0, 0))
    dc = ImageDraw.Draw(image)

    font_type  = ImageFont.truetype("assets/Roboto-Regular.ttf", 115)
    price = 8050
    dc.text((0, 100), f"{price}", fill=(255, 255, 255), font = font_type)

    return image

def on_clicked(icon, item):
    global state
    state = not item.checked

# Update the state in `on_clicked` and return the new state in
# a `checked` callable
indicator = icon('test1', create_image(), menu=menu(
    item(
        'Checkable',
        on_clicked,
        checked=lambda item: state)))

thread = Thread(target=indicator.run)
thread.start()

icon('test2', create_text(), menu=menu(
    item(
        'Checkable',
        on_clicked,
        checked=lambda item: state))).run()