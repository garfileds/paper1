#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
    fileOverview: 对wfdb数据进行wqrs，得到不同部位同时测量ECG的RR结果集
'''

import re
import logging

import tools as tool

logging.basicConfig(level=logging.INFO and logging.DEBUG)


def splitDir(path):
    result = re.split(r'\\', path)
    return result


def extractTime(recordLine):
    '''
    @fn 将形如'08:10.854'转成毫秒
    '''
    pattern = r'(\d+):(\d+)\.(\d+)'
    m = re.search(pattern, recordLine.strip('\r\n'))
    return int(m.group(1), 10) * 60000 + int(m.group(2), 10) * 1000 + int(m.group(3), 10)


def computeRR(qrsFile):
    '''
    @fn 根据qrs时间点计算RR间隔
    @param qrsFile:string qrs时间点文件名
    @return RR间隔集文件
    '''
    rr = []
    i, prevTime = 0, 0
    with open(qrsFile) as f:
        for line in f.readlines():
            time = extractTime(line)

            if i == 0:
                prevTime = time
            else:
                rr.append(str(time - prevTime))
                prevTime = time
            i += 1

    path = splitDir(qrsFile)
    logging.info('path:' + str(path))
    with open('../data/rr/RR_' + path[len(path) - 1], 'w') as f:
        f.write('\n'.join(rr))

    return


def index():
    '''
    @fn 由rdann得到的qrs文件计算RR
    '''
    qrsFiles = tool.GetFileList('../data/qrs')
    for qrs in qrsFiles:
        computeRR(qrs)

index()
