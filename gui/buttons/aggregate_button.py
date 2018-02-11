from tkinter import DISABLED
from tkinter import NORMAL
from gui.buttons.buttons import AGGREGATE_BUTTON_TEXT
from gui.buttons.buttons import create_aggregate_button
from tkinter import W
from tkinter import E


class AggregateButton:
    __toggle_aggregate = False

    def __init__(self,
                 root,
                 canvas,
                 pagination_label,
                 pagination_buttons,
                 election_winner_label,
                 update_winner_text,
                 toggle_button,
                 ratio_labels):
        self.__canvas = canvas
        self.__pagination_label = pagination_label
        self.__pagination_buttons = pagination_buttons
        self.__toggle_button = toggle_button
        self.__election_winner_label = election_winner_label
        self.__ratio_labels = ratio_labels
        self.__update_winner_text = update_winner_text
        self.__button = create_aggregate_button(root,
                                                self.__toggle_aggregate_results)

    def configure_layout(self, row, num_columns, padding):
        self.__button.grid(row=row, columnspan=num_columns, sticky=W + E, pady=(padding * 2, 0), padx=padding)

    def __toggle_aggregate_results(self):
        self.__toggle_aggregate = False if self.__toggle_aggregate else True

        if self.__toggle_aggregate:
            self.__show_aggregate_results()
        else:
            self.__hide_aggregate_results()

    def __show_aggregate_results(self):
        self.__pagination_label.config(state=DISABLED)
        self.__pagination_buttons.disable()
        self.__toggle_button.config(state=DISABLED)
        self.__election_winner_label.set_text("Aggregate Winning Ratios (Green : Purple)")
        self.__button['text'] = 'Hide ' + AGGREGATE_BUTTON_TEXT
        self.__ratio_labels.enable()
        self.__canvas.show_pie_chart()

    def __hide_aggregate_results(self):
        self.__pagination_label.config(state=NORMAL)
        self.__pagination_buttons.enable()
        self.__toggle_button.config(state=NORMAL)
        self.__update_winner_text()
        self.__button['text'] = 'Show ' + AGGREGATE_BUTTON_TEXT
        self.__ratio_labels.disable()
        self.__canvas.show_district_grid()

    def grid(self, **kwargs):
        self.__button.grid(kwargs)
