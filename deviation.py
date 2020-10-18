#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'Akinava'
__author_email__ = 'akinava@gmail.com'
__copyright__ = 'Copyright © 2020'
__license__ = 'MIT License'
__version__ = [0, 0]


import sys


def print_help():
    print('run:', __file__, 'args')
    print('example:', __file__, '-d \'/path/to/deviation_file.csv\' -m \'100\'')
    print('example:', __file__, '-d \'./path/to/deviation_file.csv\' -c \'200\'')
    print('example of file deviation_file.csv > \'C,M\'')
    print('                                     \'0,2\'')
    print('                                     \'30,29\'')
    print('                                     \'...,...\'')
    print('                                     \'330,331\'')
    print('help: -h | print help')


def parse_help():
    if '-h' in sys.argv:
        print_help()
        exit(0)


def read_file(file_path):
    with open(file_path) as f:
        return f.read()

def get_option(option):
    if not option in sys.argv:
        return None
    option_index = sys.argv.index(option)
    if option_index+1 == len(sys.argv):
        return None
    return sys.argv[option_index+1]


def angle_cast(angle):
    while angle > 359:
        angle -= 360
    while angle < 0:
        angle += 360
    return angle


def get_deviation(options):
    deviation_file = read_file(options['deviation'])
    deviation_file_lines = deviation_file.split('\n')
    course = options['magnetic_course'] if options['compass_course'] is None else options['compass_course']
  
    if course == 0:
        first_line = 1
        last_line = 2
    else:
        first_line = int(course / 30) + 1
        last_line = int(course / 30) + 2
    if last_line > 12:
        last_line = 1

    x1, y1 = map(int, deviation_file_lines[first_line].split(','))
    x2, y2 = map(int, deviation_file_lines[last_line].split(','))
    
    k = (y1 - y2)/(x1 - x2)
    m = y1 - x1 * k
    deviation_course = course * k + m
    # E+ W-
    deviation = round(deviation_course - course)
    if deviation > 0:
        options['deviation'] = '{}E'.format(deviation)
    else:
        options['deviation'] = '{}W'.format(-deviation)
    return deviation


def calculate_magnetic_course(options):
    deviation = get_deviation(options)
    options['magnetic_course'] = angle_cast(options['compass_course'] + deviation)
    return options


def calculate_compass_course(options):
    deviation = get_deviation(options)
    options['compass_course'] = angle_cast(options['magnetic_course'] - deviation)
    return options


def calculate_deviation(options):
    deviation = options['magnetic_course'] - options['compass_course']
    if deviation > 0:
        return '{}E'.format(deviation)
    return '{}W'.format(-deviation)


def calculate(options):
    if options['magnetic_course'] is None:
        return calculate_magnetic_course(options)
    if options['compass_course'] is None:
        return calculate_compass_course(options)
    if options['deviation'] is None:
        return calculate_deviation(options)
    raise Exception('deviation task error')


def parse_magnetic_course():
    magnetic_course = get_option('-m')
    if magnetic_course:
        return angle_cast(int(magnetic_course))
    return magnetic_course


def parse_compass_course():
    compass_course = get_option('-c')
    if compass_course:
        return angle_cast(int(compass_course))
    return compass_course


def parse_deviation():
    return get_option('-d')


def op_parse():
    parse_help()
    magnetic_course = parse_magnetic_course()
    compass_course = parse_compass_course()
    deviation = parse_deviation()
    return {'magnetic_course': magnetic_course, 'compass_course': compass_course, 'deviation': deviation}


if __name__ == '__main__':
    options = op_parse()
    result = calculate(options)
    print(result)
