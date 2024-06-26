from dataAPI.utils import *


# load the station id
stationIdOrderByBuildTime = getJsonData('stationIdOrderByBuildTime.json')
stationIdList = stationIdOrderByBuildTime['stationID']
transitionMatrix = np.loadtxt(os.path.join(txtPath, 'transitionMatrix.txt'), delimiter=' ')
# get the directed graph
directedGraphWeight = []
demandThreshold = 600
for i in range(len(transitionMatrix)):
    for j in range(len(transitionMatrix[i])):
        if transitionMatrix[i][j] > demandThreshold:
            directedGraphWeight.append([i, j, transitionMatrix[i][j] / np.sum(transitionMatrix, axis=1)[i]])
# get the degree
degreeList = [0 for _ in range(len(stationIdList))]
for edge in directedGraphWeight:
    start = edge[0]
    end = edge[1]
    weight = edge[2]
    degreeList[start] += 1
    degreeList[end] += 1

# find the largest n degree stations
n = stationIdList.__len__()
centralStationList = sorted([[e, degreeList[e]] for e in range(n)], key=lambda x:x[1], reverse=True)
for i in range(n, len(degreeList)):
    degree = degreeList[i]
    for j in range(n):
        if centralStationList[j][1] < degree:
            centralStationList.insert(j, [i, degree])
            del centralStationList[-1]
            break
centralStationList = [e[0] for e in centralStationList]
centralStationLocation = [getStationLocation(stationIdList[e]) for e in centralStationList]
centralStationIDList = [stationIdList[e] for e in centralStationList]
saveJsonData({'centralStationIDList': centralStationIDList,
              'allStationIDList': stationIdList}, 'centralStationIDList.json')