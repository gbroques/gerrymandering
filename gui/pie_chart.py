from gui.colors import get_pie_chart_piece_color
from tkinter import HIDDEN

_CIRCUMFERENCE = 1000


class PieChart:
    def __init__(self, num_pieces):
        self.num_pieces = num_pieces
        self.pieces = [None for _ in range(num_pieces)]

    def create(self, canvas, percents):
        coordinates = (100, 100, 400, 400)
        start_arc = 0
        for i in range(self.num_pieces):
            color = get_pie_chart_piece_color(i)
            extent = percents[i] * _CIRCUMFERENCE
            kwargs = self.__get_arc_kwargs(color, start_arc, extent)
            self.pieces[i] = canvas.create_arc(coordinates, **kwargs)
            if extent + start_arc >= _CIRCUMFERENCE:
                break
            start_arc = extent

    @classmethod
    def __get_arc_kwargs(cls, color, start, extent):
        return {
            'fill': color,
            'outline': color,
            'start': cls.__proportion(start),
            'extent': cls.__proportion(extent),
            'state': HIDDEN  # Hide pie chart by default
        }

    @staticmethod
    def __proportion(n):
        return 360.0 * n / _CIRCUMFERENCE


def get_pie_chart_percents(winning_ratios, total):
    percents = []
    for key in winning_ratios.keys():
        percents.append(winning_ratios[key] / total)
    return percents
