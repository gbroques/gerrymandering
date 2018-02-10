import unittest

from HW4Roques import find_start_positions
from HW4Roques import get_contiguous_coordinates
from HW4Roques import get_district_winners
from HW4Roques import is_district_contiguous
from HW4Roques import is_grid_contiguous


class HW4Roques(unittest.TestCase):
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

    def test_get_district_winners(self):
        expected_district_winners = {
            1: 'Purple',
            2: 'Green',
            3: 'Purple',
            4: 'Green',
            5: 'Purple'
        }
        coordinates = get_contiguous_coordinates()
        district_winners = get_district_winners(coordinates)
        self.assertEqual(expected_district_winners, district_winners)

    def test_is_district_contiguous(self):
        self.assertTrue(is_district_contiguous(self.contiguous_grid, (0, 0)))
        self.assertFalse(is_district_contiguous(self.non_contiguous_grid, (0, 0)))

    def test_find_start_positions(self):
        expected_start_positions = {
            1: (0, 0),
            2: (0, 1),
            3: (3, 0),
            4: (0, 2),
            5: (1, 3)
        }

        start_positions = find_start_positions(self.contiguous_grid)

        self.assertEqual(start_positions, expected_start_positions)

    def test_is_grid_contiguous(self):
        self.assertTrue(is_grid_contiguous(self.contiguous_grid))
        self.assertFalse(is_grid_contiguous(self.non_contiguous_grid))


if __name__ == '__main__':
    unittest.main()
