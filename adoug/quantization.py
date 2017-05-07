#! /usr/bin/python
# -*- coding: utf-8 -*-

'''
    fileOverview: 对检测到的IPI进行特征提取
'''

import re

FeatureNum = 30


def judgeDomain(data):
    for i in range(len(domains)):
        if (data > float(domains[i]) and data <= float(domains[i + 1])):
            return hex(i)[2:]


def _readIpt(path):
    """read file, return string result"""
    ipt = []
    with open(path) as f:
        for line in f.readlines():
            ipt.append(line.strip())
    return ' '.join(ipt)


def filterIpt(pattern, ipt):
    match = re.findall(pattern, ipt)

    intMatch = list(map(lambda item: float(item) - AVERAGE, match))
    return intMatch


def featureGenerator(path, average, u, sigma, round2=False):
    '''entry function'''
    global domains, AVERAGE, U, SIGMA
    AVERAGE, U, SIGMA = average, u, sigma

    if round2:
        ipiCount = 5
    else:
        ipiCount = 3

    dataSet = filterIpt(r'\d+', _readIpt(path))
    # 如果是第二轮，需要从新的时间点开始处理数据
    if round2:
        cutIndex = FeatureNum * 3 + 1
        dataSet = dataSet[cutIndex:len(dataSet)]

    domains = ['-inf', U - 1.534 * SIGMA, U - 1.151 * SIGMA, U - 0.887 * SIGMA, U - 0.675 * SIGMA, U - 0.489 * SIGMA, U - 0.319 * SIGMA, U - 0.157 * SIGMA, U, U + 0.157 * SIGMA, U + 0.319 * SIGMA, U + 0.489 * SIGMA, U + 0.675 * SIGMA, U + 0.887 * SIGMA, U + 1.151 * SIGMA, U + 1.534 * SIGMA, 'inf']

    extract, feature = [], []

    # 提取IPI的末尾bit
    for item in dataSet:
        extract.append(judgeDomain(item))

    i, length = 0, len(extract)
    limit = min(length, FeatureNum * ipiCount)
    while True:
        resultFea = ''
        if (i + ipiCount - 1 < limit):
            for num in range(ipiCount):
                resultFea += extract[i + num]
            feature.append(resultFea)
            i += ipiCount
        else:
            break

    return feature
