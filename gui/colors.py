RED = '#f44336'
PURPLE = '#9C27B0'
BLUE = '#2196F3'
GREEN = '#4CAF50'
AMBER = '#FFC107'


def get_district_color(district):
    colors = [RED, PURPLE, BLUE, GREEN, AMBER]
    return colors[district - 1]


def get_pie_chart_piece_color(piece):
    colors = [RED, BLUE, GREEN, AMBER]
    return colors[piece]
