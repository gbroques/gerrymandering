from tkinter import DISABLED
from tkinter import Button

_BUTTON_FONT = ('Helvetica', 16)


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
    return __get_button_kwargs('Show District Results', command)


def __get_next_button_kwargs(command):
    return __get_button_kwargs('Next', command)


def __get_prev_button_kwargs(command):
    kwargs = __get_button_kwargs('Previous', command)
    kwargs['state'] = DISABLED
    return kwargs


def __get_aggregate_button_kwargs(command):
    return __get_button_kwargs('Show Aggregate Results', command)
