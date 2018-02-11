from constants import G
from constants import P
from district_winners import get_election_winner
from district_winners import get_winning_ratio
from coordinates import get_district_winners


class ContiguousCoordinateList:
    def __init__(self, contiguous_coordinate_list):
        self.__list = contiguous_coordinate_list

        # Keep track of how many times each party wins an election.
        self.num_wins = self.__initialize_num_wins()

        self.winning_ratios = self.__initialize_winning_ratios()

        for contiguous_coordinates in contiguous_coordinate_list:
            district_winners = get_district_winners(contiguous_coordinates)

            election_winner = get_election_winner(district_winners)
            self.num_wins[election_winner] += 1

            winning_ratio = get_winning_ratio(district_winners)
            self.winning_ratios[winning_ratio] += 1

    def __len__(self):
        return len(self.__list)

    def __iter__(self):
        self.i = 0
        return self

    def __next__(self):
        if self.i < len(self):
            result = self.__list[self.i]
            self.i += 1
            return result
        else:
            raise StopIteration

    @staticmethod
    def __initialize_num_wins():
        return {
            G: 0,
            P: 0
        }

    @staticmethod
    def __initialize_winning_ratios():
        """Initializes a dictionary to keep track which ratio wins each election.

        The key consists of the number of districts green won per election,
        versus the number of districts purple won per election.

        Key: 'num_green_wins:num_purple_wins'
        :return: Winning ratios dictionary.
        """
        return {
            '2:3': 0,
            '3:2': 0,
            '4:1': 0,
            '5:0': 0
        }
