#! /usr/bin/python
# -*- coding: utf-8 -*-

'''
    fileOverview: 各种分析数据的小工具
'''

import numpy as np
from math import log
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt

import normalFit as dataProcess


def draw(path):
    '''
    @fn 绘制离散数据的直方图
    @param path:string 数据文件路径
    '''
    ipt = dataProcess._readIpt(path)
    a, dataSet, o = dataProcess.filterIpt(r'\d+', ipt)
    pointSet = np.array(dataSet)
    u, sigma = dataProcess.estimateNormal(dataSet)
    n, bins, patches = plt.hist(pointSet, 100, normed=1, facecolor='green', alpha=0.5)
    y = mlab.normpdf(bins, u, sigma)
    y = np.add.accumulate(pointSet)
    plt.plot(bins, y, 'r--')
    plt.xlabel('Difference between IPI and average')
    plt.ylabel('Probability')
    plt.title(r'Histogram of difference: $\mu=0$, $\sigma=40$')
    plt.show()

# draw('../data/input/edb/RR_e0113_MLIII_normalFit.txt')


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


def IsSubString(SubStrList, Str):
    '''
    @fn 判断Str是否包含SubStrList中的字符串
    '''
    flag = True
    for substr in SubStrList:
        if not(substr in Str):
            flag = False

    return flag


def GetFileList(FindPath, FlagStr=[]):
    '''
    @fn 获取FindPath目录下的指定文件名
    '''
    import os
    FileList = []
    FileNames = os.listdir(FindPath)
    if (len(FileNames) > 0):
        for fn in FileNames:
            if (len(FlagStr) > 0):
                # 返回指定类型的文件名
                if (IsSubString(FlagStr, fn)):
                    fullfilename = os.path.join(FindPath, fn)
                    FileList.append(fullfilename)
            else:
                # 默认直接返回所有文件名
                fullfilename = os.path.join(FindPath, fn)
                FileList.append(fullfilename)

    # 对文件名排序
    if (len(FileList) > 0):
        FileList.sort()

    return FileList
