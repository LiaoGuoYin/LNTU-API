import unittest

from models import CET


class ModelTest(unittest.TestCase):
    def setUp(self):
        pass

    def test_cet(self):
        CET.objects.create("大学英语4级（CET4）", "2019-12-14", "390.0")


if __name__ == "__main__":
    unittest.main()
