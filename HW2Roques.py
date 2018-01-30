
'''
Name: G Roques
Date: 1/30/18
Course: [CS4500] Intro to the Software Profession - Section 001
Version: 1.0.0

Output Files:
  * HW2output.txt (generated in the same directory as the program)

Sources:
  * https://docs.python.org/ 
  * https://jeffknupp.com/blog/2014/06/18/improve-your-python-python-classes-and-object-oriented-programming/

Description:
  A python program to explore redestricting schemes with a set of 25 voters.
  There are 15 green voters, and 10 purple voters. Making a 60-40 split.
  In each election, there is one green candidate, and one purple candidate in each district.
  Green voters always for the green candidate, and the purple voter always vote for the purple candidate.
  Statistics are output to the terminal and a file named "HW2output.txt":
    * The percentage of elections won
    * The average number of districts won per election
'''

from random import randint
from enum import Enum

# Name of output file
OUTPUT_FILE = "HW2output.txt"

# Total number of redistricting schemes
NUM_REDISTRICTING_SCHEMES = 1000000  # 1 million

# Total number of voters
NUM_VOTERS = 25

# Total number of districts
NUM_DISTRICTS = 5

# Total number of voters in each district
NUM_VOTERS_IN_DISTRICT = 5

# Total number of green voters
MAX_GREEN_VOTERS = 15

# Total number of purple voters
MAX_PURPLE_VOTERS = 10

def main():
    text_file = open(OUTPUT_FILE, "w")

    # Keep track of how many times each party wins an election
    num_wins = {
        Party.GREEN: 0,
        Party.PURPLE: 0
    }

    # Keep track of the average number of districts each party wins per election
    avg_district_wins = {
        Party.GREEN: 0,
        Party.PURPLE: 0
    }

    # Keep track which ration wins each election
    # "Number of districts green wins":"Number of districts purple wins"
    winning_ratios = {
      "2:3": 0,
      "3:2": 0,
      "4:1": 0,
      "5:0": 0
    }

    print("Running " + str(NUM_REDISTRICTING_SCHEMES) + " redistrictings (this may take awhile)...\n")

    for i in range(NUM_REDISTRICTING_SCHEMES):
        voters = get_voters()

        district_winners = VoterHelper.get_district_winners(voters)
        num_districts_won = VoterHelper.get_num_districts_won(district_winners)
        winning_ratio = VoterHelper.get_winning_ratio(district_winners)
        winning_ratios[winning_ratio] += 1

        update_avg_district_wins(avg_district_wins, num_districts_won)
        
        election_winner = VoterHelper.get_election_winner(district_winners)
        num_wins[election_winner] += 1
        
        PartyHelper.reset_num_voters()

    print_statistics(text_file, num_wins, avg_district_wins, winning_ratios)

    text_file.close()

def get_voters():
    """Get a list of Voter objects."""

    voters = []
    for i in range(NUM_VOTERS):
        party = PartyHelper.get_party()
        district = DistrictHelper.get_district(i)
        voters.append(Voter(party, district))
    return voters

def get_percent_elections_won(num_wins, party):
    """Get the percentage of elections won by a party

    :param num_wins: A dictionary containing parties as keys and election wins as values
    :return: The percent of total elections won
    """
    num_elections_won = num_wins[party]
    return num_elections_won / NUM_REDISTRICTING_SCHEMES * 100

def update_avg_district_wins(avg_district_wins, num_districts_won):
    """Update the average number of districts each party wins per election."""

    for party in avg_district_wins.keys():
        avg_district_wins[party] += num_districts_won[party] / NUM_REDISTRICTING_SCHEMES

def print_statistics(text_file, num_wins, avg_district_wins, winning_ratios):
    """Prints statistics of interest."""   
    print_statistics_report_header(text_file)

    print_winning_ratios(text_file, winning_ratios)

    for party in num_wins.keys():
        percent_won = get_percent_elections_won(num_wins, party)
        print_percent_won(text_file, party, percent_won)
        print_avg_num_districts_won(text_file, party, avg_district_wins[party])

def print_statistics_report_header(text_file):
    print_to_screen_and_file("STATISTICS REPORT", text_file)
    print_to_screen_and_file("-----------------", text_file)

def print_percent_won(text_file, party, percentage_won):
    """Print the percentage of elections the party won."""

    message = str(party) + " won " + str(round(percentage_won, 2)) + "% percent of elections."
    print_to_screen_and_file(message, text_file)

def print_avg_num_districts_won(text_file, party, avg_district_wins):
    """Print the average number of districts a party won per election."""

    message = str(party) + " won " + str(round(avg_district_wins, 2)) + " districts on average per election."
    print_to_screen_and_file(message, text_file)

def print_winning_ratios(text_file, winning_ratios):
    for key in winning_ratios.keys():
        ratio = key.split(':')
        num_green_wins = ratio[0]
        num_purple_wins = ratio[1]
        message = "Green won " + num_green_wins + " districts "
        message += "and Purple won " + num_purple_wins + " districts "
        percent = winning_ratios[key] / NUM_REDISTRICTING_SCHEMES * 100
        message += str(round(percent, 2)) + "% of the time."
        print_to_screen_and_file(message, text_file)
    print_to_screen_and_file("", text_file)  # Print extra newline character

def print_to_screen_and_file(message, file):
    """Prints a message to the screen and a file."""
    
    print(message)
    file.write(message + "\n")

class Party(Enum):
    GREEN = 1
    PURPLE = 2

    def __str__(self):
        return self.name.capitalize()

class Voter:
    """A class representing a voter.
    Each voter has the following properties:

    Attributes:
        party: A enum representing the party a voter belongs to.
        district: A number representing which district the voter belongs to.
    """

    def __init__(self, party, district):
        """Return a Voter object with a party and district."""

        self.party = party
        self.district = district

class MaxVoterError(Exception):
    """Raised when the number of maximum voters is exceeded."""
    pass

class PartyHelper:
    """A helper class to get which party a voter belongs to."""

    num_green_voters = 0
    num_purple_voters = 0

    @classmethod
    def reset_num_voters(cls):
        cls.num_green_voters = 0
        cls.num_purple_voters = 0

    @classmethod
    def get_party(cls):
        """Get a randomly generated political party that a voter belongs to."""

        if cls.num_green_voters == MAX_GREEN_VOTERS and cls.num_purple_voters == MAX_PURPLE_VOTERS:
            raise MaxVoterError("You can't get a party when more than the maximum number of voters have been created.")
    
        is_green = randint(0, 1)

        if cls.num_green_voters == MAX_GREEN_VOTERS and cls.num_purple_voters != MAX_PURPLE_VOTERS:
            is_green = 0

        if cls.num_green_voters != MAX_GREEN_VOTERS and cls.num_purple_voters == MAX_PURPLE_VOTERS:
            is_green = 1

        if is_green:
            party = Party.GREEN
            cls.num_green_voters += 1
        else:
            party = Party.PURPLE
            cls.num_purple_voters += 1
        return party

class DistrictHelper:
    """A helper class to get which district a voter belongs to."""
        
    district = 1

    @classmethod
    def get_district(cls, voter_index):
        """Get the district for a particular voter based upon an index."""

        if voter_index % NUM_DISTRICTS == 0 and voter_index != 0:
            cls.district += 1

        return cls.district

class VoterHelper:
    """A helper class for handling a list of voter objects."""

    def get_district_winners(voters):
        """Get the party who won each district.

        :param voters: A list of voter objects
        :return: A dictionary where keys are districts and values are parties.
        """
        district_winners = dict.fromkeys(range(1, NUM_DISTRICTS + 1), 0)

        district = 1
        num_green_votes = 0
        num_purple_votes = 0
        for i in range(1, NUM_VOTERS + 1):
            voter = voters[i - 1]
            if (voter.party is Party.GREEN):
                num_green_votes += 1

            if (voter.party is Party.PURPLE):
                num_purple_votes += 1

            if i % NUM_DISTRICTS == 0:
                if num_green_votes > num_purple_votes:
                    district_winners[district] = Party.GREEN
                else:
                    district_winners[district] = Party.PURPLE
                num_green_votes = 0
                num_purple_votes = 0
                district += 1

        return district_winners

    def get_num_districts_won(district_winners):
        """Get the number of districts each party won per election."""

        num_districts_won = {
            Party.GREEN: 0,
            Party.PURPLE: 0
        }
        for party in district_winners.values():
            num_districts_won[party] += 1
        return num_districts_won

    def print_district_winners(district_winners):
        """Print which party won each district."""
       
        for district in district_winners.keys():
            message = "District " + str(district)
            message += " winner is "
            message += str(district_winners[district])
            print(message)

    def get_election_winner(district_winners):
        """Get the election winner from the district winners.

        :param district_winners: A dictionary where keys are districts and values are parties.
        :return: The party who won the election.
        """
        num_green_votes = 0
        num_purple_votes = 0
        for party in district_winners.values():
            if party is Party.GREEN:
                num_green_votes += 1

            if party is Party.PURPLE:
                num_purple_votes += 1

        if num_green_votes > num_purple_votes:
            return Party.GREEN
        else:
            return Party.PURPLE

    def print_election_winner(election_winner):
        """Print the party who won the election"""

        print("Election winner is " + str(election_winner))

    def get_winning_ratio(district_winners):
        """Get how many districts green won vs the number of districts purple won."""
        num_green_wins = 0
        num_purple_wins = 0
        for party in district_winners.values():
            if party is Party.GREEN:
                num_green_wins += 1
            else:
                num_purple_wins += 1
        return str(num_green_wins) + ":" + str(num_purple_wins)


if __name__ == '__main__':
    main()
