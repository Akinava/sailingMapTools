#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'Akinava'
__author_email__ = 'akinava@gmail.com'
__copyright__ = 'Copyright © 2020'
__license__ = 'MIT License'
__version__ = [0, 0]


import math
from utility import parse_help, get_option, coordinates_to_point, distance_between_points, calculate_course_by_points
from track_point import calculate_point, point_to_coordinates


def print_help():
    print('run:', __file__, 'args')
    print('args: -b1 bearing1, -b2 bearing2')
    print('example:', __file__, '-b1 \'71 58.07365N,24.48623E\' -b2 \'6 58.17873N,24.19983E\'')
    print('help: -h | print help')


def parse_bearing(option):
    bearing = coordinates_to_point(option.split(' ')[1])
    bearing['course'] = int(option.split(' ')[0])
    return bearing


def parse_bearing1():
    return parse_bearing(get_option('-b1'))


def parse_bearing2():
    return parse_bearing(get_option('-b2'))


def calculate(options):
    distance_bearing1_bearing2 = distance_between_points(options['bearing1'], options['bearing2'])
    bearing_course_1 = calculate_course_by_points(options['bearing1'], options['bearing2'])

    yacht_angle = abs(options['bearing1']['course'] - options['bearing2']['course'])
    bearing1_angle = bearing_course_1 % 180 - options['bearing1']['course']
    bearing2_angle = 180 - yacht_angle - bearing1_angle

    distance_yacht_bearing1 = distance_bearing1_bearing2 * math.sin(math.radians(bearing2_angle)) / math.sin(math.radians(yacht_angle))
    bearing1_true_course = 180 + options['bearing1']['course']

    options['yacht'] = calculate_point(options['bearing1'], distance_yacht_bearing1, bearing1_true_course, 'SW')
    return options


def op_parse():
    parse_help(print_help)
    bearing1 = parse_bearing1()
    bearing2 = parse_bearing2()
    return {'bearing1': bearing1, 'bearing2': bearing2}


def pprint(result):
    for key, value in result.items():
        result[key] = point_to_coordinates(value)
    print(result)


if __name__ == '__main__':
    options = op_parse()
    result = calculate(options)
    pprint(result)
    exit(0)
