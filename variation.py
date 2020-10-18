#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'Akinava'
__author_email__ = 'akinava@gmail.com'
__copyright__ = 'Copyright © 2020'
__license__ = 'MIT License'
__version__ = [0, 0]


import sys
import os
from datetime import date


def print_help():
    print('run:', __file__, 'args')
    print('example:', __file__, '\'5w\'')
    print('example:', __file__, '\'3 35E 2007 (5E)\'')
    print('example:', __file__, '\'./path/to/variation_file.txt\'')
    print('example of file variation_file.txt > \'3 35E 2007 (5E)\'')
    print('help: -h | print help')


def parse_help():
    if '-h' in sys.argv:
        print_help()
        exit(0)


def read_file(file_path):
    with open(file_path) as f:
        return f.read()


def define_variation_option_type(variation_option):
    if os.path.isfile(variation_option):
        return 'file'
    if len(variation_option) > 2:
        return 'year_variation'
    return 'variation'


def parse_year_variation(variation_option):
    variation_option = variation_option.replace('\n', '')
    degrees, minutes_direction, year, year_variation_direction = variation_option.split(' ')
    minutes = minutes_direction[:-1]
    variation_direction = minutes_direction[-1:]
    year_variation_direction = year_variation_direction[1:-1]
    year_variation = year_variation_direction[:-1]
    year_variation_direction = year_variation_direction[-1:]
    return int(degrees), int(minutes), variation_direction, int(year), int(year_variation), year_variation_direction


def calculate_year_variation(variation_option):
    degrees, minutes, variation_direction, year, year_variation, year_variation_direction = parse_year_variation(variation_option)
    degrees += minutes/60

    current_delta_variation = (date.today().year - year) * year_variation / 60
    if variation_direction != year_variation_direction:
        current_delta_variation *= -1

    current_variation = degrees + current_delta_variation
    if current_variation < 0:
        current_variation *= -1
        variation_direction = year_variation_direction

    return '{}{}'.format(round(current_variation), variation_direction)


def get_variation(variation_option):
    variation_option_type = define_variation_option_type(variation_option)
    if variation_option_type == 'file':
        variation_option = read_file(variation_option)
        variation_option = calculate_year_variation(variation_option)

    if variation_option_type == 'year_variation':
        variation_option = calculate_year_variation(variation_option)

    return variation_option


if __name__ == '__main__':
    parse_help()
    variation = get_variation(sys.argv[1]) 
    print(variation)
    exit(0) 
