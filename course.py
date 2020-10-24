#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'Akinava'
__author_email__ = 'akinava@gmail.com'
__copyright__ = 'Copyright © 2020'
__license__ = 'MIT License'
__version__ = [0, 0]


from variation import parse_true_course, parse_variation, calculate_true_course, calculate_variation
from deviation import parse_deviation, parse_compass_course, calculate_deviation, calculate_compass_course
from variation import calculate_magnetic_course as calculate_variation_magnetic_course
from deviation import calculate_magnetic_course as calculate_deviation_magnetic_course
from utility import parse_help, get_option, angle_cast


def print_help():
    print('run:', __file__, 'args')
    print('args: -t true_course, -v variation, -m magnetic_course, -d deviation, -c compass_course')
    print('example:', __file__, '-v \'5W\' -m \'20\'')
    print('example:', __file__, '-v \'3 35E 2007 (5E)\'')
    print('example:', __file__, '-v \'./path/to/variation_file.txt\'')
    print('example:', __file__, '-d \'5W\' -m \'100\'')
    print('example:', __file__, '-d \'./path/to/deviation_file.csv\' -c \'200\'')
    print('example of file variation_file.txt > \'3 35E 2007 (5E)\'')
    print('example of file deviation_file.csv > \'C,M\'')
    print('                                     \'0,2\'')
    print('                                     \'30,29\'')
    print('                                     \'...,...\'')
    print('                                     \'330,331\'')
    print('help: -h | print help')


def parse_magnetic_course():
    magnetic_course = get_option('-m')
    if magnetic_course:
        return angle_cast(int(magnetic_course))
    return magnetic_course


def op_parse():
    parse_help(print_help)
    true_course = parse_true_course()
    variation = parse_variation()
    magnetic_course = parse_magnetic_course()
    deviation = parse_deviation()
    compass_course = parse_compass_course()
    return {'true_course': true_course, 'variation': variation, 'magnetic_course': magnetic_course, 'deviation': deviation, 'compass_course': compass_course}


def get_task(options):
    if options['true_course'] is None and options['variation'] and options['magnetic_course']:
        return calculate_true_course
    if options['true_course'] and options['variation'] is None and options['magnetic_course']:
        return calculate_variation
    if options['true_course'] and options['variation'] and options['magnetic_course'] is None:
        return calculate_variation_magnetic_course
    if options['magnetic_course'] is None and options['deviation'] and options['compass_course']:
        return calculate_deviation_magnetic_course 
    if options['magnetic_course'] and options['deviation'] is None and options['compass_course']:
        return calculate_deviation 
    if options['magnetic_course'] and options['deviation'] and options['compass_course'] is None:
        return calculate_compass_course 


def calculate(options):
    while get_task(options):
        task = get_task(options)
        task(options)
    return options


if __name__ == '__main__':
    options = op_parse()
    result = calculate(options)
    print(result)
    exit(0) 
