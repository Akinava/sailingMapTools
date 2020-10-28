#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'Akinava'
__author_email__ = 'akinava@gmail.com'
__copyright__ = 'Copyright © 2020'
__license__ = 'MIT License'
__version__ = [0, 0]


import math
from utility import parse_help, get_option, angle_cast


def print_help():
    print('run:', __file__, 'args')
    print('args: -b beginning_point, -f finishing_point, -c true_course -d distance')
    print('example:', __file__, '-b \'58.07365N,24 27.8E\' -c \'189\' -d \'15.5\'')
    print('example:', __file__, '-c \'189\' -b \'58 22.1N,24 27.8E\' -f \'58 07N,24 23E\'')
    print('help: -h | print help')


def parse_true_course():
    true_course = get_option('-t')
    if true_course:
        return angle_cast(int(true_course))
    return true_course


def parse_distance():
    distance = get_option('-d')
    if distance:
        return float(distance)
    return distance


def coordinate_to_number(coordinate):
    if ' ' in coordinate:
        degree, rest = coordinate.split(' ')
        minute = rest[:-1]
        directions = rest[-1]
        number = int(degree) * 60 + float(minute)
    else:
        degree = float(coordinate[0:-1])
        directions = coordinate[-1]
    return number, directions


def nmiles_to_longitude(latitude_minutes, nmiles):
    longitude_degrees = latitude_minutes / 60
    return nmiles / math.cos(math.radians(longitude_degrees))


def empty_point():
    #                             0-90                N/S                           0-180               E/W
    return {'latitude': {'value': None, 'directions': None}, 'longitude': {'value': None, 'directions': None}}


def coordinates_to_point(coordinates):
    point = empty_point()
    latitude, longitude = coordinates.upper().split(',')
    point['latitude']['value'], point['latitude']['directions'] = coordinate_to_number(latitude)
    point['longitude']['value'], point['longitude']['directions'] = coordinate_to_number(longitude)
    return point


def point_to_coordinates(point):
    coordinates = {}
    for x in ['latitude', 'longitude']:
        degree, minute = divmod(point[x]['value'], 60)
        coordinates[x] = '{:02} {:04.1f}{}'.format(int(degree), round(minute, 1), point[x]['directions'])
    return coordinates


def parse_beginning_point():
    beginning_point = get_option('-b')
    if beginning_point:
        return coordinates_to_point(beginning_point)
    return beginning_point


def parse_finishing_point():
    finishing_point = get_option('-f')
    if finishing_point:
        return coordinates_to_point(finishing_point)
    return finishing_point


def op_parse():
    parse_help(print_help)
    true_course = parse_true_course()
    distance = parse_distance()
    beginning_point = parse_beginning_point()
    finishing_point = parse_finishing_point()
    return {'true_course': true_course, 'distance': distance, 'beginning_point': beginning_point, 'finishing_point': finishing_point}


def calculate_point(p1, negative_direction, options):
    p2 = empty_point()
    latitude_delta = options['distance'] * math.cos(math.radians(options['true_course']))
    if p1['latitude']['directions'].upper() in negative_direction:
        latitude_delta *= -1
    p2['latitude']['value'] = p1['latitude']['value'] + latitude_delta
    p2['latitude']['directions'] = p1['latitude']['directions']

    longitude_delta_nm = options['distance'] * math.sin(math.radians(options['true_course']))
    longitude_delta = nmiles_to_longitude(p1['latitude']['value'], longitude_delta_nm)
    if p1['longitude']['directions'].upper() in negative_direction:
        longitude_delta *= -1
    p2['longitude']['value'] = p1['longitude']['value'] + longitude_delta
    p2['longitude']['directions'] = p1['longitude']['directions']
    return p2


def calculate_finishing_point(options):
    options['finishing_point'] = calculate_point(options['beginning_point'], 'SW', options)
    return


def calculate_beginning_point(options):
    options['beginning_point'] = calculate_point(options['finishing_point'], 'NE', options)
    return


def calculate_distance(options):
    # TODO
    pass


def calculate_true_course(options):
    # TODO
    pass


def calculate(options):
    if options['true_course'] and options['distance'] and options['beginning_point'] and options['finishing_point'] is None:
        calculate_finishing_point(options)
    if options['true_course'] and options['distance'] and options['beginning_point'] is None and options['finishing_point']:
        calculate_beginning_point(options)
    if options['true_course'] and options['distance'] is None and options['beginning_point'] and options['finishing_point']:
        calculate_distance(options)
    if options['true_course'] is None and options['distance'] and options['beginning_point'] and options['finishing_point']:
        calculate_true_course(options)
    return options


def pprint(result):
    if options['beginning_point']:
        options['beginning_point'] = point_to_coordinates(options['beginning_point'])
    if options['finishing_point']:
        options['finishing_point'] = point_to_coordinates(options['finishing_point'])
    print(result)


if __name__ == '__main__':
    options = op_parse()
    result = calculate(options)
    pprint(result)
    exit(0) 
