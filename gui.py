from tkinter import *

from constants import G
from constants import NUM_DISTRICTS
from coordinates import get_district_winners
from coordinates import get_districts_from_coordinates

TITLE = 'Gerrymandering'
CANVAS_DIMENSION = 500


class App:

    __coordinate_list = []
    __current_district = 0
    __root = None
    __canvas = None
    __tiles = [None for _ in range(NUM_DISTRICTS * NUM_DISTRICTS)]
    __district_nums = [None for _ in range(NUM_DISTRICTS * NUM_DISTRICTS)]
    __toggle_button = None
    __prev_button = None
    __next_button = None
    __toggle_results = False

    def __init__(self, coordinate_list):
        self.__coordinate_list = coordinate_list
        self.__init_root()
        self.__init_canvas()

        self.__create_canvas()
        winner = StringVar(value='Election Winner: ')
        winner_label = Label(self.__root, textvariable=winner, font=('Helvetica', 16))
        self.__create_buttons()
        self.__init_grid_layout(winner_label)

    def run_mainloop(self):
        self.__root.mainloop()

    def __init_grid_layout(self, winner_label):
        self.__root.columnconfigure(0, weight=1)
        self.__root.columnconfigure(1, weight=1)
        self.__root.columnconfigure(2, weight=1)
        self.__canvas.grid(row=0, columnspan=3, padx=15, pady=15)
        winner_label.grid(row=1, columnspan=3, pady=15, sticky=W+E)
        self.__prev_button.grid(row=2, column=0, sticky=W+E, padx=15, pady=15)
        self.__toggle_button.grid(row=2, column=1, sticky=W+E, pady=15)
        self.__next_button.grid(row=2, column=2, sticky=W+E, padx=15, pady=15)

    def __create_buttons(self):
        button_font = ('Helvetica', 16)

        toggle_button_kwargs = self.__get_toggle_button_kwargs(button_font)
        self.__toggle_button = Button(self.__root, toggle_button_kwargs)

        next_button_kwargs = self.__get_next_button_kwargs(button_font)
        self.__next_button = Button(self.__root, next_button_kwargs)

        prev_button_kwargs = self.__get_prev_button_kwargs(button_font)
        self.__prev_button = Button(self.__root, prev_button_kwargs)

    def __get_toggle_button_kwargs(self, button_font):
        return {
            'text': 'Show District Results',
            'command': lambda: self.__toggle_district_results(),
            'font': button_font
        }

    def __init_canvas(self):
        self.__canvas = Canvas(self.__root,
                               width=CANVAS_DIMENSION,
                               height=CANVAS_DIMENSION,
                               background='white')

    def __init_root(self):
        self.__root = Tk()
        self.__root.title(TITLE)

    def __handle_next(self):
        self.__current_district += 1
        self.__prev_button.config(state=NORMAL)
        self.__next_button.config(state=self.__is_next_button_enabled())
        self.__redraw()

    def __handle_prev(self):
        self.__current_district -= 1
        self.__prev_button.config(state=self.__is_prev_button_enabled())
        self.__next_button.config(state=self.__is_next_button_enabled())
        self.__redraw()

    def __is_prev_button_enabled(self):
        return DISABLED if self.__current_district == 0 else NORMAL

    def __is_next_button_enabled(self):
        num_coordinates = len(self.__coordinate_list)
        return DISABLED if self.__current_district == (num_coordinates - 1) else NORMAL

    def __redraw(self):
        coordinates = self.__coordinate_list[self.__current_district]
        districts = get_districts_from_coordinates(coordinates)
        for i in range(NUM_DISTRICTS):
            for j in range(NUM_DISTRICTS):
                index = i * NUM_DISTRICTS + j
                district = districts[index]
                color = self.__get_district_color(district)
                self.__canvas.itemconfig(self.__tiles[index], fill=color)
                self.__canvas.itemconfig(self.__district_nums[index], text=district)
                self.__toggle_results = False
                self.__toggle_button['text'] = 'Show District Results'

    def __create_canvas(self):
        square_size = CANVAS_DIMENSION / NUM_DISTRICTS
        coordinates = self.__coordinate_list[self.__current_district]
        contiguous_districts = get_districts_from_coordinates(coordinates)

        for i in range(NUM_DISTRICTS):
            for j in range(NUM_DISTRICTS):
                index = i * NUM_DISTRICTS + j
                district = contiguous_districts[index]
                color = self.__get_district_color(district)
                square_coordinates = self.__get_square_coordinates(i, j, square_size)
                self.__tiles[index] = self.__canvas.create_rectangle(*square_coordinates, fill=color)
                font_coordinates = self.__get_font_coordinates(i, j, square_size)
                self.__district_nums[index] = self.__canvas.create_text(*font_coordinates, text=district, font=('Helvetica', 28))

    def __toggle_district_results(self):
        self.__toggle_results = False if self.__toggle_results else True
        if self.__toggle_results:
            self.__show_district_results()
        else:
            self.__hide_district_results()

    def __show_district_results(self):
        coordinates = self.__coordinate_list[self.__current_district]
        contiguous_districts = get_districts_from_coordinates(coordinates)
        winners = get_district_winners(coordinates)
        for i in range(NUM_DISTRICTS):
            for j in range(NUM_DISTRICTS):
                index = i * NUM_DISTRICTS + j
                winner = winners[contiguous_districts[index]]
                if winner == G:
                    fill = 'lime'
                else:
                    fill = 'magenta'

                self.__canvas.itemconfig(self.__tiles[index], fill=fill)
        self.__toggle_button['text'] = 'Hide District Results'

    def __hide_district_results(self):
        coordinates = self.__coordinate_list[self.__current_district]
        contiguous_districts = get_districts_from_coordinates(coordinates)
        for i in range(NUM_DISTRICTS):
            for j in range(NUM_DISTRICTS):
                index = i * NUM_DISTRICTS + j
                district = contiguous_districts[index]
                color = self.__get_district_color(district)
                self.__canvas.itemconfig(self.__tiles[index], fill=color)
        self.__toggle_button['text'] = 'Show District Results'

    def __get_next_button_kwargs(self, button_font):
        return {
            'text': 'Next',
            'font': button_font,
            'command': lambda: self.__handle_next()
        }

    def __get_prev_button_kwargs(self, button_font):
        return {
            'text': 'Previous',
            'font': button_font,
            'command': lambda: self.__handle_prev(),
            'state': DISABLED
        }

    @staticmethod
    def __get_font_coordinates(i, j, square_size):
        x = (square_size * j) + square_size / 2
        y = (square_size * i) + square_size / 2
        return x, y

    @staticmethod
    def __get_square_coordinates(i, j, square_size):
        x0 = square_size * j
        y0 = square_size * i
        x1 = square_size * (j + 1)
        y1 = square_size * (i + 1)
        return x0, y0, x1, y1

    @staticmethod
    def __get_district_color(district):
        colors = ['#f44336',  # Red
                  '#9C27B0',  # Purple
                  '#2196F3',  # Blue
                  '#4CAF50',  # Green
                  '#FFC107']  # Amber
        return colors[district - 1]
