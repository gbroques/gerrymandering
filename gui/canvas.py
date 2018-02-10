from tkinter import Canvas
from constants import NUM_DISTRICTS
from coordinates import get_districts_from_coordinates
from gui.colors import get_district_color

_CANVAS_DIMENSION = 500


def init_canvas(root):
    return Canvas(root,
                  width=_CANVAS_DIMENSION,
                  height=_CANVAS_DIMENSION,
                  background='white')


def create_canvas(canvas, coordinates, tiles, district_nums):
    square_size = _CANVAS_DIMENSION / NUM_DISTRICTS
    contiguous_districts = get_districts_from_coordinates(coordinates)

    for i in range(NUM_DISTRICTS):
        for j in range(NUM_DISTRICTS):
            index = i * NUM_DISTRICTS + j
            district = contiguous_districts[index]
            color = get_district_color(district)
            square_coordinates = __get_square_coordinates(i, j, square_size)
            tiles[index] = canvas.create_rectangle(*square_coordinates, fill=color)
            font_coordinates = __get_font_coordinates(i, j, square_size)
            district_nums[index] = canvas.create_text(*font_coordinates, text=district, font=('Helvetica', 28))


def __get_font_coordinates(i, j, square_size):
    x = (square_size * j) + square_size / 2
    y = (square_size * i) + square_size / 2
    return x, y


def __get_square_coordinates(i, j, square_size):
    x0 = square_size * j
    y0 = square_size * i
    x1 = square_size * (j + 1)
    y1 = square_size * (i + 1)
    return x0, y0, x1, y1
