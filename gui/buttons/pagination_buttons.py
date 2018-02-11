from tkinter import DISABLED
from tkinter import NORMAL

from gui.buttons.buttons import create_next_button
from gui.buttons.buttons import create_prev_button


class PaginationButtons:
    __current_district = 0

    def __init__(self, root, pagination_label, redraw):
        self.__pagination_label = pagination_label
        self.__redraw = redraw
        self.next = create_next_button(root,
                                       self.__handle_next)
        self.prev = create_prev_button(root,
                                       self.__handle_prev)

    def enable(self):
        self.next.config(state=self.__is_next_button_enabled())
        self.prev.config(state=self.__is_prev_button_enabled())

    def disable(self):
        self.next.config(state=DISABLED)
        self.prev.config(state=DISABLED)

    def __handle_next(self):
        self.__pagination_label.next()
        self.prev.config(state=NORMAL)
        self.next.config(state=self.__is_next_button_enabled())
        self.__redraw()

    def __handle_prev(self):
        self.__pagination_label.prev()
        self.prev.config(state=self.__is_prev_button_enabled())
        self.next.config(state=self.__is_next_button_enabled())
        self.__redraw()

    def __is_prev_button_enabled(self):
        return DISABLED if self.__pagination_label.current_page == 1 else NORMAL

    def __is_next_button_enabled(self):
        return DISABLED if self.__pagination_label.is_last_page() else NORMAL
