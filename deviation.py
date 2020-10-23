#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'Akinava'
__author_email__ = 'akinava@gmail.com'
__copyright__ = 'Copyright © 2020'
__license__ = 'MIT License'
__version__ = [0, 0]


from utility import (
        course_to_number,
        parse_help,
        get_option,
        angle_cast,
        read_file)


def print_help():
    print('run:', __file__, 'args')
    print('args: -m magnetic_course, -c compass_course, -d deviation')
    print('example:', __file__, '-d \'/path/to/deviation_file.csv\' -m \'100\'')
    print('example:', __file__, '-d \'./path/to/deviation_file.csv\' -c \'200\'')
    print('example of file deviation_file.csv > \'C,M\'')
    print('                                     \'0,2\'')
    print('                                     \'30,29\'')
    print('                                     \'...,...\'')
    print('                                     \'330,331\'')
    print('help: -h | print help')


def get_deviation(options):
    deviation_file = read_file(options['deviation'])

    if deviation_file is None:
        return course_to_number(options['deviation'])

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

    c1, m1 = map(int, deviation_file_lines[first_line].split(','))
    c2, m2 = map(int, deviation_file_lines[last_line].split(','))

    if first_line == 1 and m1 > 30:
        m1 = -(360 - m1)

    if last_line == 1 and m2 > 30:
        m2 = -(360 - m2)
    
    k = (m1 - m2)/(c1 - c2)
    t = m1 - c1 * k
    deviation_course = course * k + t
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


def calculate_compass_course(options):
    deviation = get_deviation(options)
    options['compass_course'] = angle_cast(options['magnetic_course'] - deviation)


def calculate_deviation(options):
    deviation = options['magnetic_course'] - options['compass_course']
    options['deviation'] = number_to_course(deviation)


def calculate(options):
    if options['magnetic_course'] is None:
        calculate_magnetic_course(options)
    elif options['compass_course'] is None:
        calculate_compass_course(options)
    elif options['deviation'] is None:
        calculate_deviation(options)
    else:
        raise Exception('deviation task error')
    return options


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
    parse_help(print_help)
    magnetic_course = parse_magnetic_course()
    compass_course = parse_compass_course()
    deviation = parse_deviation()
    return {'magnetic_course': magnetic_course, 'compass_course': compass_course, 'deviation': deviation}


if __name__ == '__main__':
    options = op_parse()
    result = calculate(options)
    print(result)
    exit(0)
