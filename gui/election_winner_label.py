from tkinter import Label
from tkinter import StringVar

from constants import G
from gui.styles import LABEL_FONT


class ElectionWinnerLabel:
    def __init__(self, root, election_winner, winning_ratio):
        self.__text = self.__get_election_winner_text(election_winner, winning_ratio)
        self.__label = Label(root, textvariable=self.__text, font=LABEL_FONT)

    def __get_election_winner_text(self, election_winner, winning_ratio):
        election_winner_text = self.__build_election_winner_text(election_winner, winning_ratio)
        return StringVar(value=election_winner_text)

    @staticmethod
    def __build_election_winner_text(election_winner, winning_ratio):
        num_green_wins, num_purple_wins = winning_ratio.split(':')
        if election_winner == G:
            winning_ratio_text = num_green_wins + ' to ' + num_purple_wins
        else:
            winning_ratio_text = num_purple_wins + ' to ' + num_green_wins
        return 'Election Winner: ' + election_winner + ' ' + winning_ratio_text

    def set_election_winner(self, election_winner, winning_ratio):
        self.__text.set(self.__build_election_winner_text(election_winner, winning_ratio))

    def set_text(self, text):
        self.__text.set(text)

    def grid(self, **kwargs):
        self.__label.grid(kwargs)