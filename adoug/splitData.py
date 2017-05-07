#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
    fileOverview: 对wfdb_edb数据进行分解，得到不同部位同时测量的结果
'''

import os
import re
import logging

logging.basicConfig(level=logging.INFO and logging.DEBUG)

NormalfitTime, QuantizationTime = '3600', '600'


def paddCommand(command, *param):
    return re.sub(r'{(\d)}', lambda match: param[int(match.group(1), 10)], command)

# 定义用到的命令模板
tempCp = 'cp {0} {1}'
tempWrsamp = 'wrsamp -i {0} -o {1}'
tempRdsamp = 'rdsamp -r {0} -H -f {1} -t {2} -v -pd -s {3} >{4}'
tempAnn2rr = 'ann2rr -r {0} -a atr -f {1} -t {2} -v T -i s3 -V T -w -W >{3}'

# records = [x.split('.')[0] for x in os.listdir('./edb') if re.search(r'.hea', x)]
records = ['e0103', 'e0104']
for record in records:
    # show sample as text：取前一小时的V4记录用于拟合正态分布
    os.system(paddCommand(tempRdsamp, 'edb/' + record, '0', NormalfitTime, 'V4', 'edb_split/record/' + record + '_V4_normalFit.txt'))
    # convert txt to PhysioBank-compatible formats
    os.system(paddCommand(tempWrsamp, 'edb_split/record/' + record + '_V4_normalFit.txt', 'edb_split/record/' + record + '_V4_normalFit'))
    # 创建相应的atr文件
    os.system(paddCommand(tempCp, 'edb/' + record + '.atr', 'edb_split/record/' + record + '_V4_normalFit.atr'))

    print('next...')
    # show sample as text：取一小时之后的10分钟V4数据作为生成密钥的源
    os.system(paddCommand(tempRdsamp, 'edb/' + record, NormalfitTime, '4200', 'V4', 'edb_split/record/' + record + '_V4_quan.txt'))
    logging.info('执行命令: %s' % paddCommand(tempRdsamp, 'edb/' + record, NormalfitTime, '4200', 'V4', 'edb_split/record/' + record + '_V4_quan.txt'))
    # convert txt to PhysioBank-compatible formats
    os.system(paddCommand(tempWrsamp, 'edb_split/record/' + record + '_V4_quan.txt', 'edb_split/record/' + record + '_V4_quan'))
    logging.info('执行命令: %s' % paddCommand(tempWrsamp, 'edb_split/record/' + record + '_V4_quan.txt', 'edb_split/record/' + record + '_V4_quan'))
    # 创建相应的atr文件
    os.system(paddCommand(tempCp, 'edb/' + record + '.atr', 'edb_split/record/' + record + '_V4_quan.atr'))
    logging.info('执行命令: %s' % paddCommand(tempCp, 'edb/' + record + '.atr', 'edb_split/record/' + record + '_V4_quan.atr'))

    print('next...')
    # show sample as text：取一小时之后的10分钟MLIII数据作为生成密钥的源
    os.system(paddCommand(tempRdsamp, 'edb/' + record, NormalfitTime, '4200', 'MLIII', 'edb_split/record/' + record + '_MLIII_quan.txt'))
    # convert txt to PhysioBank-compatible formats
    os.system(paddCommand(tempWrsamp, 'edb_split/record/' + record + '_MLIII_quan.txt', 'edb_split/record/' + record + '_MLIII_quan'))
    # 创建相应的atr文件
    os.system(paddCommand(tempCp, 'edb/' + record + '.atr', 'edb_split/record/' + record + '_MLIII_quan.atr'))

newRecords = [x.split('.')[0] for x in os.listdir('./edb_split/record') if re.search(r'hea', x)]
for record in newRecords:
    if record.find('normalFit') > -1:
        # show RR intervals as text：用于归一化的
        os.system(paddCommand(tempAnn2rr, 'edb_split/record/' + record, '0', NormalfitTime, 'edb_split/input/' + record + '.txt'))
    else:
        # show RR intervals as text：用于拟合正态分布的
        os.system(paddCommand(tempAnn2rr, 'edb_split/record/' + record, '0', QuantizationTime, 'edb_split/input/' + record + '.txt'))
