import tkinter as tk

from constants import NUM_DISTRICTS
from coordinates import get_districts_from_coordinates
from gui.colors import get_district_color
from gui.pie_chart import PieChart
from gui.colors import CANVAS_BG_COLOR
from coordinates import get_district_winners
from constants import G
from gui.colors import DISTRICT_RESULTS_GREEN
from gui.colors import DISTRICT_RESULTS_PURPLE

_DIMENSION = 500


class Canvas:
    def __init__(self, root):
        self.instance = self.__init(root)
        self.tiles = self.__get_empty_tiles()
        self.district_nums = self.__get_empty_tiles()
        self.pie_chart = None

    @staticmethod
    def __init(root):
        return tk.Canvas(root,
                         width=_DIMENSION,
                         height=_DIMENSION,
                         background=CANVAS_BG_COLOR)

    def itemconfig(self, tag_or_id, **kwargs):
        self.instance.itemconfig(tag_or_id, kwargs)

    def create_district_grid(self, coordinates):
        districts = get_districts_from_coordinates(coordinates)

        for i in range(NUM_DISTRICTS):
            for j in range(NUM_DISTRICTS):
                index = i * NUM_DISTRICTS + j
                district = districts[index]
                self.tiles[index] = self.__create_tile(district, i, j)
                self.district_nums[index] = self.__create_district_num(district, i, j)

    def draw_district_grid(self, coordinates):
        districts = get_districts_from_coordinates(coordinates)

        for i in range(len(districts)):
            district = districts[i]
            color = get_district_color(district)
            self.instance.itemconfig(self.tiles[i], fill=color)
            self.instance.itemconfig(self.district_nums[i], text=district)

    def color_district_grid_by_winner(self, coordinates):
        districts = get_districts_from_coordinates(coordinates)
        winners = get_district_winners(coordinates)
        for i in range(len(districts)):
            winner = winners[districts[i]]
            fill = DISTRICT_RESULTS_GREEN if winner == G else DISTRICT_RESULTS_PURPLE
            self.instance.itemconfig(self.tiles[i], fill=fill)

    def color_district_grid_by_district(self, coordinates):
        districts = get_districts_from_coordinates(coordinates)
        for i in range(len(districts)):
            district = districts[i]
            fill = get_district_color(district)
            self.instance.itemconfig(self.tiles[i], fill=fill)

    def create_pie_chart(self, num_pieces, percents):
        self.pie_chart = PieChart(num_pieces)
        self.pie_chart.create(self.instance, percents)

    def show_pie_chart(self):
        self.__hide_district_grid()
        self.__set_pie_chart_visibility(True)

    def __hide_pie_chart(self):
        self.__set_pie_chart_visibility(False)

    def __set_pie_chart_visibility(self, visible):
        state = self.get_visible_state(visible)
        for i in range(self.pie_chart.num_pieces):
            self.instance.itemconfig(self.pie_chart.pieces[i], state=state)

    def show_district_grid(self):
        self.__hide_pie_chart()
        self.__set_district_grid_visibility(True)

    def __hide_district_grid(self):
        self.__set_district_grid_visibility(False)

    def __set_district_grid_visibility(self, visible):
        state = self.get_visible_state(visible)
        for i in range(NUM_DISTRICTS * NUM_DISTRICTS):
            self.instance.itemconfig(self.tiles[i], state=state)
            self.instance.itemconfig(self.district_nums[i], state=state)

    def __create_tile(self, district, i, j):
        color = get_district_color(district)
        tile_coordinates = self.__get_tile_coordinates(i, j)
        return self.instance.create_rectangle(*tile_coordinates, fill=color)

    def __create_district_num(self, district, i, j):
        text_coordinates = self.__get_text_coordinates(i, j)
        text_kwargs = self.__get_text_kwargs(district)
        return self.instance.create_text(*text_coordinates, **text_kwargs)

    @classmethod
    def __get_tile_coordinates(cls, i, j):
        tile_size = cls.__get_tile_size()
        x0 = tile_size * j
        y0 = tile_size * i
        x1 = tile_size * (j + 1)
        y1 = tile_size * (i + 1)
        return x0, y0, x1, y1

    @classmethod
    def __get_text_coordinates(cls, i, j):
        tile_size = cls.__get_tile_size()
        x = (tile_size * j) + tile_size / 2
        y = (tile_size * i) + tile_size / 2
        return x, y

    @staticmethod
    def __get_text_kwargs(district):
        return {
            'text': district,
            'font': ('Helvetica', 28)
        }

    @staticmethod
    def __get_empty_tiles():
        return [None for _ in range(NUM_DISTRICTS * NUM_DISTRICTS)]

    @staticmethod
    def __get_tile_size():
        return _DIMENSION / NUM_DISTRICTS

    @staticmethod
    def get_visible_state(visible):
        return tk.NORMAL if visible else tk.HIDDEN
