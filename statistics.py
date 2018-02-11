"""
Helper functions for printing out statistics.
"""

from util import print_to_screen_and_file
from util import get_border


def print_statistics(text_file, num_wins, winning_ratios, num_contiguous):
    """Prints statistics report.

    Includes:
      * A report header
      * Percentage of which ratio won each election
      * Percentage of elections each party won
    """
    __print_statistics_report_header(text_file)

    __print_winning_ratios(text_file, winning_ratios, num_contiguous)

    for party in num_wins.keys():
        percent_won = __get_percent_elections_won(num_wins, party, num_contiguous)
        __print_percent_won(text_file, party, percent_won)


def __get_percent_elections_won(num_wins, party, num_contiguous):
    """Get the percentage of elections won by a party

    :param num_wins: A dictionary containing parties as keys and election wins as values.
    :param party: The party.
    :param num_contiguous: The number of contiguous redistrictings.
    :return: The percent of total elections won.
    """
    num_elections_won = num_wins[party]
    return num_elections_won / num_contiguous * 100


def __print_statistics_report_header(text_file):
    """Print the header to the statistics report."""
    report_title = 'STATISTICS REPORT'
    print_to_screen_and_file(report_title, text_file)
    border = get_border('-', len(report_title))
    print_to_screen_and_file(border, text_file)


def __print_percent_won(text_file, party, percentage_won):
    """Print the percentage of elections the party won."""
    message = party + " won " + str(round(percentage_won, 2)) + "% percent of elections."
    print_to_screen_and_file(message, text_file)


def __print_winning_ratios(text_file, winning_ratios, num_contiguous):
    for key in winning_ratios.keys():
        ratio = key.split(':')
        num_green_wins = ratio[0]
        num_purple_wins = ratio[1]
        message = "Green won " + num_green_wins + " districts "
        message += "and Purple won " + num_purple_wins + " districts "
        percent = winning_ratios[key] / num_contiguous * 100
        message += str(round(percent, 2)) + "% of the time."
        print_to_screen_and_file(message, text_file)
    print_to_screen_and_file("", text_file)  # Print extra newline character

