import unittest
from HW3Roques import *

class HW3Roques(unittest.TestCase):

    contiguous_grid = [[1, 2, 4, 4, 4],
                       [2, 1, 1, 5, 4],
                       [2, 2, 1, 5, 4],
                       [3, 2, 1, 3, 5],
                       [3, 3, 3, 5, 5]]

    non_contiguous_grid = [[1, 2, 4, 4, 4],
                           [2, 1, 1, 5, 4],
                           [2, 2, 1, 5, 4],
                           [3, 2, 3, 3, 5],
                           [3, 3, 3, 5, 5]]

    def test_is_grid_contiguous(self):
        self.assertTrue(is_grid_contiguous(self.contiguous_grid))
        self.assertFalse(is_grid_contiguous(self.non_contiguous_grid))


if __name__ == '__main__':
    unittest.main()
