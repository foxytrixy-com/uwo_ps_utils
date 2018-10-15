"""This module get the cropped image from the screenshot.
But to get the cropped image from 'Market Rates' screen,
use 'market_rates_cropper.py'.
"""
from PIL import Image

CHAT_MSG_RECT = []

def get_chat_msg(im):
    """This function gets the chatting messages.

    Arguments:
        im (PIL.Image.Image): Image object

    Return:
        Image object list (PIL.Image.Image).
        [0]: The most latest chatting message. e.g, The most below messages.
    """
    __get_rects(im.size)
    chats = []
    for r in CHAT_MSG_RECT:
        chats.append(im.crop(r))

    return chats

def get_teller(chat):
    """Get teller rect image from chat image

    Arguments:
        msg (PIL.Image.Image): Image object

    Return:
        teller (PIL.Image.Image): Image object
    """
    return chat.crop((0, 0, 110, chat.height))

def get_msg(chat):
    """Get message rect image from chat image

    Arguments:
        chat (PIL.Image.Image): Image object

    Return:
        message (PIL.Image.Image): Image object
    """
    return chat.crop((140, 0, chat.width, chat.height))

def get_first_token(chat):
    """Get the first token image from chat image

    Arguments:
        msg (PIL.Image.Image): Image object

    Return:
        token (PIL.Image.Image): Image object
    """
    return chat.crop((140, 0, 210, chat.height))

def get_plummet_second_token(chat):
    """Get the second token image from chat image when plummeted


    Arguments:
        msg (PIL.Image.Image): Image object

    Return:
        token (PIL.Image.Image): Image object
    """
    return chat.crop((215, 0, 242, chat.height))

def get_flooded_second_token(chat):
    """Get the first token image from chat image when flooded

    Arguments:
        msg (PIL.Image.Image): Image object

    Return:
        token (PIL.Image.Image): Image object
    """
    return chat.crop((342, 0, 369, chat.height))

def __get_rects(wh):
    """Get rects from the image size.
    This will initialize CHAT_MSG_RECT variable

    Arguments:
        wh (tuple) : (width, height)
    """
    left = 13
    right = 500
    height = wh[1]
    msg_cnt = 5
    sy = -50
    step = -20
    CHAT_MSG_RECT.clear()
    for y in range(msg_cnt):
        CHAT_MSG_RECT.append((left, height + sy, right, height + sy + 10))
        sy = sy + step
