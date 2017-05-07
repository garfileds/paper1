#! /usr/bin/python
# -*- coding: utf-8 -*-

'''
    fileOverview: 杂活琐碎活都在这里，业务代码
'''

import normalFit as dataProcess
import quantizationForExact as quan
import tools
import math
import permutation as pm


def entryOfCalEntroy(dataFileName):
    output = []

    for dataFile in dataFileName:
        average, u, sigma = dataProcess.process(dataFile)
        dataSet = quan.featureGenerator(dataFile, average, u, sigma)
        result = tools.calShannonEnt(dataSet)

        output.append(result)

    with open('../static/entroyOfEdb.txt', 'w') as f:
        for index in range(len(output)):
            f.write(dataFileName[index] + ': ' + str(output[index]) + '\n')
        f.write('熵的平均值是：' + str(sum(output) / len(output)) + '\n')

# edb的数据
# dataFileName = tools.GetFileList('../data/input/edb/', ['RR', 'normalFit'])

# mitdb的数据
# dataFileName = tools.GetFileList('../data/input/mitdb/', ['RR', 'normalFit'])

# entryOfCalEntroy(dataFileName)


def entryOfCompareEntroy(path):
    '''
    @fn 计算特征值和IPI的熵，随样本数量变化
    '''
    outputOfFeature = []
    outputOfIPI = []

    iterableArr = list(range(1, 155))[4:151:5]

    average, u, sigma = dataProcess.process(path)
    dataSetOfFeature = quan.featureGenerator(path, average, u, sigma)
    dataSetOfIPI = quan.filterIpt(r'\d+', quan._readIpt(path))
    for i in iterableArr:
        entroyOfFeature = round(tools.calShannonEnt(dataSetOfFeature[0:i]), 2)
        entroyOfIPI = round(tools.calShannonEnt(dataSetOfIPI[0:i]), 2)
        outputOfFeature.append(entroyOfFeature)
        outputOfIPI.append(entroyOfIPI)

    with open('../static/outputOfFeature.txt', 'w') as f:
        for entroy in outputOfFeature:
            f.write(str(entroy) + '\t')

    with open('../static/outputOfIPI.txt', 'w') as f:
        for entroy in outputOfIPI:
            f.write(str(entroy) + '\t')

# entryOfCompareEntroy('../data/input/edb/RR_e0103_MLIII_normalFit.txt')


def splitPath(path):
    '''
    @fn 分割文件路径，得到文件名称（含后缀）
    '''
    interList = path.split('/')
    return interList[len(interList) - 1]


def getInputOfNIST(paths):
    '''
    @fn 获取特征提取值，作为NIST随机数测试的输入
    @param paths:list 记录IPI的文件路径
    '''
    for path in paths:
        average, u, sigma = dataProcess.process(path)
        dataSetOfFeature = quan.featureGenerator(path, average, u, sigma)

        output = splitPath(path)
        with open('../static/featureExtract/' + output, 'w') as f:
            f.write(' '.join(dataSetOfFeature))

    return

# dataFileName = tools.GetFileList('../data/input/mitdb/', ['RR', 'normalFit'])
# getInputOfNIST([dataFileName[0]])


def calStrengthOfCoffer():
    cofferSize = [300, 600, 1000, 2000, 4000, 8000]
    threshold = list(range(5, 16))

    for size in cofferSize:
        for num in threshold:
            print('%s and %s: %s\n' % (size, num, math.log(pm.permcount(size, num), 2)))

calStrengthOfCoffer()
