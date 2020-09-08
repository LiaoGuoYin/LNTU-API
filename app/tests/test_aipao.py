import unittest

from app.aipao import core


class MyTestCase(unittest.TestCase):
    def test_aipao_core_check_imei_code(self):
        valid_imei_code = 'd584b33e9a3e484da5e13eb38e73fc25'
        self.assertIsInstance(core.check_imei_code(valid_imei_code), dict)

        invalid_imei_code = valid_imei_code + 'invalid'
        self.assertRaises(Exception, core.check_imei_code, invalid_imei_code)


if __name__ == '__main__':
    unittest.main()