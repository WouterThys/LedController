import os
from yaml import load, dump

PATH = os.path.join(os.path.dirname(__file__), "")
UART_SETTINGS = "UartSettings"
CIRCLE_PWM_COLORS = "CirclePwmColors"


def read_settings(which):
    with open(PATH+"settings.yml", 'r') as sets:
        sets_dict = load(sets)
        return sets_dict[which]


def write_settings(which, val):
    with open(PATH+"settings.yml", 'r') as sets:
        sets_dict = load(sets)

    sets_dict[which] = val
    with open(PATH+"settings.yml", 'w') as sets:
        dump(sets_dict, sets, default_flow_style=False)