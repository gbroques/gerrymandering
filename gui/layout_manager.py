from tkinter import W
from tkinter import E


class LayoutManager:
    def __init__(self,
                 root,
                 pagination_label,
                 canvas,
                 election_winner_label,
                 pagination_buttons,
                 toggle_button,
                 aggregate_button,
                 ratio_labels):
        self.__root = root
        self.__pagination_label = pagination_label
        self.__canvas = canvas
        self.__election_winner_label = election_winner_label
        self.__pagination_buttons = pagination_buttons
        self.__toggle_button = toggle_button
        self.__aggregate_button = aggregate_button
        self.__ratio_labels = ratio_labels

    def configure(self, num_columns):
        self.__configure_columns(num_columns)
        self.__configure_rows()

        column_padding = 10

        # Layout first row
        self.__pagination_label.grid(row=0, columnspan=num_columns)

        # Layout second row
        self.__canvas.instance.grid(row=1, columnspan=num_columns, padx=column_padding)

        # Layout third row
        self.__election_winner_label.grid(row=2, columnspan=num_columns, sticky=W + E)

        # Layout fourth row
        self.__pagination_buttons.prev.grid(row=3, column=0, sticky=W + E, padx=column_padding)
        self.__toggle_button.grid(row=3, column=1, columnspan=2, sticky=W + E)
        self.__pagination_buttons.next.grid(row=3, column=3, sticky=W + E, padx=column_padding)

        # Layout fifth row
        self.__aggregate_button.configure_layout(4, num_columns, column_padding)

        # Layout sixth row
        self.__ratio_labels.configure_layout(5, column_padding)

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
