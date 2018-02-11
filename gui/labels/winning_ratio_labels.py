from tkinter import DISABLED
from tkinter import Label

from gui.labels.styles import LABEL_FONT
from gui.pie_chart import get_pie_chart_piece_color
from tkinter import ACTIVE

from tkinter import W
from tkinter import E


class WinningRatioLabels:
    def __init__(self, root, winning_ratios):
        """Construct winning ratio labels.

        :param root: Root tkinter instance.
        :param winning_ratios: A list of winning ratios.
        """
        self.length = len(winning_ratios)
        self.__labels = self.__create(root, winning_ratios)

    def __create(self, root, winning_ratios):
        """Create the winning ratio labels.

        Label background colors correspond to pie chart colors.
        """
        labels = []
        for i in range(self.length):
            kwargs = self.__get_kwargs(winning_ratios[i], get_pie_chart_piece_color(i))
            labels.append(Label(root, **kwargs))
        return labels

    def configure_layout(self, row, padding):
        for i in range(self.length):
            horizontal_padding = self.__get_padding(i, padding)
            self.__labels[i].grid(row=row, column=i, sticky=W + E, padx=horizontal_padding)

    def __get_padding(self, column, default_padding):
        """Add half padding to outer edges of label's row."""
        half_padding = default_padding / 2
        if self.__is_first_column(column):
            return default_padding, half_padding
        elif self.__is_last_column(column):
            return half_padding, default_padding
        else:
            return default_padding

    @staticmethod
    def __is_first_column(column):
        return column == 0

    def __is_last_column(self, column):
        return column == self.length - 1

    def disable(self):
        self.__toggle_state(False)

    def enable(self):
        self.__toggle_state(True)

    def __toggle_state(self, enabled):
        """Toggle the state of the labels from enabled to disabled and vise versa."""
        state = ACTIVE if enabled else DISABLED
        for i in range(self.length):
            self.__labels[i].config(state=state)

    @staticmethod
    def __get_kwargs(text, activebackground):
        return {
            'text': text,
            'font': LABEL_FONT,
            'activebackground': activebackground,
            'state': DISABLED
        }

    def __getitem__(self, key):
        """Overload square brackets '[]' operator."""
        return self.__labels[key]
