import unittest

from PIL import Image

from uwo_ps_utils import market_rates_cropper as mrc

class MarketRatesCropperTest(unittest.TestCase):
    def test_get_selected_goods_cell(self):
        im = Image.new("RGB", (800, 600), (255, 255, 255))
        with self.assertRaises(Exception):
            mrc.get_selected_goods_cell_image(im)

        im = Image.open("sample_screenshot.png")
        self.assertIsNotNone(mrc.get_selected_goods_cell_image(im))

    def test_get_nearby_towns_cell(self):
        im = Image.new("RGB", (800, 600), (255, 255, 255))
        with self.assertRaises(Exception):
            mrc.get_nearby_towns_cell_images(im)

        im = Image.open("sample_screenshot.png")
        self.assertEquals(4, len(mrc.get_nearby_towns_cell_images(im)))
