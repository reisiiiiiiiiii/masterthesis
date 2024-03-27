import os

def copyFileFromTo(fileStart, target, destList):
    currentPath = os.path.dirname(os.path.abspath(__file__))
    print(currentPath)
    path_to_files = "/content/masterthesis/NYC/GraphFusionModel" # vollständiger Pfad zu den GraphFusionModel-Dateien
    print(path_to_files)
    allFileList = [e for e in os.listdir(path_to_files) if e.startswith(fileStart) and e.endswith('.py')]
    allFileName = [e[:-3] for e in allFileList]

    sourceRank = target

    sourceFile = ''
    targetFileList = []
    for fileName in allFileName:
        rank_str = fileName.split('V')[-1] # Extrahiere den Rang als Zeichenfolge nach 'V'
        if rank_str.isdigit(): # Überprüfe, ob der Rang eine Zahl ist
            rank = int(rank_str)
            if rank == sourceRank:
                sourceFile = fileName + '.py' # Füge die Dateierweiterung '.py' hinzu
            elif rank >= destList[0] and rank <= destList[1]:
                targetFileList.append(fileName + '.py')

    # Quelldateiinhalt erhalten
    if sourceFile == '':
        print('Can not find source file')
    else:
        with open(os.path.join(path_to_files, sourceFile), 'r', encoding='utf-8') as f:
            sourceFileContent = f.readlines()
        if len(targetFileList) == 0:
            print('No target file')
        else:
            for targetFile in targetFileList:
                with open(os.path.join(currentPath, targetFile + '.py'), 'w', encoding='utf-8') as f:
                    f.writelines(sourceFileContent)
    print('Succeed')
    print("Dateien im Verzeichnis:", os.listdir(path_to_files))


if __name__ == '__main__':
    copyFileFromTo('GraphFusionModelV', 14, [1, 299])

    #copyFileFromTo('GraphSingleStationDemandPre', 0, [1, 9])
    #copyFileFromTo('GraphSingleStationDemandPreV2', 0, [1, 299])
    #copyFileFromTo('GraphFusionModel_', 0, [1, 299])
    #generateFile('GraphFusionModel_%s.py', 0, [1, 299])
