from constants import G
from coordinates import get_district_winners
from coordinates import get_districts_from_coordinates
from gui.buttons import TOGGLE_BUTTON_TEXT
from gui.buttons import create_toggle_button
from gui.colors import get_district_color


class DistrictResultsToggle:
    __toggle_results = False

    def __init__(self, root, canvas, coordinates):
        self.__coordinates = coordinates
        self.__button = create_toggle_button(root,
                                             lambda: self.__toggle_district_results(canvas))

    def set_coordinates(self, coordinates):
        self.__coordinates = coordinates

    def reset(self):
        self.__toggle_results = False
        self.__button['text'] = 'Show ' + TOGGLE_BUTTON_TEXT

    def __toggle_district_results(self, canvas):
        self.__toggle_results = False if self.__toggle_results else True
        if self.__toggle_results:
            self.__show_district_results(canvas)
        else:
            self.__hide_district_results(canvas)

    def __show_district_results(self, canvas):
        districts = get_districts_from_coordinates(self.__coordinates)
        winners = get_district_winners(self.__coordinates)
        for i in range(len(districts)):
            winner = winners[districts[i]]
            fill = 'lime' if winner == G else 'magenta'
            canvas.itemconfig(canvas.tiles[i], fill=fill)
        self.__button['text'] = 'Hide ' + TOGGLE_BUTTON_TEXT

    def __hide_district_results(self, canvas):
        districts = get_districts_from_coordinates(self.__coordinates)
        for i in range(len(districts)):
            district = districts[i]
            fill = get_district_color(district)
            canvas.itemconfig(canvas.tiles[i], fill=fill)
        self.__button['text'] = 'Show ' + TOGGLE_BUTTON_TEXT

    def grid(self, **kwargs):
        self.__button.grid(kwargs)

    def config(self, **kwargs):
        self.__button.config(kwargs)
