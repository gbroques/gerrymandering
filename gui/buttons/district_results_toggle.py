from gui.buttons.buttons import TOGGLE_BUTTON_TEXT
from gui.buttons.buttons import create_toggle_button


class DistrictResultsToggle:
    __toggle_results = False

    def __init__(self, root, canvas, coordinates):
        self.__coordinates = coordinates
        self.__button = create_toggle_button(root,
                                             lambda: self.__toggle_district_results(canvas))

    def reset(self, coordinates):
        self.__coordinates = coordinates
        self.__toggle_results = False
        self.__button['text'] = 'Show ' + TOGGLE_BUTTON_TEXT

    def __toggle_district_results(self, canvas):
        self.__toggle_results = False if self.__toggle_results else True
        if self.__toggle_results:
            self.__show_district_results(canvas)
        else:
            self.__hide_district_results(canvas)

    def __show_district_results(self, canvas):
        canvas.color_district_grid_by_winner(self.__coordinates)
        self.__button['text'] = 'Hide ' + TOGGLE_BUTTON_TEXT

    def __hide_district_results(self, canvas):
        canvas.color_district_grid_by_district(self.__coordinates)
        self.__button['text'] = 'Show ' + TOGGLE_BUTTON_TEXT

    def grid(self, **kwargs):
        self.__button.grid(kwargs)

    def config(self, **kwargs):
        self.__button.config(kwargs)
