## This file is part of HamsiManager.
## 
## Copyright (c) 2010 - 2013 Murat Demir <mopened@gmail.com>      
##
## Hamsi Manager is free software; you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 2 of the License, or
## (at your option) any later version.
## 
## Hamsi Manager is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.
## 
## You should have received a copy of the GNU General Public License
## along with HamsiManager; if not, write to the Free Software
## Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA


from Core import Variables
from Core import FileManager
from Core import Dialogs
from Core import Universals
import InputOutputs
from Core import Organizer
from Core.MyObjects import *
from Core import ReportBug
from Options import TableQuickOptions

class Tables(MTableWidget):
    def __init__(self, _parent):
        global layouts,widgets
        MTableWidget.__init__(self, _parent)
        self.isAskShowHiddenColumn = True
        self.currentDirectoryPath = ""
        self.newDirectoryPath = ""
        self.currentTableContentValues = []
        self.changedValueNumber = 0
        self.history = []
        self.future = []
        self.setAlternatingRowColors(True)
        self.setWordWrap(False)
        self.setVerticalScrollMode(self.ScrollPerPixel)
        self.setHorizontalScrollMode(self.ScrollPerPixel)
        MObject.connect(self,SIGNAL("cellClicked(int,int)"),self.cellClicked)
        MObject.connect(self,SIGNAL("itemChanged(QTableWidgetItem *)"),self.itemChanged)
        MObject.connect(self,SIGNAL("cellDoubleClicked(int,int)"),self.cellDoubleClicked)
        self.pbtnSave = MPushButton(translate("Tables", "Save"))
        self.pbtnSave.setObjectName("pbtnSave")
        self.pbtnSave.setIcon(MIcon("Images:save.png"))
        self.pbtnShowDetails = MPushButton(translate("Tables", "See Details"))
        self.pbtnTableQuickOptions = MPushButton(translate("Tables", "Options"))
        self.mTableQuickOptions = TableQuickOptions.TableQuickOptions(self)
        self.pbtnTableQuickOptions.setMenu(self.mTableQuickOptions)
        self.tbCorrect = MToolButton()
        self.tbCorrect.setToolTip(translate("Tables", "Re Correct"))
        self.tbCorrect.setIcon(MIcon("Images:correct.png"))
        self.tbCorrect.setAutoRaise(True)
        MObject.connect(self.pbtnShowDetails, SIGNAL("clicked()"), self.showDetails)
        self.actRefresh = MToolButton()
        self.actRefresh.setToolTip(translate("Tables", "Refresh"))
        self.actRefresh.setIcon(MIcon("Images:refresh.png"))
        self.actRefresh.setAutoRaise(True)
        MObject.connect(self.actRefresh, SIGNAL("clicked()"), self.refresh)
        self.tbGoBack = MToolButton()
        self.tbGoForward = MToolButton()
        self.tbCreateHistoryPoint = MToolButton()
        self.tbGoBack.setToolTip(translate("Tables", "Go To Previous Action"))
        self.tbGoForward.setToolTip(translate("Tables", "Perform Next Action"))
        self.tbCreateHistoryPoint.setToolTip(translate("Tables", "Create An Action Point"))
        self.tbGoBack.setIcon(MIcon("Images:edit-undo.png"))
        self.tbGoForward.setIcon(MIcon("Images:edit-redo.png"))
        self.tbCreateHistoryPoint.setIcon(MIcon("Images:createHistoryPoint.png"))
        self.tbGoBack.setAutoRaise(True)
        self.tbGoForward.setAutoRaise(True)
        self.tbCreateHistoryPoint.setAutoRaise(True)
        MObject.connect(self.pbtnSave, SIGNAL("clicked()"), self.save)
        MObject.connect(self.tbGoBack, SIGNAL("clicked()"), self.goBack)
        MObject.connect(self.tbGoForward, SIGNAL("clicked()"), self.goForward)
        MObject.connect(self.tbCreateHistoryPoint, SIGNAL("clicked()"), self.createHistoryPoint)
        MObject.connect(self.tbCorrect, SIGNAL("clicked()"), self.correct)
        _parent.MainLayout.addWidget(self, 10)
        self.mContextMenu = MMenu(self)
        self.hblBox = MHBoxLayout()
        self.hblBox.addWidget(self.pbtnTableQuickOptions)
        self.hblBox.addWidget(self.actRefresh)
        self.hblBox.addWidget(self.tbGoBack)
        self.hblBox.addWidget(self.tbCreateHistoryPoint)
        self.hblBox.addWidget(self.tbGoForward)
        self.hblBox.addWidget(self.tbCorrect)
        self.hblBox.addWidget(self.pbtnShowDetails, 1)
        self.hblBox.addWidget(self.pbtnSave, 2)
        self.setSubTable()
        self.hiddenTableColumns = Universals.getListValue(self.SubTable.hiddenTableColumnsSettingKey)
        _parent.MainLayout.addLayout(self.hblBox)
        self.mContextMenuColumns = MMenu()
        self.mContextMenuColumns.setTitle(translate("Tables", "Show Fields"))
        self.mContextMenuOpenWith = MMenu()
        self.mContextMenuOpenWith.setTitle(translate("Tables", "Open With"))
        self.refreshForColumns()
        self.mContextMenuActionNames = [translate("Tables", "Cut"),
                            translate("Tables", "Copy"),
                            translate("Tables", "Paste"),
                            translate("Tables", "Replace"), 
                            translate("Tables", "Remove From System")]
        for actName in self.mContextMenuActionNames:
            self.mContextMenu.addAction(actName).setObjectName(actName)
        self.mContextMenuOpenWithNames = [translate("Tables", "File Manager"),
                            translate("Tables", "Default Application")]
        if Variables.isWindows == False:
            self.mContextMenuOpenWithNames.append(translate("Tables", "Konsole"))
        for actName in self.mContextMenuOpenWithNames:
            self.mContextMenuOpenWith.addAction(actName).setObjectName(actName)
        self.mContextMenu.addMenu(self.mContextMenuColumns)
        self.mContextMenu.addAction(translate("Tables", "Open Details")).setObjectName(translate("Tables", "Open Details"))
        self.mContextMenu.addMenu(self.mContextMenuOpenWith)
        self.checkActionsStates()
        self.fillSelectionInfo()
    
    def setSubTable(self):
        if Universals.tableType==0:
            from Tables import FolderTable
            self.SubTable = FolderTable.FolderTable(self)
        elif Universals.tableType==1:
            from Tables import FileTable
            self.SubTable = FileTable.FileTable(self)
        elif Universals.tableType==2:
            import Taggers
            if Taggers.getTagger(True)!=None:
                from Tables import MusicTable
                self.SubTable = MusicTable.MusicTable(self)
            else:
                Universals.tableType = 1
                from Tables import FileTable
                self.SubTable = FileTable.FileTable(self)
        elif Universals.tableType==3:
            from Tables import SubFolderTable
            self.SubTable = SubFolderTable.SubFolderTable(self)
        elif Universals.tableType==4:
            if Variables.isActiveDirectoryCover:
                from Tables import CoverTable
                self.SubTable = CoverTable.CoverTable(self)
            else:
                Dialogs.showError(translate("Tables", "Directory Cover Not Usable"), translate("Tables", "Any icon can not set to any directory. This feature is not usable in your system."))
                Universals.tableType = 1
                from Tables import FileTable
                self.SubTable = FileTable.FileTable(self)
        elif Universals.tableType==5:
            import Amarok
            if Amarok.checkAmarok(True,  False):
                Universals.tableType = 5
                import AmarokCoverTable
                self.SubTable = AmarokCoverTable.AmarokCoverTable(self)
            else:
                Universals.tableType = 1
                from Tables import FileTable
                self.SubTable = FileTable.FileTable(self)
        elif Universals.tableType==6:
            import Taggers, Amarok
            if Taggers.getTagger(True)!=None and Amarok.checkAmarok(True,  False):
                import AmarokMusicTable
                self.SubTable = AmarokMusicTable.AmarokMusicTable(self)
            else:
                Universals.tableType = 1
                from Tables import FileTable
                self.SubTable = FileTable.FileTable(self)
        elif Universals.tableType==7:
            import Amarok
            if Amarok.checkAmarok(True,  False):
                import AmarokArtistTable
                self.SubTable = AmarokArtistTable.AmarokArtistTable(self)
            else:
                Universals.tableType = 1
                from Tables import FileTable
                self.SubTable = FileTable.FileTable(self)
        elif Universals.tableType==8:
            import Taggers, Amarok
            if Taggers.getTagger(True)!=None and Amarok.checkAmarok(True,  False):
                import AmarokCopyTable
                self.SubTable = AmarokCopyTable.AmarokCopyTable(self)
            else:
                Universals.tableType = 1
                from Tables import FileTable
                self.SubTable = FileTable.FileTable(self)
            
    
    def getColumnKeyFromName(self, _nameWithMark):
        for x, name in enumerate(self.tableColumns):
            if str(name) == str(_nameWithMark).replace("&", ""):
                return self.tableColumnsKey[x]
        return _nameWithMark
        
    def getColumnNameFromName(self, _nameWithMark):
        for x, name in enumerate(self.tableColumns):
            if str(name) == str(_nameWithMark).replace("&", ""):
                return self.tableColumns[x]
        return _nameWithMark
        
    def getColumnNameFromKey(self, _keyName):
        for x, name in enumerate(self.tableColumnsKey):
            if str(name) == str(_keyName):
                return self.tableColumns[x]
        return _keyName
                        
    def showDetails(self):
        try:
            rowNo = self.currentRow()
            if rowNo!=-1:
                self.SubTable.showDetails(rowNo, self.currentColumn())
        except:
            ReportBug.ReportBug()
    
    def correct(self):
        try:
            self.SubTable.correctTable()
        except:
            ReportBug.ReportBug()
    
    def goBack(self):
        self.future.append(self.createHistoryPoint(True))
        self.goActionPoint(self.history.pop())
        self.checkActionsStates()
        
    def goForward(self):
        self.history.append(self.createHistoryPoint(True))
        self.goActionPoint(self.future.pop())
        self.checkActionsStates()
        
    def createHistoryPoint(self, _isReturn=False):
        point=[]
        for rowNo in range(self.rowCount()):
            point.append([])
            for columnNo in range(self.columnCount()):
                item = self.item(rowNo, columnNo)
                if item is not None:
                    point[-1].append(item.text())
                else:
                    point[-1].append("")
            point[-1].append(self.isRowHidden(rowNo))
        if _isReturn==False:
            self.future = []
            self.history.append(point)
            self.checkActionsStates()
        else:
            return point
    
    def goActionPoint(self, _actionPoint):
        for rowNo, row in enumerate(_actionPoint):
            for columnNo, column in enumerate(row[:-1]):
                item = self.item(rowNo, columnNo)
                if item is not None:
                    item.setText(column)
            if row[-1]==True:
                self.hideRow(rowNo)
            else:
                self.showRow(rowNo)
                
    def checkActionsStates(self):
        if len(self.history)==0:
            self.tbGoBack.setEnabled(False)
        else:
            self.tbGoBack.setEnabled(True)
        if len(self.future)==0:
            self.tbGoForward.setEnabled(False)
        else:
            self.tbGoForward.setEnabled(True)
            
    def clearHistoryPoints(self):
        self.history = []
        self.future = []
        self.checkActionsStates()
            
    def contextMenuEvent(self,_event):
        try:
            currentItem = self.currentItem()
            if currentItem is not None:
                self.mContextMenu.setGeometry(_event.globalX(),_event.globalY(),1,1)
                selectedItem = self.mContextMenu.exec_()
                if selectedItem!=None:
                    if selectedItem.objectName()==self.mContextMenuActionNames[0]:
                        self.createHistoryPoint()
                        MApplication.clipboard().setText(currentItem.text())
                        currentItem.setText("")
                    elif selectedItem.objectName()==self.mContextMenuActionNames[1]:
                        MApplication.clipboard().setText(currentItem.text())
                    elif selectedItem.objectName()==self.mContextMenuActionNames[2]:
                        self.createHistoryPoint()
                        currentItem.setText(MApplication.clipboard().text())
                    elif selectedItem.objectName()==self.mContextMenuActionNames[3]:
                        self.editItem(currentItem)
                    elif selectedItem.objectName()==self.mContextMenuActionNames[4]:
                        self.createHistoryPoint()
                        for rowNo in self.getSelectedRows():
                            self.hideRow(rowNo)
                    elif selectedItem.objectName()==translate("Tables", "Open Details"):
                        self.showDetails()
                    elif selectedItem.objectName()==self.mContextMenuOpenWithNames[0]:
                        from Core import Execute
                        Execute.openWith([InputOutputs.getRealDirName(self.currentTableContentValues[currentItem.row()]["path"])])
                    elif selectedItem.objectName()==self.mContextMenuOpenWithNames[1]:
                        from Core import Execute
                        Execute.openWith([self.currentTableContentValues[currentItem.row()]["path"]])
                    elif Variables.isWindows == False and selectedItem.objectName()==self.mContextMenuOpenWithNames[2]:
                        from Core import Execute
                        Execute.execute(["konsole","--workdir", InputOutputs.getRealDirName(self.currentTableContentValues[currentItem.row()]["path"])])
        except:
            ReportBug.ReportBug()
    
    def getSelectedRows(self):
        sr = []
        for item in self.selectedItems():
            if sr.count(item.row())==0:
                sr.append(item.row())
        return sr
        
    def getSelectedColumns(self):
        sc = []
        for item in self.selectedItems():
            if sc.count(item.column())==0:
                sc.append(item.column())
        return sc
    
    def refreshShowedAndHiddenColumns(self):
        self.hiddenTableColumns = []
        for x, act in enumerate(self.mContextMenuColumnsActions):
            if act.isChecked()==False:
                self.hiddenTableColumns.append(str(x))
        for c in range(len(self.tableColumns)):
            if self.hiddenTableColumns.count(str(c))>0:
                self.hideColumn(c)
            else:
                self.showColumn(c)
    
    def cellClicked(self,_row,_column):
        try:
            self.SubTable.cellClicked(_row, _column)
        except:
            ReportBug.ReportBug()
    
    def cellDoubleClicked(self,_row,_column):
        try:
            self.SubTable.cellDoubleClicked(_row, _column)
        except:
            ReportBug.ReportBug()
    
    def refreshForColumns(self):
        self.mContextMenuColumns.clear()
        self.SubTable.refreshColumns()
        self.mContextMenuColumnsActions = []
        for columnName in self.tableColumns:
            self.mContextMenuColumnsActions.append(MAction(columnName,self.mContextMenuColumns))
        for key,act in enumerate(self.mContextMenuColumnsActions):
            act.setCheckable(True)
            if self.hiddenTableColumns.count(str(key))==0:
                act.setChecked(True)
            self.mContextMenuColumns.addAction(act)
            MObject.connect(act,SIGNAL("triggered(bool)"), self.refreshShowedAndHiddenColumns)
        self.refreshShowedAndHiddenColumns()
        
    def setCurrentDirectory(self, _path):
        if _path=="":
            if hasattr(Universals.MainWindow, "FileManager") and Universals.MainWindow.FileManager is not None:
                _path = Universals.MainWindow.FileManager.getCurrentDirectoryPath()
            else:
                _path = InputOutputs.userDirectoryPath
        self.currentDirectoryPath = _path
        self.newDirectoryPath = _path
    
    def setNewDirectory(self, _path):
        if _path=="":
            _path = self.currentDirectoryPath
        if _path=="":
            if hasattr(Universals.MainWindow, "FileManager") and Universals.MainWindow.FileManager is not None:
                _path = Universals.MainWindow.FileManager.getCurrentDirectoryPath()
            else:
                _path = InputOutputs.userDirectoryPath
        self.newDirectoryPath = _path
        
    def refresh(self, _path = ""):
        global isShowChanges
        self.setCurrentDirectory(_path)
        self.isAskShowHiddenColumn = True
        isShowChanges=False
        self.clearHistoryPoints()
        self.clear()
        self.setColumnCount(len(self.tableColumns))
        self.setHorizontalHeaderLabels(self.tableColumns)
        columnWidth = (Universals.MainWindow.CentralWidget.width()-90)/len(self.tableColumns)
        if columnWidth>110:
            for x in range(len(self.tableColumns)):
                self.setColumnWidth(x,columnWidth)
        from Core import MyThread
        myProcs = MyThread.MyThread(self.SubTable.refresh, self.continueRefresh, [self.currentDirectoryPath])
        myProcs.run()

    def continueRefresh(self, _returned=None):
        global isShowChanges
        isShowChanges=True
        for rowNo in range(self.rowCount()):
            if self.isRowHidden(rowNo):
                self.showRow(rowNo)
        self.refreshShowedAndHiddenColumns()
        if Universals.getBoolValue("isResizeTableColumnsToContents"):
            self.resizeColumnsToContents()
        Universals.MainWindow.StatusBar.setTableInfo(Variables.tableTypesNames[Universals.tableType] + trForUI(" : ") + trForUI(str(self.rowCount())))
        
    def save(self):
        try:
            from Core import Records
            Records.setTitle(Variables.tableTypesNames[Universals.tableType])
            InputOutputs.activateSmartCheckIcon()
            InputOutputs.activateSmartCheckEmptyDirectories()
            from Core import MyThread
            myProcs = MyThread.MyThread(self.SubTable.save, self.continueSave)
            myProcs.run()
        except:
            ReportBug.ReportBug()
        
    def continueSave(self, _returned=None):
        try:
            if _returned:
                from Core import Records
                isGoUpDirectoryWithFileTable = False
                if Universals.tableType in [0, 1, 2, 3, 4]:
                    if Universals.getBoolValue("isClearEmptyDirectoriesWhenSave"):
                        if InputOutputs.checkEmptyDirectories(self.currentDirectoryPath, True, True, Universals.getBoolValue("isAutoCleanSubFolderWhenSave")):
                            isGoUpDirectoryWithFileTable = True
                if isGoUpDirectoryWithFileTable == False or self.currentDirectoryPath != self.newDirectoryPath:
                    if Universals.tableType in [0, 1, 2, 3]:
                        if Variables.isActiveDirectoryCover and Universals.getBoolValue("isActiveAutoMakeIconToDirectory") and Universals.getBoolValue("isAutoMakeIconToDirectoryWhenSave"):
                            InputOutputs.checkIcon(self.newDirectoryPath)
                InputOutputs.completeSmartCheckIcon()
                InputOutputs.completeSmartCheckEmptyDirectories(True, True)
                Records.saveAllRecords()
                if self.changedValueNumber==0:
                    Dialogs.show(translate("Tables", "Did Not Change Any Things"), 
                                 translate("Tables", "Did not change any things in this table.Please check the criteria you select."))
                else:
                    if Universals.getBoolValue("isShowTransactionDetails"):
                        Dialogs.show(translate("Tables", "Transaction Details"), 
                                     str(translate("Tables", "%s value(s) changed.")) % self.changedValueNumber)
                if isGoUpDirectoryWithFileTable and self.currentDirectoryPath == self.newDirectoryPath:
                    Universals.MainWindow.FileManager.goUp()
                elif isGoUpDirectoryWithFileTable and self.currentDirectoryPath != self.newDirectoryPath:
                    Universals.MainWindow.FileManager.makeRefresh(self.newDirectoryPath)
                else:
                    Universals.MainWindow.FileManager.makeRefresh("")
                    if Universals.tableType in [5, 6, 7, 8]:
                        self.refresh(self.newDirectoryPath)
        except:
            ReportBug.ReportBug()
        
    def fillSelectionInfo(self):
        if Universals.getBoolValue("isChangeAll"):
            self.pbtnSave.setText(translate("Tables", "Save"))
            self.pbtnSave.setToolTip(translate("Tables", "All informations will be changed"))
        else:
            self.pbtnSave.setText(str(" ! " + translate("Tables", "Save") + " ! "))
            if Universals.getBoolValue("isChangeSelected"):
                self.pbtnSave.setToolTip(translate("Tables", "Just selected informations will be changed"))
            else:
                self.pbtnSave.setToolTip(translate("Tables", "Just unselected informations will be changed"))
        
    def isChangableItem(self, _rowNo, _columnNo, _checkLikeThis=None, isCanBeEmpty=True, _isCheckLike=True):
        item = self.item(_rowNo, _columnNo)
        if item is not None:
            if item.isReadOnly == False:
                if self.isColumnHidden(_columnNo)!=True and item.isSelected()==Universals.getBoolValue("isChangeSelected") or Universals.getBoolValue("isChangeAll"):
                    if _isCheckLike and _checkLikeThis!=None:
                        if str(_checkLikeThis)!=str(item.text()):
                            if isCanBeEmpty==False:
                                if str(item.text()).strip()!="":
                                    return True
                                return False
                            else:
                                return True
                        return False
                    else:
                        if isCanBeEmpty==False:
                            if str(item.text()).strip()!="":
                                return True
                            return False
                        else:
                            return True
        return False
        
    def createTableWidgetItem(self, _value, _currentValue=None, _isReadOnly = False):
        item = MyTableWidgetItem(_currentValue)
        item.setText(trForUI(_value))
        item.isReadOnly = _isReadOnly
        if _isReadOnly:
            item.setToolTip(translate("Tables", "This value is NOT changeable!"))
            item.setFlags(Mt.ItemIsSelectable | Mt.ItemIsEnabled)
        return item
    
    def itemChanged(self, _item):
        if _item.text()!=_item.currentText and _item.isReadOnly==False:
            _item.setToolTip(_item.currentText)
            _item.setBackground(MBrush(MColor(142,199,255)))
        
    def checkUnSavedValues(self, _isForceToCheck=False):
        if Universals.getBoolValue("isCheckUnSavedValues") or _isForceToCheck:
            isClose=True
            for rowNo in range(self.rowCount()):
                if isClose==False:
                    break
                if self.isRowHidden(rowNo):
                    isClose=False
                    break
                for columnNo in range(len(self.tableColumns)):
                    if self.isColumnHidden(columnNo)==False:
                        if self.item(rowNo,columnNo)!=None:
                            if self.item(rowNo,columnNo).background()==MBrush(MColor(142,199,255)):
                                isClose=False
                                break
                        else:break
            if isClose==False:
                answer = Dialogs.ask(translate("Tables", "There Are Unsaved Values"),
                            translate("Tables", "Do you want to save these values?<br>If you click to Yes : Table will be saved without any other question or option.<br>If you click to No : Application will be closed without doing any process.<br>If you click to Cancel : Application won't be closed."),
                            True)
                if answer==Dialogs.Yes:
                    self.save()
                elif answer==Dialogs.Cancel:
                    return False
        return True
        
    def checkFileExtensions(self, _columnNo, _fileNameKeyOrDestinationColumnNo, _isCheckFile=False):
        destinationParameterType = "fileNameKey"
        if type(_fileNameKeyOrDestinationColumnNo)==type(0):
            destinationParameterType = "destinationColumnNo"
        isYesToAll, isNoToAll=False, False
        for rowNo in range(self.rowCount()):
            if _isCheckFile:
                if InputOutputs.isFile(self.currentTableContentValues[rowNo]["path"])==False:
                    continue
            if destinationParameterType == "fileNameKey":
                sFileExt = InputOutputs.getFileExtension(self.currentTableContentValues[rowNo][_fileNameKeyOrDestinationColumnNo])
                sFilePath = self.currentTableContentValues[rowNo]["path"]
            else:
                sFileExt = InputOutputs.getFileExtension(str(self.item(rowNo, _fileNameKeyOrDestinationColumnNo).text()))
                sFilePath = str(self.item(rowNo, _fileNameKeyOrDestinationColumnNo).text())
            cFileName = str(self.item(rowNo,_columnNo).text())
            if sFileExt!="":
                if InputOutputs.getFileExtension(cFileName)!=sFileExt:
                    if isYesToAll:
                        answer = Dialogs.Yes
                    elif isNoToAll:
                        answer = Dialogs.No
                    else:
                        answer = Dialogs.askSpecial(translate("Tables", "Incorrect File Extension"), 
                                str(translate("Tables", "\"%s\": the file extension is different from the source file extension.<br>Do you want to set the source file extension?<br><b>Source file : </b>\"%s\"")) % (cFileName, sFilePath), 
                                translate("Dialogs", "Yes"), 
                                translate("Dialogs", "No"), 
                                translate("Dialogs", "Yes To All"), 
                                translate("Dialogs", "No To All"))
                    if answer==translate("Dialogs", "Yes To All"):
                        isYesToAll=True
                        answer = Dialogs.Yes
                    elif answer==translate("Dialogs", "No To All"):
                        isNoToAll=True
                        answer = Dialogs.No
                    if answer==Dialogs.Yes or answer==translate("Dialogs", "Yes"):
                        self.item(rowNo,_columnNo).setText(trForUI(cFileName + "." + sFileExt))

    def askHiddenColumn(self, _columnNo, _isYesToAll=True):
        if _isYesToAll==False:
            self.isAskShowHiddenColumn = True
        if self.isAskShowHiddenColumn:
            if _isYesToAll==True:
                answer = Dialogs.askSpecial(translate("Tables", "Hidden Field"), 
                                str(translate("Tables", "\"%s\": you have hidden this field in the table.<br>Do you want to activate this field and perform the action?")) % (self.tableColumns[_columnNo]), 
                                translate("Dialogs", "Yes"), 
                                translate("Dialogs", "No"), 
                                translate("Dialogs", "Yes To All"))  
            else:
                answer = Dialogs.ask(translate("Tables", "Hidden Field"), 
                                str(translate("Tables", "\"%s\": you have hidden this field in the table.<br>Do you want to activate this field and perform the action?")) % (self.tableColumns[_columnNo]))   
            if answer==Dialogs.No or answer==translate("Dialogs", "No"):
                Dialogs.showError(translate("Tables", "Action Cancelled"), 
                                translate("Tables", "You have cancelled the action.<br>You can make the necessary changes and reperform the action."))
                return False
            elif answer==translate("Dialogs", "Yes To All"):
                self.isAskShowHiddenColumn=False
        self.mContextMenuColumnsActions[_columnNo].setChecked(True)
        self.refreshShowedAndHiddenColumns()
        return True
    
    def checkHiddenColumn(self, _columnNo, _isYesToAll=True):
        if self.isColumnHidden(_columnNo)==True:
            return self.askHiddenColumn(_columnNo, _isYesToAll)
        return True
        
    def exportValues(self, _actionType="return",_formatType="html", _extInfo="no"):
        import os
        info = ""
        if _formatType=="html":
            if _extInfo=="no":
                pass
            elif _extInfo=="title":
                info += " \n<h3>%s : </h3>" % (str(translate("Tables", "Table Contents")))
            info += " \n<table border=1> \n<tr> \n<td>*</td> \n"
            for columnNo in range(self.columnCount()):
                if self.isColumnHidden(columnNo)==False:
                    info +="<td><b>"
                    info +=str(self.tableColumns[columnNo])
                    info +="</b></td> \n"
            info +="</tr> \n"
            for rowNo in range(self.rowCount()):
                if self.isRowHidden(rowNo)==False:
                    info +=" \n<tr> \n<td>" + str (rowNo + 1) + "</td> \n"
                    for columnNo in range(self.columnCount()):
                        if self.isColumnHidden(columnNo)==False:
                            info +="<td>"
                            info +=str(str(self.item(rowNo,columnNo).text()))
                            info +="</td> \n"
                    info +="</tr> \n"
            info+="</table> \n"
        elif _formatType=="plainText":
            if _extInfo=="no":
                pass
            elif _extInfo=="title":
                info +=" %s : \n" % (str(translate("Tables", "Table Contents")))
            info += "*\t"
            for columnNo in range(self.columnCount()):
                if self.isColumnHidden(columnNo)==False:
                    info +=str(self.tableColumns[columnNo])
                    info +="\t"
            info +="\n"
            for rowNo in range(self.rowCount()):
                info += str(rowNo + 1)+"\t"
                if self.isRowHidden(rowNo)==False:
                    for columnNo in range(self.columnCount()):
                        if self.isColumnHidden(columnNo)==False:
                            info +=str(str(self.item(rowNo,columnNo).text()))
                            info +="\t"
                    info +="\n"
        if _actionType=="return":
            return info
        elif _actionType=="file":
            if _formatType=="html":
                if _extInfo!="no":
                    strHeader = ("<!DOCTYPE html PUBLIC \"-//W3C//DTD XHTML 1.0 Strict//EN\" \n"+
                        "\"http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd\"> \n"+
                        "<html xmlns=\"http://www.w3.org/1999/xhtml\" xml:lang=\"tr\" lang=\"tr\" dir=\"ltr\"> \n"+
                        "<head> \n<meta http-equiv=\"Content-Type\" content=\"text/html; charset=utf-8\" /> \n</head> \n<body> \n")
                    strFooter = " \n</body> \n</html>"
                    info = strHeader + info + strFooter
                formatTypeName = translate("Tables", "HTML")
                fileExt="html"
            elif _formatType=="plainText":
                formatTypeName = translate("Tables", "Plain Text")
                fileExt="txt"
            filePath = Dialogs.getSaveFileName(translate("Tables", "Save As"),
                                    InputOutputs.joinPath(Variables.userDirectoryPath, InputOutputs.getBaseName(self.currentDirectoryPath) + "." + fileExt), formatTypeName+" (*."+fileExt+")", 2)
            if filePath is not None:
                if _formatType=="html" and filePath[-5:]!=".html":
                    filePath += ".html"
                elif _formatType=="plainText" and filePath[-4:]!=".txt":
                    filePath += ".txt"
                InputOutputs.writeToFile(filePath, info)
                Dialogs.show(translate("Tables", "Table Exported"),
                            str(translate("Tables", "Table contents are exported to file: \"%s\".")) % Organizer.getLink(filePath))
        elif _actionType=="dialog":
            dDialog = MDialog(Universals.MainWindow)
            if isActivePyKDE4==True:
                dDialog.setButtons(MDialog.NoDefault)
            dDialog.setWindowTitle(translate("Tables", "Table Contents"))
            mainPanel = MWidget(dDialog)
            vblMain = MVBoxLayout(mainPanel)
            if _formatType=="html":
                QtWebKit = getMyObject("QtWebKit")
                wvWeb = QtWebKit.QWebView()
                wvWeb.setHtml(trForUI(info))
            elif _formatType=="plainText":
                wvWeb = MTextEdit()
                wvWeb.setPlainText(trForUI(info))
            pbtnClose = MPushButton(translate("Tables", "OK"))
            MObject.connect(pbtnClose, SIGNAL("clicked()"), dDialog.close)
            vblMain.addWidget(wvWeb)
            vblMain.addWidget(pbtnClose)
            if isActivePyKDE4==True:
                dDialog.setMainWidget(mainPanel)
            else:
                dDialog.setLayout(vblMain)
            dDialog.setMinimumWidth(600)
            dDialog.setMinimumHeight(400)
            dDialog.show()
        elif _actionType=="clipboard":
            MApplication.clipboard().setText(trForUI(info))
            

            
            
class MyTableWidgetItem(MTableWidgetItem):
    
    def __init__(self, _value):
        MTableWidgetItem.__init__(self, trForUI(_value))
        self.currentText = trForUI(_value)
        self.isReadOnly = False



