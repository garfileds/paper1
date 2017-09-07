# -*- coding: utf-8 -*-

'''
    计算香农熵
'''

from math import log
import re

import adoug.tools as tools

def calShannonEnt(dataSet):
    '''@fn 计算香农熵'''
    propabilitySet = {}
    shannoEnt = 0.0
    length = len(dataSet)

    for data in dataSet:
        if data not in propabilitySet.keys():
            propabilitySet[data] = 0
        propabilitySet[data] += 1

    for key in propabilitySet:
        prop = float(propabilitySet[key]) / length
        shannoEnt -= prop * log(prop, 2)

    return shannoEnt

def singleFile(dataPath):
    rrSet = []
    with open(dataPath) as f:
        for line in f.readlines():
            # 兼容两种数据格式：换行或空格做分隔符
            if re.match('\d+\n', line) is not None:
                rrSet.append(line.strip())
            else:
                rrSet.extend(re.split('\s', line.strip()))

    print('AE of %s is : %s' % (dataPath, str(calShannonEnt(rrSet))))
    return calShannonEnt(rrSet)

def multiFiles(path):
    fileLists = tools.GetFileList(path)
    for file in fileLists:
        singleFile(file)
