from coordinates import get_district_winners
from district_winners import get_election_winner
from district_winners import get_winning_ratio
from gui.buttons import AGGREGATE_BUTTON_TEXT
from gui.buttons import DistrictResultsToggle
from gui.buttons import PaginationButtons
from gui.buttons import create_aggregate_button
from gui.canvas import *
from gui.colors import *
from gui.labels import ElectionWinnerLabel
from gui.labels import PaginationLabel
from gui.labels import WinningRatioLabels
from gui.pie_chart import get_pie_chart_percents

# Title of GUI window
_TITLE = 'Gerrymandering'

# Disable resizing of GUI window
_RESIZEABLE = False


class App:
    __toggle_aggregate = False

    def __init__(self, coordinate_list, winning_ratios):
        self.__coordinate_list = coordinate_list
        self.__winning_ratios = winning_ratios
        self.__root = self.__init_root()
        self.__ratio_labels = WinningRatioLabels(self.__root, list(winning_ratios.keys()))
        self.__canvas = Canvas(self.__root)
        self.__pagination_label = PaginationLabel(self.__root, len(coordinate_list))
        self.__canvas.draw_district_grid(self.__get_coordinates())

        num_winning_ratios = len(winning_ratios.keys())
        percents = get_pie_chart_percents(self.__winning_ratios, len(coordinate_list))
        self.__canvas.draw_pie_chart(num_winning_ratios, percents)

        election_winner_and_ratio = self.get_election_winner_and_ratio()
        self.__election_winner_label = ElectionWinnerLabel(self.__root, *election_winner_and_ratio)

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
        root.title(_TITLE)
        root.resizable(width=_RESIZEABLE, height=_RESIZEABLE)
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
        self.__pagination_buttons.prev.grid(row=3, column=0, sticky=tk.W + tk.E, padx=padding)
        self.__toggle_button.grid(row=3, column=1, columnspan=2, sticky=tk.W + tk.E)
        self.__pagination_buttons.next.grid(row=3, column=3, sticky=tk.W + tk.E, padx=padding)

        # Layout fifth row
        self.__aggregate_button.grid(row=4, columnspan=num_columns, sticky=tk.W + tk.E, pady=(padding * 2, 0),
                                     padx=padding)

        # Layout sixth row
        self.__ratio_labels.configure_layout(5, padding)

    def __configure_columns(self, num_columns):
        """Configure columns to have equal weights.

        Add uniform group to make columns equal widths.
        """
        group = 'group'
        for i in range(num_columns):
            self.__root.columnconfigure(i, weight=1, uniform=group)

    def __configure_rows(self):
        row_padding = 40
        for row in self.__rows_with_padding():
            self.__root.rowconfigure(row, pad=row_padding)

    @staticmethod
    def __rows_with_padding():
        return [0, 2, 5]

    def __create_buttons(self):
        self.__toggle_button = DistrictResultsToggle(self.__root,
                                                     self.__canvas,
                                                     self.__get_coordinates())
        self.__pagination_buttons = PaginationButtons(self.__root,
                                                      self.__pagination_label,
                                                      self.__redraw)
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
        return self.__coordinate_list[self.__pagination_label.current_page - 1]

    def __toggle_aggregate_results(self):
        self.__toggle_aggregate = False if self.__toggle_aggregate else True

        if self.__toggle_aggregate:
            self.__show_aggregate_results()
        else:
            self.__hide_aggregate_results()

    def __show_aggregate_results(self):
        self.__pagination_label.config(state=tk.DISABLED)
        self.__canvas.hide_district_grid()
        self.__pagination_buttons.disable()
        self.__toggle_button.config(state=tk.DISABLED)
        self.__election_winner_label.set_text("Aggregate Winning Ratios (Green : Purple)")
        self.__aggregate_button['text'] = 'Hide ' + AGGREGATE_BUTTON_TEXT
        self.__ratio_labels.enable()
        self.__canvas.show_pie_chart()

    def __hide_aggregate_results(self):
        self.__pagination_label.config(state=tk.NORMAL)
        self.__canvas.show_district_grid()
        self.__pagination_buttons.enable()
        self.__toggle_button.config(state=tk.NORMAL)
        self.__update_winner_text()
        self.__aggregate_button['text'] = 'Show ' + AGGREGATE_BUTTON_TEXT
        self.__ratio_labels.disable()
        self.__canvas.hide_pie_chart()
