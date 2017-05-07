#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
    fileOverview: 对原始RR处理得到(g, g')的样本
'''

import random


def readRR(rr1File, rr2File):
  file1 = open(rr1File, 'r')
  file2 = open(rr2File, 'r')

  rr1Lines = file1.readlines()
  rr2Lines = file2.readlines()

  file1.close()
  file2.close()

  return (rr1Lines, rr2Lines)


def getGG(rr1File, rr2File, record):
  rr1Lines, rr2Lines = readRR(rr1File, rr2File)

  with open('data/sample/gg_%s.txt' % record, 'w') as f:
    result = []

    for i in range(len(rr1Lines)):
      result.append('%s %s\n' % (rr1Lines[i].strip('\r\n'), rr2Lines[i].strip('\r\n')))

    f.write(''.join(result))


def getGI_G(rr1File, rr2File, record):
  rr1Lines, rr2Lines = readRR(rr1File, rr2File)

  result = []
  lenRR2 = len(rr2Lines)

  for rr1 in rr1Lines:
    rr2Index = random.randint(0, lenRR2-1)
    rr2 = rr2Lines[rr2Index]
    result.append('%s %s\n' % (rr1.strip('\r\n'), rr2.strip('\r\n')))

  with open('data/sample/gi_g_%s.txt' % record, 'w') as f:
    f.write(''.join(result))


def getGI_other(rr1File, rr2File, record1, record2):
  rr1Lines, rr2Lines = readRR(rr1File, rr2File)

  result = []
  for i in range(min(len(rr1Lines), len(rr2Lines))):
      rr1 = rr1Lines[i].strip('\r\n')
      rr2 = rr2Lines[i].strip('\r\n')
      result.append('%s %s\n' % (rr1, rr2))

  with open('data/sample/gi_other_%s_%s.txt' % (record1, record2), 'w') as f:
    f.write(''.join(result))

getGG('data/rr/RR_e0103_MLIII_normalFit.txt', 'data/rr/RR_e0103_V4_normalFit.txt', 'e0103')
getGI_G('data/rr/RR_e0103_MLIII_normalFit.txt', 'data/rr/RR_e0103_V4_normalFit.txt', 'e0103')
getGI_other('data/rr/RR_e0103_MLIII_normalFit.txt', 'data/rr/RR_e0123_MLIII_normalFit.txt', 'e0103', 'e0123')
