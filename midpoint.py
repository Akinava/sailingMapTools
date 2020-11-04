#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'Akinava'
__author_email__ = 'akinava@gmail.com'
__copyright__ = 'Copyright © 2020'
__license__ = 'MIT License'
__version__ = [0, 0]


import json
import sys
from utility import parse_help, coordinates_to_point, distance_between_points, calculate_course_by_points


def print_help():
    print('run:', __file__, 'args')
    #                               HS                   HK
    print('example:', __file__, '\'["58 07.8N,24 48.1E", "58 10.8N,25 04.6E", "58 12.4N,24 12.5E"]\'')
    print('help: -h | print help')


def op_parse():
    parse_help(print_help)
    args = json.loads(sys.argv[1])
    result = {}
    for p in range(len(args)):
        result[p] = args[p]
    return result


def order_points_by_latitude(options):
    latitudes = []
    lat_point = {}
    result = {}

    for k, v in options.items():
        lat_point[v['latitude']['value']] = v
        latitudes.append(v['latitude']['value'])
    latitudes.sort(reverse = True)

    for p in range(len(latitudes)):
        var = lat_point[latitudes[p]]
        result[p] = var

    return result


def calculate(options):
    for p in range(3):
        options[p] = coordinates_to_point(options[p])
    options = order_points_by_latitude(options)

    distance_0_1 = distance_between_points(options[0], options[1])
    course_0 = calculate_course_by_points(options[0], options[1])
    print(options)
    print(distance_0_1, course_0)


if __name__ == '__main__':
    options = op_parse()
    result = calculate(options)
    print(result)
    exit(0)