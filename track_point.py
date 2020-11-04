#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'Akinava'
__author_email__ = 'akinava@gmail.com'
__copyright__ = 'Copyright © 2020'
__license__ = 'MIT License'
__version__ = [0, 0]


import math
from utility import parse_help, get_option, angle_cast, coordinates_to_point, empty_point, distance_between_points, nmiles_to_longitude, calculate_course_by_points


def print_help():
    print('run:', __file__, 'args')
    print('args: -b beginning_point, -f finishing_point, -t true_course -d distance')
    print('example:', __file__, '-b \'58.07365N,24 27.8E\' -t \'189\' -d \'15.5\'')
    print('example:', __file__, '-b \'58 22.1N,24 27.8E\' -f \'58 07N,24 23E\'')
    print('help: -h | print help')


def parse_true_course():
    true_course = get_option('-t')
    if true_course:
        return angle_cast(int(true_course))
    return true_course


def parse_distance():
    return get_option('-d')


def get_distance(distance):
    if distance:
        return float(distance)
    return distance


def point_to_coordinates(point):
    coordinates = []
    for x in ['latitude', 'longitude']:
        value = round(point[x]['value'], 1)
        degree, minute = divmod(value, 60)
        coordinates.append('{:02} {:04.1f}{}'.format(int(degree), minute, point[x]['directions']))
    return ','.join(coordinates)


def get_coordinates(coordinates):
    if coordinates:
        return coordinates_to_point(coordinates)
    return coordinates


def parse_beginning_point():
    return get_option('-b')


def parse_finishing_point():
    return get_option('-f')


def op_parse():
    parse_help(print_help)
    true_course = parse_true_course()
    distance = parse_distance()
    beginning_point = parse_beginning_point()
    finishing_point = parse_finishing_point()
    return {'true_course': true_course, 'distance': distance, 'beginning_point': beginning_point, 'finishing_point': finishing_point}


def calculate_point(p1, distance, true_course):
    p2 = empty_point()
    latitude_delta = distance * math.cos(math.radians(true_course))
    p2['latitude']['value'] = p1['latitude']['value'] - latitude_delta
    p2['latitude']['directions'] = p1['latitude']['directions']

    longitude_delta_nm = distance * math.sin(math.radians(true_course))
    longitude_delta = nmiles_to_longitude(p1['latitude']['value'], longitude_delta_nm)
    p2['longitude']['value'] = p1['longitude']['value'] - longitude_delta
    p2['longitude']['directions'] = p1['longitude']['directions']
    return p2


def calculate_finishing_point(options):
    true_course_to_start_point = angle_cast(180+options['true_course'])
    options['distance'] = get_distance(options['distance'])
    options['beginning_point'] = get_coordinates(options['beginning_point'])
    options['finishing_point'] = calculate_point(options['beginning_point'], options['distance'], true_course_to_start_point)
    return


def calculate_beginning_point(options):
    options['distance'] = get_distance(options['distance'])
    options['finishing_point'] = get_coordinates(options['finishing_point'])
    options['beginning_point'] = calculate_point(options['finishing_point'], options['distance'], options['true_course'])
    return


def calculate_distance(options):
    options['beginning_point'] = get_coordinates(options['beginning_point'])
    options['finishing_point'] = get_coordinates(options['finishing_point'])
    options['distance'] = distance_between_points(options['beginning_point'], options['finishing_point'])


def calculate_true_course(options):
    options['beginning_point'] = get_coordinates(options['beginning_point'])
    options['finishing_point'] = get_coordinates(options['finishing_point'])
    options['true_course'] = calculate_course_by_points(options['beginning_point'], options['finishing_point'])


def calculate(options):
    if not options['true_course'] is None and not options['distance'] is None and not options['beginning_point'] is None and options['finishing_point'] is None:
        calculate_finishing_point(options)
    if not options['true_course'] is None and not options['distance'] is None and options['beginning_point'] is None and not options['finishing_point'] is None:
        calculate_beginning_point(options)
    if options['distance'] is None and not options['beginning_point'] is None and not options['finishing_point'] is None:
        calculate_distance(options)
    if options['true_course'] is None and not options['distance'] is None and not options['beginning_point'] is None and not options['finishing_point'] is None:
        calculate_true_course(options)
    return options


def pprint(result):
    if result['beginning_point']:
        result['beginning_point'] = point_to_coordinates(result['beginning_point'])
    if result['finishing_point']:
        result['finishing_point'] = point_to_coordinates(result['finishing_point'])
    return result


if __name__ == '__main__':
    options = op_parse()
    result = calculate(options)
    print(pprint(result))
    exit(0) 
