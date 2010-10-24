# -*- coding: utf-8 -*-

import InputOutputs
from MyObjects import *
from time import gmtime
from os import *
import Dialogs
import Organizer
import Universals

class SubFolders:
    """currentFilesAndFoldersValues[file no][value no]

    """
    global readSubFolders,writeSubFolders,currentFilesAndFoldersValues, changedValueNumber
    currentFilesAndFoldersValues = []
    changedValueNumber = 0
    
    def readSubFolders(_directoryPath):
        global currentFilesAndFoldersValues,types,types_nos, changedValueNumber
        changedValueNumber = 0
        currentFilesAndFoldersValues=[]
        allFilesAndDirectories = InputOutputs.IA.readDirectoryWithSubDirectories(_directoryPath, 
                    int(Universals.MySettings["subDirectoryDeep"]))
        allItemNumber = len(allFilesAndDirectories)
        Universals.startThreadAction()
        for fileNo,fileName in enumerate(allFilesAndDirectories):
            isContinueThreadAction = Universals.isContinueThreadAction()
            if isContinueThreadAction:
                fileValues=[]
                fileValues.append(str(str(InputOutputs.IA.getBaseName(_directoryPath)) + 
                                str(InputOutputs.IA.getDirName(fileName)).replace(_directoryPath,"")))
                fileValues.append(InputOutputs.IA.getBaseName(fileName))
                currentFilesAndFoldersValues.append(fileValues)
            else:
                allItemNumber = fileNo+1
            Dialogs.showState(translate("InputOutputs/SubFolders", "Reading File Informations"),
                              fileNo+1,allItemNumber, True) 
            if isContinueThreadAction==False:
                break
        Universals.finishThreadAction()
    
    def writeSubFolders(_table):
        global changedValueNumber
        changedValueNumber = 0
        changingFileDirectories=[]
        if Universals.isShowOldValues==True:
            startRowNo,rowStep=1,2
        else:
            startRowNo,rowStep=0,1
        Universals.startThreadAction()
        allItemNumber = len(currentFilesAndFoldersValues)
        Dialogs.showState(translate("InputOutputs/SubFolders", "Writing File Informations"),0,allItemNumber, True)
        for rowNo in range(startRowNo,_table.rowCount(),rowStep):
            if Universals.isShowOldValues==True:
                realRowNo=rowNo/2
            else:
                realRowNo=rowNo
            isContinueThreadAction = Universals.isContinueThreadAction()
            if isContinueThreadAction:
                if InputOutputs.IA.isWritableFileOrDir(str(InputOutputs.IA.getDirName(InputOutputs.IA.currentDirectoryPath))+"/"+str(currentFilesAndFoldersValues[realRowNo][0])+"/"+str(currentFilesAndFoldersValues[realRowNo][1])):
                    if _table.isRowHidden(rowNo):
                        InputOutputs.IA.removeFileOrDir(str(InputOutputs.IA.getDirName(InputOutputs.IA.currentDirectoryPath))+"/"+str(currentFilesAndFoldersValues[realRowNo][0])+"/"+str(currentFilesAndFoldersValues[realRowNo][1]))
                        continue
                    newFileName=str(currentFilesAndFoldersValues[realRowNo][1])
                    if _table.isColumnHidden(1)!=True and _table.item(rowNo,1).isSelected()==Universals.isChangeSelected or Universals.isChangeAll==True:
                        if str(currentFilesAndFoldersValues[realRowNo][1])!=unicode(_table.item(rowNo,1).text()).encode("utf-8"):
                            if unicode(_table.item(rowNo,1).text()).encode("utf-8").strip()!="":
                                _table.setItem(rowNo,1,MTableWidgetItem(str(unicode(_table.item(rowNo,1).text()).encode("utf-8")).decode("utf-8")))
                                newFileName = InputOutputs.IA.moveOrChange(str(InputOutputs.IA.getDirName(InputOutputs.IA.currentDirectoryPath))+"/"+str(currentFilesAndFoldersValues[realRowNo][0])+"/"+str(currentFilesAndFoldersValues[realRowNo][1]),str(InputOutputs.IA.getDirName(InputOutputs.IA.currentDirectoryPath))+"/"+str(currentFilesAndFoldersValues[realRowNo][0])+"/"+unicode(_table.item(rowNo,1).text()).encode("utf-8"))
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
                            changingFileDirectories[-1].append(str(newPath)+"/"+str(currentFilesAndFoldersValues[realRowNo][0])+"/"+str(newFileName))
                            changingFileDirectories[-1].append(str(newPath)+"/"+str(newDirectoryName)+"/"+str(newFileName))
                            changedValueNumber += 1
            else:
                allItemNumber = realRowNo+1
            Dialogs.showState(translate("InputOutputs/SubFolders", "Writing File Informations"),realRowNo+1,allItemNumber, True)
            if isContinueThreadAction==False:
                break
        Universals.finishThreadAction()
        return InputOutputs.IA.changeDirectories(changingFileDirectories)
    