from tkinter import Label
from tkinter import StringVar

from gui.labels.styles import LABEL_FONT


class PaginationLabel:
    def __init__(self, root, total_pages, start_page=1):
        self.current_page = start_page
        self.total_pages = total_pages

        text = self.__get_pagination_text()
        self.__pagination_text = StringVar(value=text)

        label_kwargs = self.__get_label_kwargs()
        self.__label = Label(root, **label_kwargs)

    def grid(self, **kwargs):
        self.__label.grid(kwargs)

    def config(self, **kwargs):
        self.__label.config(kwargs)

    def __get_pagination_text(self):
        return 'Result ' + str(self.current_page) + ' out of ' + str(self.total_pages)

    def next(self):
        self.current_page += 1
        self.__pagination_text.set(self.__get_pagination_text())

    def prev(self):
        self.current_page -= 1
        self.__pagination_text.set(self.__get_pagination_text())

    def is_last_page(self):
        return self.current_page == self.total_pages

    def __get_label_kwargs(self):
        return {
            'textvariable': self.__pagination_text,
            'font': LABEL_FONT
        }
