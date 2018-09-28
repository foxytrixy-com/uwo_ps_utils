import unittest

from PIL import Image

from uwo_ps_utils import market_rates_cropper as mrc

class MarketRatesCropperTest(unittest.TestCase):
    def test_get_selected_goods_cell(self):
        im = Image.new("RGB", (800, 600), (255, 255, 255))
        with self.assertRaises(Exception):
            mrc.get_selected_goods_cell_image(im)

        im = Image.open("./tests/sample_screenshot.png")
        self.assertIsNotNone(mrc.get_selected_goods_cell_image(im))

    def test_get_nearby_towns_cell(self):
        im = Image.new("RGB", (800, 600), (255, 255, 255))
        with self.assertRaises(Exception):
            mrc.get_nearby_towns_cell_images(im)

        im = Image.open("./tests/sample_screenshot.png")
        self.assertEquals(4, len(mrc.get_nearby_towns_cell_images(im)))

    def test_get_bar_images_from_cells(self):
        im = Image.open("./tests/sample_screenshot.png")
        cells = mrc.get_nearby_towns_cell_images(im)
        bars = mrc.get_bar_images_from_cells(cells)
        self.assertEquals((190, 1), bars[3].size)

    def test_convert_bar_to_rates(self):
        rates = mrc.convert_bar_to_rates([])
        self.assertListEqual([], rates)

        im = Image.open("./tests/sample_screenshot.png")
        cells = mrc.get_nearby_towns_cell_images(im)
        bars = mrc.get_bar_images_from_cells(cells)
        rates = mrc.convert_bar_to_rates(bars)
        self.assertAlmostEqual(128, rates[0], delta=3)
        self.assertAlmostEqual(88, rates[1], delta=3)
        self.assertAlmostEqual(96, rates[2], delta=3)
        self.assertAlmostEqual(96, rates[3], delta=3)
