#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'Akinava'
__author_email__ = 'akinava@gmail.com'
__copyright__ = 'Copyright © 2020'
__license__ = 'MIT License'
__version__ = [0, 0]


import sys
import os
import math


def read_file(file_path):
    if not os.path.isfile(file_path):
        return None
    with open(file_path) as f:
        return f.read()


def get_option(option):
    if not option in sys.argv:
        return None
    option_index = sys.argv.index(option)
    if option_index+1 == len(sys.argv):
        return None
    return sys.argv[option_index+1]


def parse_help(print_help):
    if '-h' in sys.argv:
        print_help()
        exit(0)


def angle_cast(angle):
    while angle > 359:
        angle -= 360
    while angle < 0:
        angle += 360
    return angle

def course_to_number(course):
    direction = course[-1].upper()
    angle = course[0:-1]
    if 'E' == direction:
        return int(angle)
    if 'W' == direction:
        return -int(angle)
    raise Exception('course does not have a direction')


def number_to_course(course):
    if course > 0:
        return '{}E'.format(course)
    else:
        return '{}W'.format(-course)


def empty_point():
    #                             0-90                N/S                           0-180               E/W
    return {'latitude': {'value': None, 'directions': None}, 'longitude': {'value': None, 'directions': None}}


def coordinates_to_point(coordinates):
    point = empty_point()
    latitude, longitude = coordinates.upper().split(',')
    point['latitude']['value'], point['latitude']['directions'] = coordinate_to_number(latitude)
    point['longitude']['value'], point['longitude']['directions'] = coordinate_to_number(longitude)
    return point


def coordinate_to_number(coordinate):
    if ' ' in coordinate:
        degree, rest = coordinate.split(' ')
        minute = rest[:-1]
        directions = rest[-1]
        number = int(degree) * 60 + float(minute)
    else:
        number = float(coordinate[0:-1]) * 60
        directions = coordinate[-1]
    return number, directions


def distance_between_points(p1, p2):
    latitude_delta = p1['latitude']['value'] - p2['latitude']['value']
    longitude_delta = p1['longitude']['value'] - p2['longitude']['value']
    longitude_delta_nm = longitudes_to_nmiles(p1['latitude']['value'], longitude_delta)
    distance = math.sqrt(latitude_delta**2 + longitude_delta_nm**2)
    return round(distance, 1)


def nmiles_to_longitude(latitude_minutes, nmiles):
    longitude_degrees = latitude_minutes / 60
    return nmiles / math.cos(math.radians(longitude_degrees))


def longitudes_to_nmiles(latitude_minutes, longitudes):
    longitude_degrees = latitude_minutes / 60
    return longitudes * math.cos(math.radians(longitude_degrees))


def calculate_course_by_points(p1, p2):
    latitude_delta = p1['latitude']['value'] - p2['latitude']['value']
    longitude_delta = p1['longitude']['value'] - p2['longitude']['value']
    longitude_delta_nm = longitudes_to_nmiles(p1['latitude']['value'], longitude_delta)
    if longitude_delta_nm == 0 and latitude_delta == 0:
        options['true_course'] = None
        return

    if latitude_delta == 0:
        if longitude_delta_nm > 0:
            options['true_course'] = 270
        else:
            options['true_course'] = 90
        return

    if longitude_delta_nm == 0:
        if latitude_delta > 0:
            options['true_course'] = 180
        else:
            options['true_course'] = 0
        return

    true_course = math.degrees(math.atan(longitude_delta_nm / latitude_delta))
    # 0 - 90 longitude_delta_nm < 0 latitude_delta < 0
    # pass
    # 90 - 180
    if longitude_delta_nm < 0 and latitude_delta > 0:
        true_course = 180 + true_course
    # 180 - 270
    if longitude_delta_nm > 0 and latitude_delta > 0:
        true_course = 180 + true_course
    # 270 - 360
    if longitude_delta_nm > 0 and latitude_delta < 0:
        true_course = 360 + true_course

    return angle_cast(round(true_course))