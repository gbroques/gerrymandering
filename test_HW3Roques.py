import unittest
from HW3Roques import is_grid_contiguous

class HW3Roques(unittest.TestCase):

    def test_is_grid_contiguous(self):
        contiguous_grid = self.get_contiguous_grid()

        non_contiguous_grid = self.get_non_contiguous_grid()

        self.assertTrue(is_grid_contiguous(contiguous_grid))
        self.assertFalse(is_grid_contiguous(non_contiguous_grid))

    def get_contiguous_grid(self):
        """Get a contiguous grid representing a redistricting scheme."""

        return [[1, 2, 4, 4, 4],
                [2, 1, 1, 5, 4],
                [2, 2, 1, 5, 4],
                [3, 2, 1, 3, 5],
                [3, 3, 3, 5, 5]]

    def get_non_contiguous_grid(self):
        """Get a non-contiguous redistricting scheme."""

        return [[1, 2, 4, 4, 4],
                [2, 1, 1, 5, 4],
                [2, 2, 1, 5, 4],
                [3, 2, 3, 3, 5],
                [3, 3, 3, 5, 5]]


if __name__ == '__main__':
    unittest.main()
