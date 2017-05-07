#! /usr/bin/python
# -*- coding: utf-8 -*-

'''
    fileOverview: 对大量IPI数据进行分析，得到正态分布的参数
'''

import re
import numpy as np
from scipy.stats import norm


def _paddStr(str, len):
    return ('000000' + str).slice(-len)


def _readIpt(path):
    """read file, return string result"""
    ipt = []
    with open(path) as f:
        for line in f.readlines():
            ipt.append(line.strip())
    return ' '.join(ipt)


def filterIpt(pattern, ipt):
    '''
    @fn 处理输入得到rr间隔; rr间隔减去平均值，得到的数据满足正态分布
    @param pattern:regular 根据输入设置的正则
    @return diffMatch:list 各rr与平均值的差值
    '''

    match = re.findall(pattern, ipt)

    intMatch = list(map(lambda item: float(item), match))
    total = sum(intMatch)
    average = int(total / len(intMatch))
    diffMatch = list(map(lambda item: item - average, intMatch))

    return average, diffMatch, intMatch


def estimateNormal(dataSet):
    '''
    @fn 假定数据集满足正态分布，求其参数
    @param dataSet:list
    @return u, sigma
    '''
    return norm.fit(np.array(dataSet))


def process(path):
    '''
    @fn 归一化的入口函数
    '''
    global AVERAGE, U, SIGMA
    ipt = _readIpt(path)
    AVERAGE, dataSet, originSet = filterIpt(r'\d+', ipt)
    U, SIGMA = estimateNormal(dataSet)

    return AVERAGE, round(U), round(SIGMA)
