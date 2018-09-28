"""This module get trade goods, rates, arrows, town name images
from the screenshot.
"""
from PIL import Image

# Rectangle informations - Relative in a cell
TRADE_GOODS_IMAGE_RECT = (5, 7, 47, 31)
NEARBY_TOWNS_NAME_RECT = (54, 10, 118, 25)
RATES_RECT = (168, 31, 194, 44)
ARROW_RECT = (231, 31, 244, 44)
CELL_HEIGHT = 56

# Rectangle informations - Inventory Area
# All sizes are same - 247 x 223
TRADE_GOODS_RECT = {}
TRADE_GOODS_RECT[(800, 600)] = (69, 103, 316, 326)
TRADE_GOODS_RECT[(1024, 768)] = (181, 187, 428, 410)
TRADE_GOODS_RECT[(1152, 864)] = (245, 235, 492, 458)
TRADE_GOODS_RECT[(1280, 720)] = (309, 163, 556, 386)
TRADE_GOODS_RECT[(1280, 768)] = (309, 187, 556, 410)
TRADE_GOODS_RECT[(1280, 800)] = (309, 203, 556, 426)
TRADE_GOODS_RECT[(1280, 960)] = (309, 283, 556, 506)
TRADE_GOODS_RECT[(1280, 1024)] = (309, 315, 556, 538)
TRADE_GOODS_RECT[(1360, 768)] = (349, 187, 596, 410)
TRADE_GOODS_RECT[(1366, 768)] = (352, 187, 599, 410)
TRADE_GOODS_RECT[(1440, 900)] = (389, 253, 636, 476)
TRADE_GOODS_RECT[(1600, 900)] = (469, 253, 716, 476)
TRADE_GOODS_RECT[(1600, 1024)] = (469, 315, 716, 538)
TRADE_GOODS_RECT[(1680, 1050)] = (509, 328, 756, 551)
TRADE_GOODS_RECT[(1920, 1080)] = (629, 343, 876, 566)

# Rectangle informations  - Nearby Towns Area.
# All sizes are same - 247 x 279
NEARBY_TOWNS_RECT = {}
for __key in TRADE_GOODS_RECT:
    __rect = TRADE_GOODS_RECT[__key]
    NEARBY_TOWNS_RECT[__key] = (__rect[0] + 363, __rect[1], __rect[2] + 363,
                                __rect[3] + CELL_HEIGHT)

def get_images_from_screenshot(image_path):
    """This function generate image list from screenshot.

    Each index means:
        [0] : Image of selected trade goods.
        [1] : Market Rates of selected trade goods.
        [2] : Arrow of selected trade goods.
        [3] : Name of the 1st nearby town
        [4] : Market Rates of the 1st nearby town
        [5] : Arrow of the 1st nearby town
        [6] ~ [8] : the 2nd nearby town. this index may not exist.
        [9] ~ [11] : the 3rd nearby town. this index may not exist.
        [12] ~ [14] : the 4th nearby town. this index may not exist.
        [15] ~ [17] : the 5th nearby town. this index may not exist.
    """
    im = Image.open(image_path)
    images = __process_trade_goods(im)
    images += __process_nearby_towns(im)
    return images

def __process_trade_goods(im):
    cell = get_selected_goods_cell_image(im)
    images = []
    images += [cell.crop(TRADE_GOODS_IMAGE_RECT)]
    images += [cell.crop(RATES_RECT)]
    images += [cell.crop(ARROW_RECT)]

    return images

def get_selected_goods_cell_image(im):
    """Get selected trade goods cell image.

    Arguments:
        im (PIL.Image.Image): Image object

    Return
        Image object (PIL.Image.Image)
        None if there is no selected cell
    """
    inventory_rect = TRADE_GOODS_RECT[im.size]
    inventory_area = im.crop(inventory_rect)
    width = inventory_rect[2] - inventory_rect[0]
    for i in range(4):
        cell_rect = [0, CELL_HEIGHT * i,
                     width, CELL_HEIGHT * i + CELL_HEIGHT]
        cell = inventory_area.crop(cell_rect)
        if __is_selected_cell(cell):
            return cell

    raise Exception("No Selected Cell")


def __is_selected_cell(cell_image):
    r, g, b = (56, 158, 149)
    bound = 10
    raw_data = cell_image.tobytes()
    index = cell_image.size[0] * 3 * 3 + 3     # 1 left-up pixel from goods image

    return (r - bound) < raw_data[index] and raw_data[index] < (r + bound) \
        and (g - bound) < raw_data[index+1] and raw_data[index+1] < (g + bound) \
        and (b - bound) < raw_data[index+2] and raw_data[index+2] < (b + bound)

def __process_nearby_towns(im):
    images = []
    cells = get_nearby_towns_cell_images(im)
    for cell in cells:
        images.append(cell.crop(NEARBY_TOWNS_NAME_RECT))
        images.append(cell.crop(RATES_RECT))
        images.append(cell.crop(ARROW_RECT))

    if not images:
        raise Exception("No Nearby Towns")
    return images

def get_nearby_towns_cell_images(im):
    nearby_rect = NEARBY_TOWNS_RECT[im.size]
    nearby_area = im.crop(nearby_rect)
    width = nearby_rect[2] - nearby_rect[0]
    cells = []
    for i in range(5):
        cell_rect = [0, CELL_HEIGHT * i,
                     width, CELL_HEIGHT * i + CELL_HEIGHT]
        cell = nearby_area.crop(cell_rect)
        if __has_nearby_town(cell):
            cells.append(cell)

    if not cells:
        raise Exception("No Nearby Towns")
    return cells

def __has_nearby_town(cell_image):
    r, g, b = (178, 179, 179)   # the color of image outline
    bound = 10
    raw_data = cell_image.tobytes()
    index = cell_image.size[0] * 3 * 4 + 6

    return  (r - bound) < raw_data[index] and raw_data[index] < (r + bound) \
        and (g - bound) < raw_data[index+1] and raw_data[index+1] < (g + bound) \
        and (b - bound) < raw_data[index+2] and raw_data[index+2] < (b + bound)

def clear_outside(imgpath):
    """Clear outside of inventory and nearby towns area for privacy

    Arguments:
        imgpath (str): Image path

    Return:
        Image object (PIL.Image.Image)
    """
    im = Image.open(imgpath)
    width = im.size[0]
    height = im.size[1]
    inventory = TRADE_GOODS_RECT[im.size]
    towns = NEARBY_TOWNS_RECT[im.size]

    black_img = __make_black_img(width, towns[1] - 1)
    im.paste(black_img, (0, 0))

    black_img = __make_black_img(width, height - towns[3] - 1)
    im.paste(black_img, (0, towns[3] + 1))

    black_img = __make_black_img(inventory[0] - 1, height)
    im.paste(black_img, (0, 0))

    black_img = __make_black_img(towns[0] - inventory[2], height)
    im.paste(black_img, (inventory[2] + 1, 0))

    black_img = __make_black_img(width - towns[2] - 1, height)
    im.paste(black_img, (towns[2] + 1, 0))

    return im

def __make_black_img(w, h):
    return Image.new('RGB', (w, h), color=(0, 0, 0))

def get_rates_from_bar(im):
    """Get rates from bar in the cells

    Arguments:
        im obejct (PIL.Image.Image): Image object of screenshot

    Return:
        rates (list): str format of rates.
                      The sequence is current town and nearby towns
    """
    cells = [get_selected_goods_cell_image(im)]
    cells += get_nearby_towns_cell_images(im)
    bars = get_bar_images_from_cells(cells)
    return convert_bar_to_rates(bars)

def get_bar_images_from_cells(cells):
    bars = []
    for cell in cells:
        bars.append(cell.crop((55,49,245,50)))

    return bars

def convert_bar_to_rates(bars):
    rates = []
    for bar in bars:
        count, _ = list(filter(__colored_pixel, bar.getcolors()))[0]
        rates.append(int(count * 2.12))
    return rates

def __colored_pixel(pixels):
    _, rgb = pixels
    return not (rgb[0] < 75 and rgb[1] < 75 and rgb[2] < 75)