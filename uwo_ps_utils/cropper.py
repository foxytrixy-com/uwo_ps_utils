"""This module get the cropped image from the screenshot.
But to get the cropped image from 'Market Rates' screen,
use 'market_rates_cropper.py'.

About variables:
chat : A line of chat. This contains teller and message.
       If the message is more than one line, it contains only the first line.
msg : The message area of chat
"""
from PIL import Image

# To find colon position of chat.
COLON_BYTES = b'\x00\x00\x00\x00\x00\x00\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\xff\xff\xff\xff\xff'

TH = 200    #Threshhold
def __clear_bg(c):
    return int(c / TH) * 255

def get_chats(im):
    """This function gets the chatting messages.

    Arguments:
        im (PIL.Image.Image): Image object

    Return:
        Image object list (PIL.Image.Image).
        [0]: The most latest chatting message. e.g, The most below messages.
    """
    return get_chat_msg(im)

def get_chat_msg(im):
    """This function gets the chatting messages.

    Arguments:
        im (PIL.Image.Image): Image object

    Return:
        Image object list (PIL.Image.Image).
        [0]: The most latest chatting message. e.g, The most below messages.
    """
    chat_rects = __get_chat_rects(im.size)
    chats = []
    for r in chat_rects:
        chats.append(im.crop(r))

    return chats

def get_teller(chat):
    """Get teller rect image from chat image

    Arguments:
        msg (PIL.Image.Image): Image object

    Return:
        teller (PIL.Image.Image): Image object
    """
    return chat.crop((13, 0, 123, chat.height))

def get_msg(chat):
    """Get message rect image from chat image

    Arguments:
        chat (PIL.Image.Image): Image object

    Return:
        message (PIL.Image.Image): Image object
    """
    if COLON_BYTES == chat.crop((147, 0, 149, chat.height)).point(__clear_bg).tobytes():
        left = 147
    elif COLON_BYTES == chat.crop((158, 0, 160, chat.height)).point(__clear_bg).tobytes():
        left = 158
    else:
        return None

    return chat.crop((left + 6, 0, chat.width, chat.height))    # add padding for backward compability

def get_first_token_from_msg(msg):
    """Get the first token image from message

    Arguments:
        msg (PIL.Image.Image): Image object

    Return:
        token (PIL.Image.Image): Image object
    """
    return msg.crop((0, 0, 70, msg.height))

def get_first_token(chat):
    """Get the first token image from chat image

    Arguments:
        chat (PIL.Image.Image): Image object

    Return:
        token (PIL.Image.Image): Image object
    """
    return chat.crop((140, 0, 210, chat.height))

def get_plummet_second_token_from_msg(msg):
    """Get the second token image from message when plummeted

    Arguments:
        msg (PIL.Image.Image): Image object

    Return:
        token (PIL.Image.Image): Image object
    """
    return msg.crop((75, 0, 102, msg.height))

def get_plummet_second_token(chat):
    """Get the second token image from chat image when plummeted


    Arguments:
        msg (PIL.Image.Image): Image object

    Return:
        token (PIL.Image.Image): Image object
    """
    return chat.crop((215, 0, 242, chat.height))

def get_flooded_second_token_from_msg(msg):
    """Get the first token image from message when flooded

    Arguments:
        msg (PIL.Image.Image): Image object

    Return:
        token (PIL.Image.Image): Image object
    """
    return msg.crop((202, 0, 229, msg.height))

def get_flooded_second_token(chat):
    """Get the first token image from chat image when flooded

    Arguments:
        chat (PIL.Image.Image): Image object

    Return:
        token (PIL.Image.Image): Image object
    """
    return chat.crop((342, 0, 369, chat.height))

def __get_chat_rects(wh):
    """Get rects from the image size.

    Arguments:
        wh (tuple) : (width, height)

    Return:
        rects (list) : [(left, top, right, bottom), ...]
    """
    rects = []
    left = 0
    right = 600
    height = wh[1]
    msg_cnt = 5
    sy = -50
    step = -20
    for y in range(msg_cnt):
        rects.append((left, height + sy, right, height + sy + 10))
        sy = sy + step

    return rects
