#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'Akinava'
__author_email__ = 'akinava@gmail.com'
__copyright__ = 'Copyright © 2020'
__license__ = 'MIT License'
__version__ = [0, 0]


import course
import track
import track_point


def compare_list(obj1, obj2):
    if len(obj1) != len(obj2):
        return False
    for i in range(len(obj1)):
        if compare(obj1[i], obj2[i]) is False:
            return False
    return True


def compare_dict(obj1, obj2):
    if len(obj1) != len(obj2):
        return False
    for k, v in obj1.items():
        if not k in obj2:
            return False
        if compare(obj1[k], obj2[k]) is False:
            return False
    return True


def compare(obj1, obj2):
    if type(obj1) != type(obj2):
        return False
    if isinstance(obj1, dict):
        return compare_dict(obj1, obj2)
    if isinstance(obj1, list):
        return compare_list(obj1, obj2)
    if obj1 != obj2:
        return False
    return True


def report(func, data, result, reference):
    if compare(result, reference) is False:
        print('Error: {}.{}\ndata:      {}\nresult:    {}\nreference: {}'.format(func.__module__, func.__name__, data, result, reference))


def course_calculate_test():
    data = [
        [{'true_course': None, 'variation': None, 'magnetic_course': None, 'deviation': None, 'compass_course': None},
         {'true_course': None, 'variation': None, 'magnetic_course': None, 'deviation': None, 'compass_course': None}],
        [{'true_course': None, 'variation': None, 'magnetic_course': None, 'deviation': './deviation.csv', 'compass_course': 359},
         {'true_course': None, 'variation': None, 'magnetic_course': 355, 'deviation': '4W', 'compass_course': 359}],
        [{'true_course': None, 'variation': None, 'magnetic_course': None, 'deviation': './deviation.csv', 'compass_course': 1},
         {'true_course': None, 'variation': None, 'magnetic_course': 359, 'deviation': '2W', 'compass_course': 1}],
        [{'true_course': None, 'variation': None, 'magnetic_course': None, 'deviation': './deviation.csv', 'compass_course': 0},
         {'true_course': None, 'variation': None, 'magnetic_course': 358, 'deviation': '2W', 'compass_course': 0}],
        [{'true_course': None, 'variation': None, 'magnetic_course': None, 'deviation': '3E', 'compass_course': 0},
         {'true_course': None, 'variation': None, 'magnetic_course': 3, 'deviation': '3E', 'compass_course': 0}],
        [{'true_course': None, 'variation': '7 20E 2013 (8E)', 'magnetic_course': 180, 'deviation': '3E', 'compass_course': None},
         {'true_course': 188, 'variation': '8E', 'magnetic_course': 180, 'deviation': '3E', 'compass_course': 177}],
        [{'true_course': None, 'variation': '8E', 'magnetic_course': 180, 'deviation': '3E', 'compass_course': None},
         {'true_course': 188, 'variation': '8E', 'magnetic_course': 180, 'deviation': '3E', 'compass_course': 177}],
        [{'true_course': 132, 'variation': '4E', 'magnetic_course': None, 'deviation': '2W', 'compass_course': None},
         {'true_course': 132, 'variation': '4E', 'magnetic_course': 128, 'deviation': '2W', 'compass_course': 130}],
        [{'true_course': None, 'variation': '6E', 'magnetic_course': 358, 'deviation': '6W', 'compass_course': None},
         {'true_course': 4, 'variation': '6E', 'magnetic_course': 358, 'deviation': '6W', 'compass_course': 4}],
        [{'true_course': None, 'variation': '6W', 'magnetic_course': 2, 'deviation': '6E', 'compass_course': None},
         {'true_course': 356, 'variation': '6W', 'magnetic_course': 2, 'deviation': '6E', 'compass_course': 356}],
    ]
    for data, reference in data:
        result = course.calculate(dict(data))
        report(course.calculate, data, result, reference)


def track_calculate_test():
    data = [
        [{'speed': 5.0, 'distance': None, 'time': '2.5', 'time_beginning': None, 'time_finishing': None},
         {'speed': 5.0, 'distance': 12.5, 'time': '2:30', 'time_beginning': None, 'time_finishing': None}]
    ]
    for data, reference in data:
        result = track.calculate(dict(data))
        result = track.pprint(result)
        report(track.calculate, data, result, reference)


def track_point_test():
    data = [
        [{'true_course': 0, 'distance': 60.0, 'beginning_point': '02 00.0N,24 00.0E', 'finishing_point': None},
         {'true_course': 0, 'distance': 60.0, 'beginning_point': '02 00.0N,24 00.0E', 'finishing_point': '03 00.0N,24 00.0E'}],
        [{'true_course': 90, 'distance': 60.0, 'beginning_point': '02 00.0N,24 00.0E', 'finishing_point': None},
         {'true_course': 90, 'distance': 60.0, 'beginning_point': '02 00.0N,24 00.0E', 'finishing_point': '02 00.0N,25 00.0E'}],
        [{'true_course': 180, 'distance': 60.0, 'beginning_point': '02 00.0N,24 00.0E', 'finishing_point': None},
         {'true_course': 180, 'distance': 60.0, 'beginning_point': '02 00.0N,24 00.0E', 'finishing_point': '01 00.0N,24 00.0E'}],
        [{'true_course': 270, 'distance': 60.0, 'beginning_point': '02 00.0N,24 00.0E', 'finishing_point': None},
         {'true_course': 270, 'distance': 60.0, 'beginning_point': '02 00.0N,24 00.0E', 'finishing_point': '02 00.0N,23 00.0E'}],
    ]
    for data, reference in data:
        result = track_point.calculate(dict(data))
    result = track_point.pprint(result)
    report(track_point.calculate, data, result, reference)


if __name__ == '__main__':
    course_calculate_test()
    track_calculate_test()
    track_point_test()
    exit(0)