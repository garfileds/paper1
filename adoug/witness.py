# -*- coding: utf-8 -*-
import re
import math

from adoug.grayCode import *


class Witness:

    def __init__(self, dataPath, regionMap, bits):
        self.bits = bits
        self.regionMap = regionMap
        self.dataset = list(map(lambda x: int(x)/1000, Witness.extractList(dataPath)))

    @staticmethod
    def extractList(dataPath):
        dataList = []
        with open(dataPath) as f:
            for line in f.readlines():
                # 兼容两种数据格式：换行或空格做分隔符
                if re.match('\d+\n', line) is not None:
                    dataList.append(line.strip())
                else:
                    dataList.extend(re.split('\s', line.strip()))

        return dataList

    @staticmethod
    def element2bit(element, region, grayCodeLib):
        regionNum = len(region) - 1

        for i in list(range(regionNum)):
            if region[i] <= element < region[i + 1]:
                if i >= regionNum - 1:
                    return grayCodeLib[0]
                else:
                    return grayCodeLib[i]

    def quantizer(self, level):
        datasetQuantization = []
        region = self.regionMap[level]
        grayCodeLib = GrayCode().getGray(level)

        for element in self.dataset:
            datasetQuantization.append(Witness.element2bit(element, region, grayCodeLib))

        return datasetQuantization

    def getWitness(self, level):
        datasetQuantization = self.quantizer(level)

        witnessList = []
        pointer = 0
        pointerBase = 0
        base = math.ceil(self.bits / level)
        remainer = base * level - self.bits
        datasetLen = len(self.dataset)

        if remainer == 0:
            remainer = -base * level

        while len(witnessList) <= 3000 and pointerBase + 1 <= datasetLen:
            while pointer <= datasetLen:
                elementList = datasetQuantization[pointer: pointer + base]
                witnessList.append(''.join(elementList)[: -remainer])
                pointer = pointer + base
            pointerBase += 10
            pointer = pointerBase

        return witnessList
