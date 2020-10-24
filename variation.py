#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'Akinava'
__author_email__ = 'akinava@gmail.com'
__copyright__ = 'Copyright © 2020'
__license__ = 'MIT License'
__version__ = [0, 0]


import os
from datetime import date
from utility import (parse_help,
        read_file,
        get_option,
        angle_cast,
        course_to_number)


def print_help():
    print('run:', __file__, 'args')
    print('args: -t true_course -m magnetic_course, -v variation')
    print('example:', __file__, '-v \'5w\'')
    print('example:', __file__, '-v \'3 35E 2007 (5E)\'')
    print('example:', __file__, '-v \'./path/to/variation_file.txt\'')
    print('example of file variation_file.txt > \'3 35E 2007 (5E)\'')
    print('help: -h | print help')


def define_variation_option_type(variation_option):
    if os.path.isfile(variation_option):
        return 'file'
    if len(variation_option) > 2:
        return 'year_variation'
    return 'variation'


def parse_year_variation(variation_option):
    variation_option = variation_option.replace('\n', '').upper()
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


def parse_variation():
    variation_option = get_option('-v')
    if variation_option is None:
        return None
    variation_option_type = define_variation_option_type(variation_option)
    if variation_option_type == 'file':
        variation_option = read_file(variation_option)
        variation_option = calculate_year_variation(variation_option)

    if variation_option_type == 'year_variation':
        variation_option = calculate_year_variation(variation_option)

    return variation_option


def parse_true_course():
    true_course = get_option('-t')
    if true_course:
        return angle_cast(int(true_course))
    return true_course


def parse_magnetic_course():
    magnetic_course = get_option('-m')
    if magnetic_course:
        return angle_cast(int(magnetic_course))
    return magnetic_course


def calculate_true_course(options):
    options['true_course'] = angle_cast(options['magnetic_course'] + course_to_number(options['variation']))


def calculate_magnetic_course(options):
    options['magnetic_course'] = angle_cast(options['true_course'] - course_to_number(options['variation']))


def calculate_variation(options):
    variation = options['true_course'] - options['magnetic_course']
    options['variation'] = number_to_course(variation)


def calculate(options):
    if options['true_course'] is None:
        calculate_true_course(options)
    elif options['magnetic_course'] is None:
        calculate_magnetic_course(options)
    elif options['variation'] is None:
        calculate_variation(options)
    else:
        raise Exception('deviation task error')
    return options


def op_parse():
    parse_help(print_help)
    true_course = parse_true_course()
    magnetic_course = parse_magnetic_course()
    variation = parse_variation()
    return {'true_course': true_course, 'magnetic_course': magnetic_course, 'variation': variation}



if __name__ == '__main__':
    options = op_parse()
    result = calculate(options)
    print(result)
    exit(0) 
