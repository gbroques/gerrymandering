from gui.styles import LABEL_FONT
from tkinter import Label
from gui.pie_chart import get_pie_chart_piece_color
from tkinter import DISABLED


class WinningRatioLabels:
    def __init__(self, root, winning_ratios):
        """Construct winning ratio labels.

        :param root: Root TK instance.
        :param winning_ratios: A list of winning ratios.
        """
        self.length = len(winning_ratios)
        self.__labels = [None for _ in range(self.length)]
        self.__create(root, winning_ratios)

    def __create(self, root, winning_ratios):
        for i in range(self.length):
            kwargs = self.__get_kwargs(winning_ratios[i], get_pie_chart_piece_color(i))
            self.__labels[i] = Label(root, **kwargs)

    @staticmethod
    def __get_kwargs(text, activebackground):
        return {
            'text': text,
            'font': LABEL_FONT,
            'activebackground': activebackground,
            'state': DISABLED
        }

    def __getitem__(self, key):
        return self.__labels[key]

