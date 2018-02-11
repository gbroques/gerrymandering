from constants import OUTPUT_FILE
from contiguous_coordinate_list import ContiguousCoordinateList
from coordinates import from_coordinates_to_grid
from statistics import print_statistics
from util import get_border
from util import get_voter_map
from util import print_to_screen_and_file

DISTRICT_GRID_BORDER_LENGTH = 20


# TODO: Give a more descriptive name
class OutputPrinter:
    __voter_map = get_voter_map()

    def __init__(self, contiguous_coordinate_list):
        self.text_file = None
        self.__contiguous_coordinate_list = ContiguousCoordinateList(contiguous_coordinate_list)

    def print_output(self):
        self.text_file = open(OUTPUT_FILE, "w")

        self.__print_num_contiguous()

        self.__print_district_grids()

        self.__print_legend()

        print_statistics(self.text_file,
                         self.__contiguous_coordinate_list.num_wins,
                         self.__contiguous_coordinate_list.winning_ratios,
                         len(self.__contiguous_coordinate_list))

        self.__print_output_file_generated_message()

        self.text_file.close()

    @property
    def winning_ratios(self):
        return self.__contiguous_coordinate_list.winning_ratios

    def __print_num_contiguous(self):
        num_contiguous = len(self.__contiguous_coordinate_list)
        message = 'We generated ' + str(num_contiguous) + ' contiguous random redistricting schemes.\n'
        print_to_screen_and_file(message, self.text_file)

    def __print_district_grids(self):
        for contiguous_coordinates in self.__contiguous_coordinate_list:
            grid = from_coordinates_to_grid(contiguous_coordinates)
            self.__print_district_grid(grid)

    def __print_district_grid(self, district_grid):
        border = get_border('═', DISTRICT_GRID_BORDER_LENGTH)
        self.__print_top_border(border)
        self.__print_district_grid_columns(district_grid)
        self.__print_bottom_border(border)

    def __print_district_grid_columns(self, district_grid):
        for i in range(len(district_grid)):
            self.__print_district_grid_column(district_grid, i)

    def __print_district_grid_column(self, district_grid, i):
        print_to_screen_and_file('║', self.text_file, end='')
        self.__print_district_grid_row(district_grid, i)
        print_to_screen_and_file('║', self.text_file)

    def __print_district_grid_row(self, district_grid, i):
        for j in range(len(district_grid[i])):
            self.__print_district_and_party(district_grid, i, j)

    def __print_district_and_party(self, district_map, i, j):
        district_and_party = self.__get_district_and_party_string(district_map, i, j)
        print_to_screen_and_file(' ' + district_and_party + ' ', self.text_file, end='')

    def __get_district_and_party_string(self, district_map, i, j):
        party = self.__voter_map[i][j]
        district = str(district_map[i][j])
        return district + party[0]

    def __print_top_border(self, border):
        print_to_screen_and_file('╔' + border + '╗', self.text_file)

    def __print_bottom_border(self, border):
        print_to_screen_and_file('╚' + border + '╝\n', self.text_file)

    def __print_legend(self):
        print_to_screen_and_file('LEGEND', self.text_file)
        print_to_screen_and_file('  G - Green', self.text_file)
        print_to_screen_and_file('  P - Purple\n', self.text_file)

    @staticmethod
    def __print_output_file_generated_message():
        print("\nStatistics report generated. See file '" + OUTPUT_FILE + "'.")
