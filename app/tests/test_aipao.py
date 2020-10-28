import unittest

from app.aipao import core


class TestAiPao(unittest.TestCase):
    def test_aipao_core_check_imei_code(self):
        valid_imei_code = 'd584b33e9a3e484da5e13eb38e73fc25'
        # self.assertIsInstance(core.check_imei_code(valid_imei_code), dict) # 无法保证每次都有有效的 IMEICode 来测试
        invalid_imei_code = valid_imei_code + 'invalid'
        self.assertTrue(core.check_imei_code(invalid_imei_code).id == -1)


if __name__ == '__main__':
    unittest.main()
