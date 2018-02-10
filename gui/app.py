import tkinter as tk

from constants import G
from coordinates import get_district_winners
from district_winners import get_election_winner
from district_winners import get_winning_ratio
from gui.buttons import *
from gui.canvas import *
from gui.colors import *
from gui.pie_chart import PieChart
from gui.pie_chart import get_pie_chart_percents

TITLE = 'Gerrymandering'


class App:
    __winning_ratios = {}
    __current_district = 0
    __result_number_text = None
    __result_number_label = None
    __winner_text = None
    __toggle_results = False
    __toggle_aggregate = False
    __pie_chart_pieces = None
    __ratio_labels = None

    def __init__(self, coordinate_list, winning_ratios):
        self.__coordinate_list = coordinate_list
        self.__winning_ratios = winning_ratios
        self.__ratio_labels = [None for _ in range(len(winning_ratios.keys()))]
        self.__root = self.__init_root()
        self.__canvas = Canvas(self.__root)
        self.__pie_chart = PieChart(len(winning_ratios.keys()))

        self.__canvas.draw(self.__get_coordinates())

        label_font = ('Helvetica', 16)

        self.__winner_text = self.__get_winner_text()
        winner_label = tk.Label(self.__root, textvariable=self.__winner_text, font=label_font)

        result_number_text = self.__get_result_number_text()
        self.__result_number_text = tk.StringVar(value=result_number_text)
        self.__result_number_label = tk.Label(self.__root, textvariable=self.__result_number_text, font=label_font)

        self.__create_buttons()

        self.create_winning_ratio_labels(label_font, winning_ratios)

        self.__init_grid_layout(winner_label)

    def create_winning_ratio_labels(self, label_font, winning_ratios):
        i = 0
        for key in winning_ratios.keys():
            self.__ratio_labels[i] = tk.Label(self.__root,
                                              text=key,
                                              font=label_font,
                                              activebackground=get_pie_chart_piece_color(i),
                                              state=tk.DISABLED)
            i += 1

    def __get_result_number_text(self):
        num_results = len(self.__coordinate_list)
        return 'Result ' + str((self.__current_district + 1)) + ' out of ' + str(num_results)

    def __update_result_number_text(self):
        self.__result_number_text.set(self.__get_result_number_text())

    def run_mainloop(self):
        self.__root.mainloop()

    @staticmethod
    def __init_root():
        root = tk.Tk()
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
        self.__canvas.canvas.grid(row=1, columnspan=4, padx=10)
        winner_label.grid(row=2, columnspan=4, sticky=tk.W + tk.E)
        self.__prev_button.grid(row=3, column=0, sticky=tk.W + tk.E, padx=10)
        self.__toggle_button.grid(row=3, column=1, columnspan=2, sticky=tk.W + tk.E)
        self.__next_button.grid(row=3, column=3, sticky=tk.W + tk.E, padx=10)
        self.__aggregate_button.grid(row=4, columnspan=4, sticky=tk.W + tk.E, pady=(20, 0), padx=10)
        self.__ratio_labels[0].grid(row=5, column=0, sticky=tk.W + tk.E, padx=(10, 5))
        self.__ratio_labels[1].grid(row=5, column=1, sticky=tk.W + tk.E, padx=5)
        self.__ratio_labels[2].grid(row=5, column=2, sticky=tk.W + tk.E, padx=5)
        self.__ratio_labels[3].grid(row=5, column=3, sticky=tk.W + tk.E, padx=(5, 10))

    def __get_winner_text(self):
        election_winner = self.__get_election_winner()
        winning_ratio = self.__get_winning_ratio()
        return tk.StringVar(value=self.__get_election_winner_text(election_winner, winning_ratio))

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

    def __handle_next(self):
        self.__current_district += 1
        self.__prev_button.config(state=tk.NORMAL)
        self.__next_button.config(state=self.__is_next_button_enabled())
        self.__redraw()

    def __handle_prev(self):
        self.__current_district -= 1
        self.__prev_button.config(state=self.__is_prev_button_enabled())
        self.__next_button.config(state=self.__is_next_button_enabled())
        self.__redraw()

    def __is_prev_button_enabled(self):
        return DISABLED if self.__current_district == 0 else tk.NORMAL

    def __is_next_button_enabled(self):
        num_coordinates = len(self.__coordinate_list)
        return DISABLED if self.__current_district == (num_coordinates - 1) else tk.NORMAL

    def __redraw(self):
        coordinates = self.__get_coordinates()
        districts = get_districts_from_coordinates(coordinates)
        for i in range(NUM_DISTRICTS):
            for j in range(NUM_DISTRICTS):
                index = i * NUM_DISTRICTS + j
                district = districts[index]
                color = get_district_color(district)
                self.__canvas.canvas.itemconfig(self.__canvas.tiles[index], fill=color)
                self.__canvas.canvas.itemconfig(self.__canvas.district_nums[index], text=district)
                self.__toggle_results = False
                self.__toggle_button['text'] = 'Show District Results'
                self.__update_winner_text()
                self.__update_result_number_text()

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

                self.__canvas.canvas.itemconfig(self.__canvas.tiles[index], fill=fill)
        self.__toggle_button['text'] = 'Hide District Results'

    def __hide_district_results(self):
        coordinates = self.__get_coordinates()
        contiguous_districts = get_districts_from_coordinates(coordinates)
        for i in range(NUM_DISTRICTS):
            for j in range(NUM_DISTRICTS):
                index = i * NUM_DISTRICTS + j
                district = contiguous_districts[index]
                color = get_district_color(district)
                self.__canvas.canvas.itemconfig(self.__canvas.tiles[index], fill=color)
        self.__toggle_button['text'] = 'Show District Results'

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
            self.__canvas.canvas.itemconfig(self.__canvas.tiles[i], state=tk.HIDDEN)
            self.__canvas.canvas.itemconfig(self.__canvas.district_nums[i], state=tk.HIDDEN)
        self.__next_button.config(state=DISABLED)
        self.__prev_button.config(state=DISABLED)
        self.__toggle_button.config(state=DISABLED)
        self.__winner_text.set("Aggregate Winning Ratios (Green : Purple)")
        self.__aggregate_button['text'] = 'Hide Aggregate Results'
        percents = get_pie_chart_percents(self.__winning_ratios, len(self.__coordinate_list))
        self.__pie_chart.draw(self.__canvas.canvas, percents)
        for i in range(len(self.__ratio_labels)):
            self.__ratio_labels[i].config(state=tk.ACTIVE)

    def __hide_aggregate_results(self):
        self.__result_number_label.config(state=tk.NORMAL)
        for i in range(NUM_DISTRICTS * NUM_DISTRICTS):
            self.__canvas.canvas.itemconfig(self.__canvas.tiles[i], state=tk.NORMAL)
            self.__canvas.canvas.itemconfig(self.__canvas.district_nums[i], state=tk.NORMAL)
        self.__next_button.config(state=self.__is_next_button_enabled())
        self.__prev_button.config(state=self.__is_prev_button_enabled())
        self.__toggle_button.config(state=tk.NORMAL)
        self.__update_winner_text()
        self.__aggregate_button['text'] = 'Show Aggregate Results'
        for i in range(self.__pie_chart.num_pieces):
            self.__canvas.canvas.itemconfig(self.__pie_chart.pieces[i], state=tk.HIDDEN)
            self.__ratio_labels[i].config(state=tk.DISABLED)

    def __create_buttons(self):
        self.__toggle_button = create_toggle_button(self.__root,
                                                    self.__toggle_district_results)
        self.__next_button = create_next_button(self.__root,
                                                self.__handle_next)
        self.__prev_button = create_prev_button(self.__root,
                                                self.__handle_prev)
        self.__aggregate_button = create_aggregate_button(self.__root,
                                                          self.__toggle_aggregate_results)

