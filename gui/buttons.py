from tkinter import DISABLED
from tkinter import Button

_BUTTON_FONT = ('Helvetica', 16)

TOGGLE_BUTTON_TEXT = 'District Results'
AGGREGATE_BUTTON_TEXT = 'Aggregate Results'


def create_prev_button(root, command):
    kwargs = __get_prev_button_kwargs(command)
    return Button(root, kwargs)


def create_next_button(root, command):
    kwargs = __get_next_button_kwargs(command)
    return Button(root, kwargs)


def create_toggle_button(root, command):
    kwargs = __get_toggle_button_kwargs(command)
    return Button(root, kwargs)


def create_aggregate_button(root, command):
    kwargs = __get_aggregate_button_kwargs(command)
    return Button(root, kwargs)


def __get_button_kwargs(text, command):
    return {
        'text': text,
        'command': lambda: command(),
        'font': _BUTTON_FONT
    }


def __get_toggle_button_kwargs(command):
    return __get_button_kwargs('Show ' + TOGGLE_BUTTON_TEXT, command)


def __get_next_button_kwargs(command):
    return __get_button_kwargs('Next', command)


def __get_prev_button_kwargs(command):
    kwargs = __get_button_kwargs('Previous', command)
    kwargs['state'] = DISABLED
    return kwargs


def __get_aggregate_button_kwargs(command):
    return __get_button_kwargs('Show ' + AGGREGATE_BUTTON_TEXT, command)
