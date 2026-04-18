import unittest
import math_utils

class MathUtilsTests(unittest.TestCase):
    def test_add(self):
        self.assertEqual(math_utils.add(2, 3), 5)

    def test_subtract(self):
        self.assertEqual(math_utils.subtract(10, 4), 6)

if __name__ == '__main__':
    unittest.main()
