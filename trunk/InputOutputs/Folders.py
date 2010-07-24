# -*- coding: utf-8 -*-

import InputOutputs
from MyObjects import *
from time import gmtime
from os import *
import Dialogs
import Organizer
import Universals

class Folders:
    """currentFilesAndFoldersValues[directory no][value no]

    """
    global readFolders,writeFolders,currentFilesAndFoldersValues, changedValueNumber
    currentFilesAndFoldersValues = []
    changedValueNumber = 0
    
    def readFolders(_directoryPath):
        global currentFilesAndFoldersValues,types,types_nos, changedValueNumber
        changedValueNumber = 0
        currentFilesAndFoldersValues=[]
        fileAndDirectoryNames = InputOutputs.readDirectory(_directoryPath, "fileAndDirectory")
        allItemNumber = len(fileAndDirectoryNames)
        Universals.startThreadAction()
        for dirNo,dirName in enumerate(fileAndDirectoryNames):
            isContinueThreadAction = Universals.isContinueThreadAction()
            if isContinueThreadAction:
                dInfo=[]
                dInfo.append(InputOutputs.getBaseName(_directoryPath))
                dInfo.append(dirName)
                currentFilesAndFoldersValues.append(dInfo)
            else:
                allItemNumber = dirNo+1
            Dialogs.showState(translate("InputOutputs/Folders", "Reading Directory Informations"),dirNo+1,allItemNumber, True) 
            if isContinueThreadAction==False:
                break
        Universals.finishThreadAction()
    
    def writeFolders(_table):
        global changedValueNumber
        changedValueNumber = 0
        changingFileDirectories=[]
        if Universals.isShowOldValues==True:
            startRowNo,rowStep=1,2
        else:
            startRowNo,rowStep=0,1
        Universals.startThreadAction()
        allItemNumber = len(currentFilesAndFoldersValues)
        Dialogs.showState(translate("InputOutputs/Folders", "Writing Directory Informations"),0,allItemNumber, True)
        for rowNo in range(startRowNo,_table.rowCount(),rowStep):
            if Universals.isShowOldValues==True:
                realRowNo=rowNo/2
            else:
                realRowNo=rowNo
            isContinueThreadAction = Universals.isContinueThreadAction()
            if isContinueThreadAction:
                if InputOutputs.isWritableFileOrDir(InputOutputs.currentDirectoryPath+"/"+str(currentFilesAndFoldersValues[realRowNo][1])):
                    if _table.isRowHidden(rowNo):
                        InputOutputs.removeFileOrDir(InputOutputs.currentDirectoryPath+"/"+str(currentFilesAndFoldersValues[realRowNo][1]), True)
                        continue
                    newFileName=str(currentFilesAndFoldersValues[realRowNo][1])
                    if _table.isColumnHidden(1)!=True and _table.item(rowNo,1).isSelected()==Universals.isChangeSelected or Universals.isChangeAll==True:
                        if str(currentFilesAndFoldersValues[realRowNo][1])!=unicode(_table.item(rowNo,1).text()).encode("utf-8"):
                            if unicode(_table.item(rowNo,1).text()).encode("utf-8").strip()!="":
                                _table.setItem(rowNo,1,MTableWidgetItem(str(unicode(_table.item(rowNo,1).text()).encode("utf-8")).decode("utf-8")))
                                newFileName = InputOutputs.moveOrChange(InputOutputs.currentDirectoryPath+"/"+str(currentFilesAndFoldersValues[realRowNo][1]),InputOutputs.currentDirectoryPath+"/"+unicode(_table.item(rowNo,1).text()).encode("utf-8"), InputOutputs.getObjectType(InputOutputs.currentDirectoryPath+"/"+str(currentFilesAndFoldersValues[realRowNo][1])))
                                changedValueNumber += 1
                    if newFileName==False:
                        continue
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
                            changingFileDirectories[-1].append(InputOutputs.currentDirectoryPath+"/"+newFileName)
                            changingFileDirectories[-1].append(newPath+"/"+newDirectoryName+"/"+newFileName)
                            changedValueNumber += 1
            else:
                allItemNumber = realRowNo+1
            Dialogs.showState(translate("InputOutputs/Folders", "Writing Directory Informations"),realRowNo+1,allItemNumber, True)
            if isContinueThreadAction==False:
                break
        Universals.finishThreadAction()
        return InputOutputs.changeDirectories(changingFileDirectories)

    
