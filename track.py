#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'Akinava'
__author_email__ = 'akinava@gmail.com'
__copyright__ = 'Copyright © 2020'
__license__ = 'MIT License'
__version__ = [0, 0]


from datetime import datetime, date, timedelta
from utility import parse_help, get_option


FMT = '%H:%M'


def print_help():
    print('run:', __file__, 'args')
    print('args: -s speed, -t time, -b time_beginning, -f time_finishing, -d distance')
    print('example:', __file__, '-s \'5\' -t \'2:30\'')
    print('example:', __file__, '-s \'5\' -t \'2,5\'')
    print('example:', __file__, '-d \'10\' -s \'5\' -b \'10:20\'')
    print('example:', __file__, '-b \'1:00\' -f \'2:00\' -d \'5\'')        
    print('help: -h | print help')


def parse_speed():
    speed = get_option('-s')
    if speed and speed.isdigit():
        return int(speed)
    return None


def parse_distance():
    distance = get_option('-d')
    if distance and distance.isdigit():
        return int(distance)
    return None


def time_to_float(time):
    return time.seconds/3600


def float_to_time(time):
    if isinstance(time, str) and ',' in time:
        time = time.replace(',', '.')
    return timedelta(hours=float(time))


def string_to_time(time):
    hours, minutes = time.split(':')
    return timedelta(hours=int(hours), minutes=int(minutes))


def parse_time():
    time = get_option('-t')
    if time is None:
        return None
    if ',' in time:
        return float_to_time(time)
    if ':' in time:
        return string_to_time(time)
    raise Exception('parse time error')


def parse_time_boundaries(arg):
    time = get_option(arg)
    if time is None:
        return None
    time = datetime.strptime(time, FMT)
    time.replace(year=date.today().year, month=date.today().month, day=date.today().day)
    return time


def parse_time_beginning():
    return parse_time_boundaries('-b')


def parse_time_finishing():
    return parse_time_boundaries('-f')


def op_parse():
    parse_help(print_help)
    speed = parse_speed()
    distance = parse_distance()
    time = parse_time()
    time_beginning = parse_time_beginning()
    time_finishing = parse_time_finishing()
    return {'speed': speed, 'distance': distance, 'time': time, 'time_beginning': time_beginning, 'time_finishing': time_finishing}


def calculate_time_delta(options):
    options['time'] = options['time_finishing'] - options['time_beginning']


def calculate_time_finishing(options):
    options['time_finishing'] = options['time_beginning'] + options['time']


def calculate_time_beginning(options):
    options['time_beginning'] = options['time_finishing'] - options['time']


def calculate_time(options):
    options['time'] = float_to_time(options['distance'] / options['speed'])


def calculate_distance(options):
    options['distance'] = options['speed'] * time_to_float(options['time'])


def calculate_speed(options):
    options['speed'] = options['distance'] / time_to_float(options['time'])


def get_task(options):
    if options['time_beginning'] and options['time_finishing'] and options['time'] is None:
        return calculate_time_delta
    if options['time_beginning'] and options['time_finishing'] is None and options['time']:
        return calculate_time_finishing
    if options['time_beginning'] is None and options['time_finishing'] and options['time']:
        return calculate_time_beginning
    if options['time'] is None and options['distance'] and options['speed']:
        return calculate_time
    if options['time'] and options['distance'] is None and options['speed']:
        return calculate_distance
    if options['time'] and options['distance'] and options['speed'] is None:
        return calculate_speed


def calculate(options):
    while get_task(options):
        task = get_task(options)
        task(options)
    return options


def pprint(result):
    if result['time']:
        hours, remainder = divmod(result['time'].seconds, 3600)
        minutes = divmod(remainder, 60)[0]
        result['time'] = '{}:{}'.format(hours, minutes)
    if result['time_beginning']:
        result['time_beginning'] = result['time_beginning'].strftime(FMT)
    if result['time_finishing']:
        result['time_finishing'] = result['time_finishing'].strftime(FMT)
    print(result)


if __name__ == '__main__':
    options = op_parse()
    result = calculate(options)
    pprint(result)
    exit(0)
