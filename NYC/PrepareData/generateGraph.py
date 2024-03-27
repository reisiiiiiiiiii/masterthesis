from dataAPI.utils import *
from functools import reduce
from scipy.stats import pearsonr
from dateutil.parser import parse
import numpy as np
import os
import csv
import json

def checkZero(valueList):
    result = True
    for e in valueList:
        if e != 0:
            return False
    return result

if __name__ == '__main__':
    stationIDDict = getJsonData('centralStationIDList.json')
    centralStationIDList = stationIDDict['centralStationIDList']
    allStationIDList = stationIDDict['allStationIDList']

    # distance graph
    graphMatrix = [[0 for _ in range(len(allStationIDList))] for _ in range(len(allStationIDList))]
    for i in range(len(allStationIDList)):
        for j in range(len(allStationIDList)):
            if i != j:
                distance = computeDistanceBetweenAB(allStationIDList[i], allStationIDList[j])
                distance = 100 if distance == 0 else distance
                graphMatrix[i][j] = 1.0 / distance
    graphMatrix = np.array(graphMatrix, dtype=np.float32)
    for i in range(len(allStationIDList)):
        graphMatrix[i] /= np.sum(graphMatrix[i])
        graphMatrix[i][i] = 1
    np.savetxt(os.path.join(txtPath, 'distanceGraphMatrix.txt'), graphMatrix, delimiter=' ', newline='\n')

    # demand graph
    transitionMatrix = np.loadtxt(os.path.join(txtPath, 'transitionMatrix.txt'), delimiter=' ')
    demandGraphMatrix = np.array(transitionMatrix, dtype=np.float32).transpose()
    for i in range(len(allStationIDList)):
        demandSum = np.sum(demandGraphMatrix[i]) or 1
        demandGraphMatrix[i] /= demandSum
        demandGraphMatrix[i][i] += 1
    np.savetxt(os.path.join(txtPath, 'demandGraphMatrix.txt'), demandGraphMatrix, delimiter=' ', newline='\n')

    # demand mask
    demandMask = np.array([[0 for _ in range(len(allStationIDList))] for _ in range(len(centralStationIDList))])
    for i, centralStation in enumerate(centralStationIDList):
        if centralStation in allStationIDList:
            j = allStationIDList.index(centralStation)
            demandMask[i][j] = 1
    np.savetxt(os.path.join(txtPath, 'demandMask.txt'), demandMask, delimiter=' ', newline='\n')

    # fusion graph
    fusionGraphMatrix = np.array(graphMatrix)
    inDemandTransition = transitionMatrix.transpose()
    for i in range(len(allStationIDList)):
        for j in range(len(allStationIDList)):
            if i != j:
                distance = computeDistanceBetweenAB(allStationIDList[i], allStationIDList[j]) or 100
                fusionGraphMatrix[i][j] = inDemandTransition[i, j] / distance
    for i in range(len(allStationIDList)):
        sumRow = np.sum(fusionGraphMatrix[i]) or 1
        fusionGraphMatrix[i] /= sumRow
        fusionGraphMatrix[i][i] = 1
    np.savetxt(os.path.join(txtPath, 'fusionGraphMatrix.txt'), fusionGraphMatrix, delimiter=' ', newline='\n')

    # fusion graph 2
    fusionGraphMatrix2 = 0.5 * graphMatrix + 0.5 * demandGraphMatrix
    np.savetxt(os.path.join(txtPath, 'fusionGraphMatrix2.txt'), fusionGraphMatrix2, delimiter=' ', newline='\n')

    # demand correlation graph
    if not os.path.isfile(os.path.join(txtPath, 'demandListForGraph.txt')):
        demandList = []
        timeRange = ['2015-01-01', '2015-12-31']
        timeSlot = 60
        for stationIndex in range(len(allStationIDList)):
            date = parse(timeRange[0])
            endData = parse(timeRange[1])
            stationMinDemandData = getJsonDataFromPath(os.path.join(demandMinDataPath, allStationIDList[stationIndex] + '.json'))
            dayIn, dayOut, daySum = [], [], []
            while date <= endData:
                dateString = date.strftime('%Y-%m-%d')
                if isWorkDay(dateString) and not isBadDay(dateString):
                    # Code to fill inList, outList, and sumList...
                  date += datetime.timedelta(days=1)
            if dayIn:
                demandList.append(reduce(lambda x, y: x + y, dayIn))
            else:
                demandList.append([0] * (1440 // timeSlot))
                np.savetxt(os.path.join(txtPath, 'correlationGraphMatrix.txt'), correlationGraph, newline='\n', delimiter=' ')
