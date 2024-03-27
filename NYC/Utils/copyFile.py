import os

def copyFileFromTo(fileStart, target, destList):
    currentPath = os.path.dirname(os.path.abspath(__file__))
    print(currentPath)
    path_to_files = os.path.join(currentPath, '/GraphFusionModel')  # Hier den Pfad anpassen
    print(path_to_files)
    allFileList = [e for e in os.listdir(path_to_files) if e.startswith(fileStart) and e.endswith('.py')]
    allFileName = [e[:-3] for e in allFileList]

    rankRange = destList
    sourceRank = target

    sourceFile = ''
    targetFileList = []
    for i in range(len(allFileName)):
        fileName = allFileName[i].split('_')
        rank = int(fileName[-1])
        if rank == sourceRank:
            sourceFile = allFileList[i]
        elif rank >= min(rankRange) and rank <= max(rankRange):
            targetFileList.append(allFileList[i])

    # get source file content
    if sourceFile == '':
        print('Can not find source file')
    else:
        with open(os.path.join(path_to_files, sourceFile), 'r', encoding='utf-8') as f:
            sourceFileContent = f.readlines()
        if len(targetFileList) == 0:
            print('No target file')
        else:
            for targetFile in targetFileList:
                with open(os.path.join(currentPath, targetFile), 'w', encoding='utf-8') as f:
                    f.writelines(sourceFileContent)
    print('Succeed')
    print("Dateien im Verzeichnis:", os.listdir(currentPath))


if __name__ == '__main__':
    # copyFileFromTo('GraphSingleStationDemandPre', 0, [1, 9])
    copyFileFromTo('GraphSingleStationDemandPreV2', 0, [1, 299])
    copyFileFromTo('GraphFusionModel_', 0, [1, 299])
    # generateFile('GraphFusionModel_%s.py', 0, [1, 299])
