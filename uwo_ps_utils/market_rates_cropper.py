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
    trade_goods_rect = TRADE_GOODS_RECT[im.size]
    trade_goods_area = im.crop(trade_goods_rect)
    width = trade_goods_rect[2] - trade_goods_rect[0]
    images = []
    for i in range(4):
        cell = trade_goods_area.crop([0,
                                      CELL_HEIGHT * i,
                                      width,
                                      CELL_HEIGHT * i + CELL_HEIGHT])
        if __is_selected_cell(cell):
            images += [cell.crop(TRADE_GOODS_IMAGE_RECT)]
            images += [cell.crop(RATES_RECT)]
            images += [cell.crop(ARROW_RECT)]

    return images

def __is_selected_cell(cell_image):
    r, g, b = (56, 158, 149)
    bound = 10
    raw_data = cell_image.tobytes()
    index = cell_image.size[0] * 3 * 3 + 3     # 1 left-up pixel from goods image

    return (r - bound) < raw_data[index] and raw_data[index] < (r + bound) \
        and (g - bound) < raw_data[index+1] and raw_data[index+1] < (g + bound) \
        and (b - bound) < raw_data[index+2] and raw_data[index+2] < (b + bound)

def __process_nearby_towns(im):
    nearby_towns_rect = NEARBY_TOWNS_RECT[im.size]
    nearby_towns_area = im.crop(nearby_towns_rect)
    width = nearby_towns_rect[2] - nearby_towns_rect[0]
    images = []
    for i in range(5):
        nearby_towns_cell = nearby_towns_area.crop([0,
                                                    CELL_HEIGHT * i,
                                                    width,
                                                    CELL_HEIGHT * i + CELL_HEIGHT])
        if __has_nearby_town(nearby_towns_cell):
            images += [nearby_towns_cell.crop(NEARBY_TOWNS_NAME_RECT)]
            images += [nearby_towns_cell.crop(RATES_RECT)]
            images += [nearby_towns_cell.crop(ARROW_RECT)]
    return images

def __has_nearby_town(cell_image):
    r, g, b = (178, 179, 179)   # the color of image outline
    bound = 10
    raw_data = cell_image.tobytes()
    index = cell_image.size[0] * 3 * 4 + 6

    return  (r - bound) < raw_data[index] and raw_data[index] < (r + bound) \
        and (g - bound) < raw_data[index+1] and raw_data[index+1] < (g + bound) \
        and (b - bound) < raw_data[index+2] and raw_data[index+2] < (b + bound)