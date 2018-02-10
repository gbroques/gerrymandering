from tkinter import *

from constants import G
from constants import NUM_DISTRICTS
from coordinates import get_district_winners
from coordinates import get_districts_from_coordinates
from district_winners import get_election_winner
from district_winners import get_winning_ratio

TITLE = 'Gerrymandering'
CANVAS_DIMENSION = 500


def prop(n):
    return 360.0 * n / 1000


class App:
    __coordinate_list = []
    __winning_ratios = {}
    __current_district = 0
    __root = None
    __result_number_text = None
    __result_number_label = None
    __canvas = None
    __winner_text = None
    __tiles = [None for _ in range(NUM_DISTRICTS * NUM_DISTRICTS)]
    __district_nums = [None for _ in range(NUM_DISTRICTS * NUM_DISTRICTS)]
    __toggle_button = None
    __prev_button = None
    __next_button = None
    __aggregate_button = None
    __toggle_results = False
    __toggle_aggregate = False
    __pie_chart_pieces = None
    __ratio_labels = None

    def __init__(self, coordinate_list, winning_ratios):
        self.__coordinate_list = coordinate_list
        self.__winning_ratios = winning_ratios
        self.__pie_chart_pieces = [None for _ in range(len(winning_ratios.keys()))]
        self.__ratio_labels = [None for _ in range(len(winning_ratios.keys()))]
        self.__root = self.__init_root()
        self.__canvas = self.__init_canvas()

        self.__create_canvas()

        label_font = ('Helvetica', 16)

        self.__winner_text = self.__get_winner_text()
        winner_label = Label(self.__root, textvariable=self.__winner_text, font=label_font)

        result_number_text = self.__get_result_number_text()
        self.__result_number_text = StringVar(value=result_number_text)
        self.__result_number_label = Label(self.__root, textvariable=self.__result_number_text, font=label_font)

        self.__create_buttons()

        i = 0
        for key in winning_ratios.keys():
            self.__ratio_labels[i] = Label(self.__root,
                                           text=key,
                                           font=label_font,
                                           activebackground=self.__get_pie_chart_piece_color(i),
                                           state=DISABLED)
            i += 1

        self.__init_grid_layout(winner_label)

    def __get_result_number_text(self):
        num_results = len(self.__coordinate_list)
        return 'Result ' + str((self.__current_district + 1)) + ' out of ' + str(num_results)

    def __update_result_number_text(self):
        self.__result_number_text.set(self.__get_result_number_text())

    def run_mainloop(self):
        self.__root.mainloop()

    @staticmethod
    def __init_root():
        root = Tk()
        root.title(TITLE)
        root.resizable(width=False, height=False)
        return root

    def __init_grid_layout(self, winner_label):
        self.__root.columnconfigure(0, weight=1, uniform='a')
        self.__root.columnconfigure(1, weight=1, uniform='a')
        self.__root.columnconfigure(2, weight=1, uniform='a')
        self.__root.columnconfigure(3, weight=1, uniform='a')

        self.__root.rowconfigure(0, pad=40)
        self.__root.rowconfigure(2, pad=40)
        self.__root.rowconfigure(5, pad=40)

        self.__result_number_label.grid(row=0, columnspan=4)
        self.__canvas.grid(row=1, columnspan=4, padx=10)
        winner_label.grid(row=2, columnspan=4, sticky=W + E)
        self.__prev_button.grid(row=3, column=0, sticky=W + E, padx=10)
        self.__toggle_button.grid(row=3, column=1, columnspan=2, sticky=W + E)
        self.__next_button.grid(row=3, column=3, sticky=W + E, padx=10)
        self.__aggregate_button.grid(row=4, columnspan=4, sticky=W + E, pady=(20, 0), padx=10)
        self.__ratio_labels[0].grid(row=5, column=0, sticky=W + E, padx=(10, 5))
        self.__ratio_labels[1].grid(row=5, column=1, sticky=W + E, padx=5)
        self.__ratio_labels[2].grid(row=5, column=2, sticky=W + E, padx=5)
        self.__ratio_labels[3].grid(row=5, column=3, sticky=W + E, padx=(5, 10))

    def __get_winner_text(self):
        election_winner = self.__get_election_winner()
        winning_ratio = self.__get_winning_ratio()
        return StringVar(value=self.__get_election_winner_text(election_winner, winning_ratio))

    def __get_winning_ratio(self):
        district_winners = self.__get_district_winners()
        return get_winning_ratio(district_winners)

    def __get_district_winners(self):
        coordinates = self.__get_coordinates()
        district_winners = get_district_winners(coordinates)
        return district_winners

    def __get_election_winner(self):
        district_winners = self.__get_district_winners()
        election_winner = get_election_winner(district_winners)
        return election_winner

    def __update_winner_text(self):
        election_winner = self.__get_election_winner()
        winning_ratio = self.__get_winning_ratio()
        self.__winner_text.set(self.__get_election_winner_text(election_winner, winning_ratio))

    def __create_buttons(self):
        button_font = ('Helvetica', 16)

        toggle_button_kwargs = self.__get_toggle_button_kwargs(button_font)
        self.__toggle_button = Button(self.__root, toggle_button_kwargs)

        next_button_kwargs = self.__get_next_button_kwargs(button_font)
        self.__next_button = Button(self.__root, next_button_kwargs)

        prev_button_kwargs = self.__get_prev_button_kwargs(button_font)
        self.__prev_button = Button(self.__root, prev_button_kwargs)

        aggregate_button_kwargs = self.__get_aggregate_button_kwargs(button_font)
        self.__aggregate_button = Button(self.__root, aggregate_button_kwargs)

    def __init_canvas(self):
        return Canvas(self.__root,
                      width=CANVAS_DIMENSION,
                      height=CANVAS_DIMENSION,
                      background='white')

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
        coordinates = self.__get_coordinates()
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
                self.__update_winner_text()
                self.__update_result_number_text()

    def __create_canvas(self):
        square_size = CANVAS_DIMENSION / NUM_DISTRICTS
        coordinates = self.__get_coordinates()
        contiguous_districts = get_districts_from_coordinates(coordinates)

        for i in range(NUM_DISTRICTS):
            for j in range(NUM_DISTRICTS):
                index = i * NUM_DISTRICTS + j
                district = contiguous_districts[index]
                color = self.__get_district_color(district)
                square_coordinates = self.__get_square_coordinates(i, j, square_size)
                self.__tiles[index] = self.__canvas.create_rectangle(*square_coordinates, fill=color)
                font_coordinates = self.__get_font_coordinates(i, j, square_size)
                self.__district_nums[index] = self.__canvas.create_text(*font_coordinates, text=district,
                                                                        font=('Helvetica', 28))

    def __get_coordinates(self):
        return self.__coordinate_list[self.__current_district]

    def __toggle_district_results(self):
        self.__toggle_results = False if self.__toggle_results else True
        if self.__toggle_results:
            self.__show_district_results()
        else:
            self.__hide_district_results()

    def __show_district_results(self):
        coordinates = self.__get_coordinates()
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
        coordinates = self.__get_coordinates()
        contiguous_districts = get_districts_from_coordinates(coordinates)
        for i in range(NUM_DISTRICTS):
            for j in range(NUM_DISTRICTS):
                index = i * NUM_DISTRICTS + j
                district = contiguous_districts[index]
                color = self.__get_district_color(district)
                self.__canvas.itemconfig(self.__tiles[index], fill=color)
        self.__toggle_button['text'] = 'Show District Results'

    def __get_toggle_button_kwargs(self, button_font):
        return {
            'text': 'Show District Results',
            'command': lambda: self.__toggle_district_results(),
            'font': button_font
        }

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

    def __get_aggregate_button_kwargs(self, button_font):
        return {
            'text': 'Show Aggregate Results',
            'font': button_font,
            'command': lambda: self.__toggle_aggregate_results(),
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

    @staticmethod
    def __get_pie_chart_piece_color(index):
        # Red, Blue, Green, Amber
        colors = ['#f44336', '#2196F3', '#4CAF50', '#FFC107']
        return colors[index]

    @staticmethod
    def __get_election_winner_text(election_winner, winning_ratio):
        winning_ratio_parts = winning_ratio.split(':')
        if election_winner == G:
            winning_ratio_text = winning_ratio_parts[0] + ' to ' + winning_ratio_parts[1]
        else:
            winning_ratio_text = winning_ratio_parts[1] + ' to ' + winning_ratio_parts[0]
        return 'Election Winner: ' + election_winner + ' ' + winning_ratio_text

    def __toggle_aggregate_results(self):
        self.__toggle_aggregate = False if self.__toggle_aggregate else True

        if self.__toggle_aggregate:
            self.__show_aggregate_results()
        else:
            self.__hide_aggregate_results()

    def __show_aggregate_results(self):
        self.__result_number_label.config(state=DISABLED)
        for i in range(NUM_DISTRICTS * NUM_DISTRICTS):
            self.__canvas.itemconfig(self.__tiles[i], state=HIDDEN)
            self.__canvas.itemconfig(self.__district_nums[i], state=HIDDEN)
        self.__next_button.config(state=DISABLED)
        self.__prev_button.config(state=DISABLED)
        self.__toggle_button.config(state=DISABLED)
        self.__winner_text.set("Aggregate Winning Ratios (Green : Purple)")
        self.__aggregate_button['text'] = 'Hide Aggregate Results'
        self.__create_pie_chart()
        for i in range(len(self.__ratio_labels)):
            self.__ratio_labels[i].config(state=ACTIVE)

    def __create_pie_chart(self):
        pie_chart_coordinates = (100, 100, 400, 400)
        num_contiguous = len(self.__coordinate_list)
        i = 0
        start_arc = 0
        for key in self.__winning_ratios.keys():
            percent = self.__winning_ratios[key] / num_contiguous
            pie_chart_color = self.__get_pie_chart_piece_color(i)
            extent = percent * 1000
            self.__pie_chart_pieces[i] = self.__canvas.create_arc(pie_chart_coordinates,
                                                                  fill=pie_chart_color, outline=pie_chart_color,
                                                                  start=prop(start_arc), extent=prop(extent))
            if extent + start_arc >= 1000:
                break
            start_arc = extent
            i += 1

    def __hide_aggregate_results(self):
        self.__result_number_label.config(state=NORMAL)
        for i in range(NUM_DISTRICTS * NUM_DISTRICTS):
            self.__canvas.itemconfig(self.__tiles[i], state=NORMAL)
            self.__canvas.itemconfig(self.__district_nums[i], state=NORMAL)
        self.__next_button.config(state=self.__is_next_button_enabled())
        self.__prev_button.config(state=self.__is_prev_button_enabled())
        self.__toggle_button.config(state=NORMAL)
        self.__update_winner_text()
        self.__aggregate_button['text'] = 'Show Aggregate Results'
        for i in range(len(self.__pie_chart_pieces)):
            self.__canvas.itemconfig(self.__pie_chart_pieces[i], state=HIDDEN)
            self.__ratio_labels[i].config(state=DISABLED)
