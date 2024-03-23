import os

projectPath = os.path.dirname(os.path.abspath(__file__))

baseDrivePath = '/content/drive/MyDrive'

# Definiere den relativen Pfad von deinem Google Drive Basispfad zu deinem Datenordner
relativeDataPath = 'Master Thesis Data'

# Setze den Datenordner-Pfad
dataPath = os.path.join(baseDrivePath, relativeDataPath)

csvDataPath = os.path.join(dataPath, 'csvData')

jsonPath = os.path.join(dataPath, 'json')

demandDataPath = os.path.join(dataPath, 'demandData')

pngPath = os.path.join(dataPath, 'png')

rawBikeDataPath = os.path.join(dataPath, 'RawBikeData_2015.csv')

demandMinDataPath = os.path.join(dataPath, 'demandMinData')

txtPath = os.path.join(dataPath, 'TXT')

clusterFilePath = os.path.join(dataPath, 'clusterFilePath')

GraphDemandPreDataPath = os.path.join(dataPath, 'GraphDemandPreData')

if __name__ == '__main__':
    dirList = [projectPath, dataPath, csvDataPath, jsonPath, demandDataPath, pngPath, rawBikeDataPath,
            demandMinDataPath, txtPath, GraphDemandPreDataPath]
    for dir in dirList:
        if os.path.isdir(dir) == False:
            os.mkdir(dir)