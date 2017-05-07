#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
    fileOverview: 对wfdb数据进行wqrs，得到不同部位同时测量ECG的RR结果集
'''

import os
import re
import subprocess
import logging

logging.basicConfig(level=logging.INFO and logging.DEBUG)

NormalfitTime, QuantizationTime = 1200, 60
QunanInterval = list(range(NormalfitTime, NormalfitTime + QuantizationTime * 11, QuantizationTime))


def paddCommand(command, *param):
    return re.sub(r'{(\d)}', lambda match: param[int(match.group(1), 10)], command)


def doNothing():
    print('doNothing')


def splitDir(path):
    result = re.split(r'/', path)
    return result[0], result[1]


def checkRecord(dbName, record):
    '''
    @fn 检测记录是否存在和所测信号
    @param dbName:str
    @param record:str
    @return tuple(记录是否存在，所测信号)
    '''
    tempRdsamp = 'rdsamp -r {0}/{1} -f 0 -t 1 -s {2}'
    signals = ['MLI', 'V5', 'V4', 'MLIII', 'V1', 'V2']
    signalList = []

    for signal in signals:
        s = subprocess.Popen(paddCommand(tempRdsamp, dbName, record, signal), shell=True, stdout=subprocess.PIPE)
        s.wait()
        result = s.communicate()
        if result[0] != b'':
            signalList.append(signal)

    if len(signalList) == 0:
        isExist = False
    else:
        isExist = True

    return (isExist, signalList)


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
    with open(path[0] + '/rr/RR_' + path[1], 'w') as f:
        f.write(' '.join(rr))

    return


def index(dbName, recordList):
    '''
    @fn 利用wqrs算法检测不同信号的qrs时间点，从而计算RR间隔
    @param dbName:string 数据库名称
    @param recordList:list 记录名称列表
    @return 各信号qrs时间点文件和RR间隔文件
    '''
    tempWqrs = 'wqrs -r {0}/{1} -H -f {2} -t {3} -p {4} -s {5}'
    tempRdann = 'rdann -a wqrs -r {0}/{1} > {2}'
    tempSampfreq = 'sampfreq {0}/{1}'

    # 统计量

    # 得到数据采集的频率
    s = subprocess.Popen(paddCommand(tempSampfreq, dbName, recordList[0]), shell=True, stdout=subprocess.PIPE)
    s.wait()
    result = s.communicate()
    if result[0] != b'-1\n':
        frequency = result[0].decode().strip('\n')

    # 初始化：清空统计量文件
    with open('statistic/%s_signals' % (dbName), 'w') as f:
        f.write('')

    for record in recordList:
        recordIsExist, signalList = checkRecord(dbName, record)
        with open('statistic/%s_signals' % (dbName), 'a') as f:
            f.write('%s: %s' % (record, str(signalList)))

        if not recordIsExist:
            continue

        # 定义文件目录
        outDir = dbName + '_prerun_raw/'
        if not os.path.isdir(outDir):
            os.makedirs(outDir)

        outFile = outDir + record + '_' + signalList[0] + '_normalFit.txt'
        outFile = '%s%s/%s_%s_normalFit.txt' % (outDir, 'qrs', record, signalList[0])

        # 计算normalFit qrs集
        logging.info('Command: %s' % paddCommand(tempWqrs, dbName, record, '0', str(NormalfitTime), str(frequency), signalList[0]))
        s = subprocess.run(paddCommand(tempWqrs, dbName, record, '0', str(NormalfitTime), str(frequency), signalList[0]), shell=True, stdout=subprocess.PIPE)

        logging.info('Command: %s' % paddCommand(tempRdann, dbName, record, outFile))
        s = subprocess.run(paddCommand(tempRdann, dbName, record, outFile), shell=True, stdout=subprocess.PIPE)

        # 计算RR间隔值
        while not os.path.isfile(outFile):
            doNothing()
        computeRR(outFile)

        # 计算多份quantization
        for i in range(len(QunanInterval) - 1):
            for signal in signalList:
                outFile = '%s%s/%s_%s_quantization_%s.txt' % (outDir, 'qrs', record, signal, str(i))

                logging.info('Command: %s' % paddCommand(tempWqrs, dbName, record, str(QunanInterval[i]), str(QunanInterval[i+1]), str(frequency), signal))
                s = subprocess.Popen(paddCommand(tempWqrs, dbName, record, str(QunanInterval[i]), str(QunanInterval[i+1]), str(frequency), signal))
                s.wait()

                logging.info('Command: %s' % paddCommand(tempRdann, dbName, record, outFile))
                s = subprocess.Popen(paddCommand(tempRdann, dbName, record, outFile))
                s.wait()
                while not os.path.isfile(outFile):
                    doNothing()
                computeRR(outFile)


# numberList = list(range(103, 171))
numberList = []
numberList.extend(list(range(202, 214)))
# numberList.extend(list(range(302, 307)))
# numberList.extend(list(range(403, 419)))
# numberList.extend(list(range(601, 616)))

recordList = list(map(lambda number: 'e0' + str(number), numberList))
# recordList = ['100']
index('edb', recordList)
