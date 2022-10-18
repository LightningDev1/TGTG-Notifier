"""
Utility functions
"""

from io import BytesIO

from PIL import Image, ImageDraw, ImageFont

import prettytable as pt


def prettytable_to_image(table: pt.PrettyTable, dark: bool = True) -> Image.Image:
    "Convert a prettytable to an image"

    background_color = "#333" if dark else "#fff"
    text_color = "#fff" if dark else "#000"

    table_text = table.get_string()

    # Table width: amount of characters until a newline
    table_width = table_text.find("\n")

    # Table height: amount of newlines
    table_height = len(table_text.split("\n"))

    # 21 and 38 are used to estimate the width and height of the image
    # with the table. These values were found by trial and error.
    image = Image.new("RGB", (table_width * 21, table_height * 38), background_color)
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype("CascadiaCode.ttf", 34)
    draw.text((10, 10), table_text, font=font, fill=text_color)

    return image


def image_to_io(image: Image.Image) -> BytesIO:
    "Convert an image to a BytesIO object"

    bytes_io = BytesIO()
    image.save(bytes_io, format="PNG")
    bytes_io.seek(0)

    return bytes_io
