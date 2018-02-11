from district_winners import get_election_winner
from district_winners import get_winning_ratio
from gui.buttons import DistrictResultsToggle
from gui.buttons import PaginationButtons
from gui.buttons.aggregate_button import AggregateButton
from gui.canvas import *
from gui.labels import ElectionWinnerLabel
from gui.labels import PaginationLabel
from gui.labels import WinningRatioLabels
from gui.pie_chart import get_pie_chart_percents
from gui.layout_manager import LayoutManager

# Title of GUI window
_TITLE = 'Gerrymandering'

# Disable resizing of GUI window
_RESIZEABLE = False


class App:
    def __init__(self, coordinate_list, winning_ratios):
        self.__coordinate_list = coordinate_list
        self.__winning_ratios = winning_ratios

        self.__root = self.__init_root()
        self.__pagination_label = self.__get_pagination_label()
        self.__canvas = self.__setup_canvas()
        self.__election_winner_label = self.get_election_winner_label()
        self.__ratio_labels = self.__get_winning_ratio_labels()
        self.__create_buttons()
        self.__layout_manager = self.__setup_layout_manager()

    @staticmethod
    def __init_root():
        root = tk.Tk()
        root.title(_TITLE)
        root.resizable(width=_RESIZEABLE, height=_RESIZEABLE)
        return root

    def __get_pagination_label(self):
        return PaginationLabel(self.__root, len(self.__coordinate_list))

    def __setup_canvas(self):
        canvas = Canvas(self.__root)
        canvas.create_district_grid(self.__get_coordinates())
        num_pieces_and_percents = self.__get_num_pieces_and_percents()
        canvas.create_pie_chart(*num_pieces_and_percents)
        return canvas

    def get_election_winner_label(self):
        election_winner_and_ratio = self.get_election_winner_and_ratio()
        return ElectionWinnerLabel(self.__root, *election_winner_and_ratio)

    def __create_buttons(self):
        self.__toggle_button = self.__get_toggle_button()
        self.__pagination_buttons = self.__get_pagination_buttons()
        self.__aggregate_button = self.__get_aggregate_button()

    def __get_toggle_button(self):
        return DistrictResultsToggle(self.__root,
                                     self.__canvas,
                                     self.__get_coordinates())

    def __get_pagination_buttons(self):
        return PaginationButtons(self.__root,
                                 self.__pagination_label,
                                 self.__redraw)

    def __get_aggregate_button(self):
        return AggregateButton(self.__root,
                               self.__canvas,
                               self.__pagination_label,
                               self.__pagination_buttons,
                               self.__election_winner_label,
                               self.__update_winner_text,
                               self.__toggle_button,
                               self.__ratio_labels)

    def __get_winning_ratio_labels(self):
        return WinningRatioLabels(self.__root, list(self.__winning_ratios.keys()))

    def __setup_layout_manager(self):
        layout_manager = self.__get_layout_manager()
        num_columns = len(self.__winning_ratios.keys())
        layout_manager.configure(num_columns)
        return layout_manager

    def __get_layout_manager(self):
        return LayoutManager(self.__root,
                             self.__pagination_label,
                             self.__canvas,
                             self.__election_winner_label,
                             self.__pagination_buttons,
                             self.__toggle_button,
                             self.__aggregate_button,
                             self.__ratio_labels)

    def __get_num_pieces_and_percents(self):
        num_pieces = len(self.__winning_ratios.keys())
        percents = get_pie_chart_percents(self.__winning_ratios, len(self.__coordinate_list))
        return num_pieces, percents

    def get_election_winner_and_ratio(self):
        election_winner = self.__get_election_winner()
        winning_ratio = self.__get_winning_ratio()
        return election_winner, winning_ratio

    def run_mainloop(self):
        self.__root.mainloop()

    def __get_winning_ratio(self):
        district_winners = self.__get_district_winners()
        return get_winning_ratio(district_winners)

    def __get_election_winner(self):
        district_winners = self.__get_district_winners()
        return get_election_winner(district_winners)

    def __get_district_winners(self):
        coordinates = self.__get_coordinates()
        district_winners = get_district_winners(coordinates)
        return district_winners

    def __update_winner_text(self):
        election_winner_and_ratio = self.get_election_winner_and_ratio()
        self.__election_winner_label.set_election_winner(*election_winner_and_ratio)

    def __redraw(self):
        coordinates = self.__get_coordinates()
        self.__canvas.draw_district_grid(coordinates)
        self.__toggle_button.reset(coordinates)
        self.__update_winner_text()

    def __get_coordinates(self):
        """Convenience method to get the current list of coordinates.

        Based on current page stored in pagination label,
        updated when user clicks next and previous buttons.
        """
        return self.__coordinate_list[self.__pagination_label.current_page - 1]
