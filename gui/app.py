from coordinates import get_district_winners
from district_winners import get_election_winner
from district_winners import get_winning_ratio
from gui.buttons import *
from gui.canvas import *
from gui.colors import *
from gui.district_results_toggle import DistrictResultsToggle
from gui.labels import ElectionWinnerLabel
from gui.labels import PaginationLabel
from gui.labels import WinningRatioLabels
from gui.pie_chart import PieChart
from gui.pie_chart import get_pie_chart_percents

TITLE = 'Gerrymandering'


class App:
    __current_district = 0
    __toggle_aggregate = False

    def __init__(self, coordinate_list, winning_ratios):
        self.__coordinate_list = coordinate_list
        self.__winning_ratios = winning_ratios
        self.__root = self.__init_root()
        self.__ratio_labels = WinningRatioLabels(self.__root, list(winning_ratios.keys()))
        self.__canvas = Canvas(self.__root)
        self.__canvas.draw(self.__get_coordinates())

        num_winning_ratios = len(winning_ratios.keys())
        self.__pie_chart = PieChart(num_winning_ratios)
        percents = get_pie_chart_percents(self.__winning_ratios, len(coordinate_list))
        self.__pie_chart.draw(self.__canvas.instance, percents)

        election_winner_and_ratio = self.get_election_winner_and_ratio()
        self.__election_winner_label = ElectionWinnerLabel(self.__root, *election_winner_and_ratio)

        self.__pagination_label = PaginationLabel(self.__root, len(coordinate_list))

        self.__create_buttons()

        self.__layout_grid(num_winning_ratios)

    def get_election_winner_and_ratio(self):
        election_winner = self.__get_election_winner()
        winning_ratio = self.__get_winning_ratio()
        return election_winner, winning_ratio

    def run_mainloop(self):
        self.__root.mainloop()

    @staticmethod
    def __init_root():
        root = tk.Tk()
        root.title(TITLE)
        root.resizable(width=False, height=False)
        return root

    def __layout_grid(self, num_columns):
        self.__configure_columns(num_columns)
        self.__configure_rows()

        padding = 10

        # Layout first row
        self.__pagination_label.grid(row=0, columnspan=num_columns)

        # Layout second row
        self.__canvas.instance.grid(row=1, columnspan=num_columns, padx=padding)

        # Layout third row
        self.__election_winner_label.grid(row=2, columnspan=num_columns, sticky=tk.W + tk.E)

        # Layout fourth row
        self.__prev_button.grid(row=3, column=0, sticky=tk.W + tk.E, padx=padding)
        self.__toggle_button.grid(row=3, column=1, columnspan=2, sticky=tk.W + tk.E)
        self.__next_button.grid(row=3, column=3, sticky=tk.W + tk.E, padx=padding)

        # Layout fifth row
        self.__aggregate_button.grid(row=4, columnspan=num_columns, sticky=tk.W + tk.E, pady=(padding * 2, 0),
                                     padx=padding)

        # Layout sixth row
        self.__ratio_labels[0].grid(row=5, column=0, sticky=tk.W + tk.E, padx=(padding, padding / 2))
        self.__ratio_labels[1].grid(row=5, column=1, sticky=tk.W + tk.E, padx=padding / 2)
        self.__ratio_labels[2].grid(row=5, column=2, sticky=tk.W + tk.E, padx=padding / 2)
        self.__ratio_labels[3].grid(row=5, column=3, sticky=tk.W + tk.E, padx=(padding / 2, padding))

    def __configure_columns(self, num_columns):
        """Configure columns to have equal weights.

        Add uniform group to make columns equal widths.
        """
        group = 'group'
        for i in range(num_columns):
            self.__root.columnconfigure(i, weight=1, uniform=group)

    def __configure_rows(self):
        row_padding = 40
        self.__root.rowconfigure(0, pad=row_padding)
        self.__root.rowconfigure(2, pad=row_padding)
        self.__root.rowconfigure(5, pad=row_padding)

    def __create_buttons(self):
        self.__toggle_button = DistrictResultsToggle(self.__root,
                                                     self.__canvas,
                                                     self.__get_coordinates())
        self.__next_button = create_next_button(self.__root,
                                                self.__handle_next)
        self.__prev_button = create_prev_button(self.__root,
                                                self.__handle_prev)
        self.__aggregate_button = create_aggregate_button(self.__root,
                                                          self.__toggle_aggregate_results)

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
        election_winner_and_ratio = self.get_election_winner_and_ratio()
        self.__election_winner_label.set_election_winner(*election_winner_and_ratio)

    def __handle_next(self):
        self.__current_district += 1
        self.__prev_button.config(state=tk.NORMAL)
        self.__next_button.config(state=self.__is_next_button_enabled())
        self.__redraw()
        self.__pagination_label.next()

    def __handle_prev(self):
        self.__current_district -= 1
        self.__prev_button.config(state=self.__is_prev_button_enabled())
        self.__next_button.config(state=self.__is_next_button_enabled())
        self.__redraw()
        self.__pagination_label.prev()

    def __is_prev_button_enabled(self):
        return DISABLED if self.__current_district == 0 else tk.NORMAL

    def __is_next_button_enabled(self):
        num_coordinates = len(self.__coordinate_list)
        return DISABLED if self.__current_district == (num_coordinates - 1) else tk.NORMAL

    def __redraw(self):
        coordinates = self.__get_coordinates()
        districts = get_districts_from_coordinates(coordinates)
        for i in range(len(districts)):
            district = districts[i]
            color = get_district_color(district)
            self.__canvas.itemconfig(self.__canvas.tiles[i], fill=color)
            self.__canvas.itemconfig(self.__canvas.district_nums[i], text=district)
            self.__toggle_button.reset()
            self.__toggle_button.set_coordinates(coordinates)
            self.__update_winner_text()

    def __get_coordinates(self):
        """Convenience method for getting the current list of coordinates."""
        return self.__coordinate_list[self.__current_district]

    def __toggle_aggregate_results(self):
        self.__toggle_aggregate = False if self.__toggle_aggregate else True

        if self.__toggle_aggregate:
            self.__show_aggregate_results()
        else:
            self.__hide_aggregate_results()

    def __show_aggregate_results(self):
        self.__pagination_label.config(state=tk.DISABLED)
        self.__canvas.hide_district_grid()
        self.__next_button.config(state=tk.DISABLED)
        self.__prev_button.config(state=tk.DISABLED)
        self.__toggle_button.config(state=tk.DISABLED)
        self.__election_winner_label.set_text("Aggregate Winning Ratios (Green : Purple)")
        self.__aggregate_button['text'] = 'Hide ' + AGGREGATE_BUTTON_TEXT
        for i in range(self.__pie_chart.num_pieces):
            self.__canvas.itemconfig(self.__pie_chart.pieces[i], state=tk.NORMAL)
            self.__ratio_labels[i].config(state=tk.ACTIVE)

    def __hide_aggregate_results(self):
        self.__pagination_label.config(state=tk.NORMAL)
        self.__canvas.show_district_grid()
        self.__next_button.config(state=self.__is_next_button_enabled())
        self.__prev_button.config(state=self.__is_prev_button_enabled())
        self.__toggle_button.config(state=tk.NORMAL)
        self.__update_winner_text()
        self.__aggregate_button['text'] = 'Show ' + AGGREGATE_BUTTON_TEXT
        for i in range(self.__pie_chart.num_pieces):
            self.__canvas.itemconfig(self.__pie_chart.pieces[i], state=tk.HIDDEN)
            self.__ratio_labels[i].config(state=tk.DISABLED)
