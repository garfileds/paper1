#! /usr/bin/python
# -*- coding: utf-8 -*-

'''fileOverview: 排列组合的常用方法'''

import scipy.misc as ms


def permcount(n, r):
    return facUtil(n, r)


def combcount(n, r):

    return permcount(n, r) / (ms.factorial(r) * 1)


def facUtil(start, end):
    result = start
    for i in range(end - 1):
        result = result * (start - i - 1)

    return float(format(result, '.2e'))
