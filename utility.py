#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'Akinava'
__author_email__ = 'akinava@gmail.com'
__copyright__ = 'Copyright © 2020'
__license__ = 'MIT License'
__version__ = [0, 0]


import sys
import os


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


