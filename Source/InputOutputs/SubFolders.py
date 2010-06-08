# -*- coding: utf-8 -*-

import InputOutputs
from MyObjects import *
from time import gmtime
from os import *
import Dialogs
import Organizer
import Universals
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
        InputOutputs.allFilesAndDirectories = InputOutputs.readDirectoryWithSubDirectories(_directoryPath, 
                    int(Universals.MySettings["subDirectoryDeep"]))
        for fileNo,fileName in enumerate(InputOutputs.allFilesAndDirectories):
            MApplication.processEvents()
            fileValues=[]
            fileValues.append(str(str(InputOutputs.getBaseName(_directoryPath)) + 
                            str(InputOutputs.getDirName(fileName)).replace(_directoryPath,"")))
            fileValues.append(InputOutputs.getBaseName(fileName))
            currentFilesAndFoldersValues.append(fileValues)
            Dialogs.showState(translate("InputOutputs/SubFolders", "Reading File Informations"),
                              fileNo+1,len(InputOutputs.allFilesAndDirectories)) 
    
    def writeSubFolders(_table):
        global changedValueNumber
        changedValueNumber = 0
        changingFileDirectories=[]
        if Universals.isShowOldValues==True:
            startRowNo,rowStep=1,2
        else:
            startRowNo,rowStep=0,1
        Dialogs.showState(translate("InputOutputs/SubFolders", "Writing File Informations"),0,len(currentFilesAndFoldersValues))
        for rowNo in range(startRowNo,_table.rowCount(),rowStep):
            MApplication.processEvents()
            if Universals.isShowOldValues==True:
                realRowNo=rowNo/2
            else:
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
                            newFileName = InputOutputs.moveOrChange(str(InputOutputs.getDirName(InputOutputs.currentDirectoryPath))+"/"+str(currentFilesAndFoldersValues[realRowNo][0])+"/"+str(currentFilesAndFoldersValues[realRowNo][1]),str(InputOutputs.getDirName(InputOutputs.currentDirectoryPath))+"/"+str(currentFilesAndFoldersValues[realRowNo][0])+"/"+unicode(_table.item(rowNo,1).text()).encode("utf-8"))
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
                        changingFileDirectories[-1].append(str(newPath)+"/"+str(currentFilesAndFoldersValues[realRowNo][0])+"/"+str(newFileName))
                        changingFileDirectories[-1].append(str(newPath)+"/"+str(newDirectoryName)+"/"+str(newFileName))
                        changedValueNumber += 1
            if Universals.isShowOldValues==True:
                actionNumber=rowNo/2
            else:
                actionNumber=rowNo
            Dialogs.showState(translate("InputOutputs/SubFolders", "Writing File Informations"),actionNumber+1,len(currentFilesAndFoldersValues))
        return InputOutputs.changeDirectories(changingFileDirectories)
    