"""
A collection of utility functions.
"""

from constants import G
from constants import P


def get_border(char, length):
    """Get a border consisting of a character repeated multiple times.

    :param char: The character to make up the border.
    :param length: The length of the border.
    :return: A string consisting of the character repeated for the given length.
    """
    border = ''
    for i in range(length):
        border += char
    return border


def get_voter_map():
    """Get a 5x5 map representing the location of the voters.

    P - Purple
    G - Green
    """

    return [[P, G, G, G, G],
            [G, P, P, P, G],
            [G, P, G, G, G],
            [G, G, G, P, P],
            [P, G, P, G, P]]


def print_to_screen_and_file(message, file, end='\n'):
    """Prints a message to the screen and a file."""

    print(message, end=end)
    file.write(message + ('\n' if end == '\n' else ''))
