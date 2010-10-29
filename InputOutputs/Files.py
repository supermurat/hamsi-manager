# -*- coding: utf-8 -*-

import InputOutputs
from MyObjects import *
from time import gmtime
from os import *
import Dialogs
import Organizer
import Universals

class Files:
    """currentFilesAndFoldersValues[file no][value no]

    """
    global readFiles,writeFiles,currentFilesAndFoldersValues, changedValueNumber
    currentFilesAndFoldersValues = []
    changedValueNumber = 0
    
    def readFiles(_directoryPath):
        global currentFilesAndFoldersValues, changedValueNumber
        changedValueNumber = 0
        currentFilesAndFoldersValues=[]
        fileNames = InputOutputs.IA.readDirectory(_directoryPath, "file")
        allItemNumber = len(fileNames)
        Universals.startThreadAction()
        for fileNo,fileName in enumerate(fileNames):
            isContinueThreadAction = Universals.isContinueThreadAction()
            if isContinueThreadAction:
                fInfo=[]
                fInfo.append(InputOutputs.IA.getBaseName(_directoryPath))
                fInfo.append(fileName)
                currentFilesAndFoldersValues.append(fInfo)
            else:
                allItemNumber = fileNo+1
            Dialogs.showState(translate("InputOutputs/Files", "Reading File Informations"),fileNo+1,allItemNumber, True) 
            if isContinueThreadAction==False:
                break
        Universals.finishThreadAction()
    
    def writeFiles(_table):
        global changedValueNumber
        changedValueNumber = 0
        changingFileDirectories=[]
        if Universals.isShowOldValues==True:
            startRowNo,rowStep=1,2
        else:
            startRowNo,rowStep=0,1
        Universals.startThreadAction()
        allItemNumber = len(currentFilesAndFoldersValues)
        Dialogs.showState(translate("InputOutputs/Files", "Writing File Informations"),0,allItemNumber, True)
        for rowNo in range(startRowNo,_table.rowCount(),rowStep):
            if Universals.isShowOldValues==True:
                realRowNo=rowNo/2
            else:
                realRowNo=rowNo
            isContinueThreadAction = Universals.isContinueThreadAction()
            if isContinueThreadAction:
                if InputOutputs.IA.isWritableFileOrDir(InputOutputs.IA.currentDirectoryPath+"/"+str(currentFilesAndFoldersValues[realRowNo][1])):
                    if _table.isRowHidden(rowNo):
                        InputOutputs.IA.removeFileOrDir(InputOutputs.IA.currentDirectoryPath+"/"+str(currentFilesAndFoldersValues[realRowNo][1]))
                        continue
                    newFileName=str(currentFilesAndFoldersValues[realRowNo][1])
                    if _table.isColumnHidden(1)!=True and _table.item(rowNo,1).isSelected()==Universals.isChangeSelected or Universals.isChangeAll==True:
                        if str(currentFilesAndFoldersValues[realRowNo][1])!=unicode(_table.item(rowNo,1).text()).encode("utf-8"):
                            if unicode(_table.item(rowNo,1).text()).encode("utf-8").strip()!="":
                                _table.setItem(rowNo,1,MTableWidgetItem(str(unicode(_table.item(rowNo,1).text()).encode("utf-8")).decode("utf-8")))
                                newFileName = InputOutputs.IA.moveOrChange(InputOutputs.IA.currentDirectoryPath+"/"+str(currentFilesAndFoldersValues[realRowNo][1]),InputOutputs.IA.currentDirectoryPath+"/"+unicode(_table.item(rowNo,1).text()).encode("utf-8"))
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
                            newPath=InputOutputs.IA.getDirName(InputOutputs.IA.currentDirectoryPath)
                            changingFileDirectories.append([])
                            changingFileDirectories[-1].append(newPath+"/"+str(currentFilesAndFoldersValues[realRowNo][0])+"/"+newFileName)
                            changingFileDirectories[-1].append(newPath+"/"+newDirectoryName+"/"+newFileName)
                            changedValueNumber += 1
            else:
                allItemNumber = realRowNo+1
            Dialogs.showState(translate("InputOutputs/Files", "Writing File Informations"),realRowNo+1,allItemNumber, True)
            if isContinueThreadAction==False:
                break
        Universals.finishThreadAction()
        return InputOutputs.IA.changeDirectories(changingFileDirectories)

    
