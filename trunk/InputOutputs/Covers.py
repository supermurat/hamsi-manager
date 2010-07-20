# -*- coding: utf-8 -*-

import InputOutputs
from MyObjects import *
from time import gmtime
from os import *
import Dialogs
import Organizer
import Universals

class Covers:
    """currentFilesAndFoldersValues[file no][value no]

    """
    global readCovers,writeCovers,currentFilesAndFoldersValues, changedValueNumber
    currentFilesAndFoldersValues = []
    changedValueNumber = 0
    
    def readCovers(_directoryPath):
        global currentFilesAndFoldersValues,types,types_nos, changedValueNumber
        changedValueNumber = 0
        currentFilesAndFoldersValues=[]
        InputOutputs.allFilesAndDirectories = InputOutputs.readDirectoryWithSubDirectories(_directoryPath, 
                    int(Universals.MySettings["CoversSubDirectoryDeep"]), True, True)
        for dirNo,dirName in enumerate(InputOutputs.allFilesAndDirectories):
            fileValues=[]
            fileValues.append(str(str(InputOutputs.getBaseName(_directoryPath)) + 
                            str(InputOutputs.getDirName(dirName)).replace(_directoryPath,"")))
            fileValues.append(InputOutputs.getBaseName(dirName))
            iconPath, isCorrectedFileContent = InputOutputs.getIconFromDirectory(dirName)
            selectedName = None
            if isCorrectedFileContent and iconPath!=None:
                selectedName = InputOutputs.getBaseName(iconPath)
            sourceCover = InputOutputs.getFirstImageInDirectory(dirName, selectedName, False, False)
            if iconPath==None:
                iconPath = ""
            if sourceCover==None:
                sourceCover = ""
            else:
                sourceCover = dirName + "/" + sourceCover
            fileValues.append(iconPath)
            fileValues.append(sourceCover)
            fileValues.append(sourceCover)
            fileValues.append(isCorrectedFileContent)
            currentFilesAndFoldersValues.append(fileValues)
            Dialogs.showState(translate("InputOutputs/Covers", "Reading Cover Informations"),
                              dirNo+1,len(InputOutputs.allFilesAndDirectories)) 
    
    def writeCovers(_table):
        global changedValueNumber
        changedValueNumber = 0
        changingFileDirectories=[]
        startRowNo,rowStep=0,1
        Dialogs.showState(translate("InputOutputs/Covers", "Writing Cover Informations"),0,len(currentFilesAndFoldersValues))
        for rowNo in range(startRowNo,_table.rowCount(),rowStep):
            realRowNo=rowNo
            if InputOutputs.isWritableFileOrDir(str(InputOutputs.getDirName(InputOutputs.currentDirectoryPath))+"/"+str(currentFilesAndFoldersValues[realRowNo][0])+"/"+str(currentFilesAndFoldersValues[realRowNo][1])):
                if _table.isRowHidden(rowNo):
                    InputOutputs.removeFileOrDir(str(InputOutputs.getDirName(InputOutputs.currentDirectoryPath))+"/"+str(currentFilesAndFoldersValues[realRowNo][0])+"/"+str(currentFilesAndFoldersValues[realRowNo][1]))
                    continue
                newFileName=str(currentFilesAndFoldersValues[realRowNo][1])
                if _table.isColumnHidden(1)!=True and _table.item(rowNo,1).isSelected()==Universals.isChangeSelected or Universals.isChangeAll==True:
                    if str(currentFilesAndFoldersValues[realRowNo][1])!=unicode(_table.item(rowNo,1).text()).encode("utf-8"):
                        if unicode(_table.item(rowNo,1).text()).encode("utf-8").strip()!="":
                            _table.setItem(rowNo,1,MTableWidgetItem(str(unicode(_table.item(rowNo,1).text()).encode("utf-8")).decode("utf-8")))
                            newFileName = InputOutputs.moveOrChange(str(InputOutputs.getDirName(InputOutputs.currentDirectoryPath))+"/"+str(currentFilesAndFoldersValues[realRowNo][0])+"/"+str(currentFilesAndFoldersValues[realRowNo][1]), str(InputOutputs.getDirName(InputOutputs.currentDirectoryPath))+"/"+str(currentFilesAndFoldersValues[realRowNo][0])+"/"+unicode(_table.item(rowNo,1).text()).encode("utf-8"), InputOutputs.getObjectType(str(InputOutputs.getDirName(InputOutputs.currentDirectoryPath))+"/"+str(currentFilesAndFoldersValues[realRowNo][0])+"/"+str(currentFilesAndFoldersValues[realRowNo][1])))
                            changedValueNumber += 1
                if newFileName==False:
                    continue
                #Cover Proccess
                if (_table.isColumnHidden(3)!=True and (_table.item(rowNo,3).isSelected()==Universals.isChangeSelected or Universals.isChangeAll==True)) or (_table.isColumnHidden(4)!=True and (_table.item(rowNo,4).isSelected()==Universals.isChangeSelected or Universals.isChangeAll==True)):
                    sourcePath = currentFilesAndFoldersValues[realRowNo][3]
                    destinationPath = currentFilesAndFoldersValues[realRowNo][4]
                    if (_table.isColumnHidden(3)!=True and (_table.item(rowNo,3).isSelected()==Universals.isChangeSelected or Universals.isChangeAll==True)):
                        sourcePath = unicode(_table.item(rowNo,3).text()).encode("utf-8").strip()
                    if (_table.isColumnHidden(4)!=True and (_table.item(rowNo,4).isSelected()==Universals.isChangeSelected or Universals.isChangeAll==True)):
                        destinationPath = unicode(_table.item(rowNo,4).text()).encode("utf-8").strip()
                    if (unicode(_table.item(rowNo,2).text()).encode("utf-8")!=sourcePath or sourcePath!=destinationPath or unicode(_table.item(rowNo,2).text()).encode("utf-8")!=destinationPath) or (unicode(_table.item(rowNo,2).text()).encode("utf-8")!=currentFilesAndFoldersValues[realRowNo][2] and(unicode(_table.item(rowNo,2).text()).encode("utf-8")!=sourcePath and unicode(_table.item(rowNo,2).text()).encode("utf-8")!=destinationPath)):
                        if unicode(_table.item(rowNo,3).text()).encode("utf-8").strip()!="":
                            sourcePath = InputOutputs.getRealPath(sourcePath, str(InputOutputs.getDirName(InputOutputs.currentDirectoryPath))+"/"+str(currentFilesAndFoldersValues[realRowNo][0])+"/"+newFileName)
                            if InputOutputs.checkSource(sourcePath, "file"):
                                if destinationPath!="":
                                    destinationPath = InputOutputs.getRealPath(destinationPath, str(InputOutputs.getDirName(InputOutputs.currentDirectoryPath))+"/"+str(currentFilesAndFoldersValues[realRowNo][0])+"/"+newFileName)
                                    if sourcePath!=destinationPath:
                                        destinationPath = InputOutputs.moveOrChange(sourcePath, destinationPath)
                                else:
                                    destinationPath = sourcePath
                                if destinationPath!=False:
                                    InputOutputs.setIconToDirectory(str(InputOutputs.getDirName(InputOutputs.currentDirectoryPath))+"/"+str(currentFilesAndFoldersValues[realRowNo][0]) + "/" + newFileName, destinationPath)
                                    changedValueNumber += 1
                        else:
                            InputOutputs.setIconToDirectory(str(InputOutputs.getDirName(InputOutputs.currentDirectoryPath))+"/"+str(currentFilesAndFoldersValues[realRowNo][0])+"/"+newFileName, "")
                            changedValueNumber += 1
                if _table.isColumnHidden(0)!=True and _table.item(rowNo,0).isSelected()==Universals.isChangeSelected or Universals.isChangeAll==True:
                    newDirectoryName=unicode(_table.item(rowNo,0).text()).encode("utf-8")
                    try:
                        newDirectoryName=int(newDirectoryName)
                        newDirectoryName=str(newDirectoryName)
                    except:
                        if newDirectoryName.decode("utf-8").lower()==newDirectoryName.upper():
                            newDirectoryName=str(currentFilesAndFoldersValues[realRowNo][0])
                    if str(currentFilesAndFoldersValues[realRowNo][0])!=newDirectoryName:
                        newPath=InputOutputs.getDirName(InputOutputs.currentDirectoryPath)
                        changingFileDirectories.append([])
                        changingFileDirectories[-1].append(str(newPath)+"/"+str(currentFilesAndFoldersValues[realRowNo][0])+"/"+str(newFileName))
                        changingFileDirectories[-1].append(str(newPath)+"/"+str(newDirectoryName)+"/"+str(newFileName))
                        changedValueNumber += 1
            actionNumber=rowNo
            Dialogs.showState(translate("InputOutputs/Covers", "Writing Cover Informations"),actionNumber+1,len(currentFilesAndFoldersValues))
        return InputOutputs.changeDirectories(changingFileDirectories)

