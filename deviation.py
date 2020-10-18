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
    print('example:', __file__, '-f \'/path/to/deviation_file.csv\' -m \'100\'')
    print('example:', __file__, '-f \'./path/to/deviation_file.csv\' -c \'200\'')
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


def op_parse():
    parse_help()

if __name__ == '__main__':
    ptions = op_parse()
