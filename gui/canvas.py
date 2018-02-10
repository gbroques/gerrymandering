import tkinter as tk

from constants import NUM_DISTRICTS
from coordinates import get_districts_from_coordinates
from gui.colors import get_district_color

_BG_COLOR = 'white'
_DIMENSION = 500


class Canvas:
    def __init__(self, root):
        self.canvas = self.init(root)
        self.tiles = self.get_empty_tiles()
        self.district_nums = self.get_empty_tiles()

    @staticmethod
    def init(root):
        return tk.Canvas(root,
                         width=_DIMENSION,
                         height=_DIMENSION,
                         background=_BG_COLOR)

    @staticmethod
    def get_empty_tiles():
        return [None for _ in range(NUM_DISTRICTS * NUM_DISTRICTS)]

    @staticmethod
    def get_tile_size():
        return _DIMENSION / NUM_DISTRICTS

    def draw(self, coordinates):
        districts = get_districts_from_coordinates(coordinates)

        for i in range(NUM_DISTRICTS):
            for j in range(NUM_DISTRICTS):
                index = i * NUM_DISTRICTS + j
                district = districts[index]
                self.tiles[index] = self.create_tile(district, i, j)
                self.district_nums[index] = self.create_district_num(district, i, j)

    def create_tile(self, district, i, j):
        color = get_district_color(district)
        tile_coordinates = self.__get_tile_coordinates(i, j)
        return self.canvas.create_rectangle(*tile_coordinates, fill=color)

    def create_district_num(self, district, i, j):
        text_coordinates = self.__get_text_coordinates(i, j)
        text_kwargs = self.__get_text_kwargs(district)
        return self.canvas.create_text(*text_coordinates, **text_kwargs)

    @classmethod
    def __get_tile_coordinates(cls, i, j):
        tile_size = cls.get_tile_size()
        x0 = tile_size * j
        y0 = tile_size * i
        x1 = tile_size * (j + 1)
        y1 = tile_size * (i + 1)
        return x0, y0, x1, y1

    @classmethod
    def __get_text_coordinates(cls, i, j):
        tile_size = cls.get_tile_size()
        x = (tile_size * j) + tile_size / 2
        y = (tile_size * i) + tile_size / 2
        return x, y

    @staticmethod
    def __get_text_kwargs(district):
        return {
            'text': district,
            'font': ('Helvetica', 28)
        }

