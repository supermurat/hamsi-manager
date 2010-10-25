# -*- coding: utf-8 -*-

import Variables
import MusicTable
import FileTable
import FolderTable
import SubFolderTable
import CoverTable
import FileManager
import Dialogs
import Universals
import InputOutputs
import Organizer
from MyObjects import *
import ReportBug

class Tables(MTableWidget):
    global refreshTable, refreshShowedAndHiddenColumns, clickedContextMenuColumns, checkHiddenColumn, isAskShowHiddenColumn, isChangeHiddenColumn, refreshForTableColumns, exportTableValues, askHiddenColumn
    isAskShowHiddenColumn = True
    def __init__(self, _parent):
        global refreshTable,layouts,widgets, table
        MTableWidget.__init__(self, _parent)
        table=self
        self.changedValueNumber = 0
        self.history = []
        self.future = []
        self.setAlternatingRowColors(True)
        self.setWordWrap(False)
        self.setVerticalScrollMode(self.ScrollPerPixel)
        self.setHorizontalScrollMode(self.ScrollPerPixel)
        MObject.connect(self,SIGNAL("cellClicked(int,int)"),self.tableCellClicked)
        MObject.connect(self,SIGNAL("itemChanged(QTableWidgetItem *)"),self.tableItemChanged)
        MObject.connect(self,SIGNAL("cellDoubleClicked(int,int)"),self.tableCellDoubleClicked)
        self.pbtnSave = MPushButton(translate("Tables", "Save"))
        self.pbtnSave.setObjectName("pbtnSave")
        self.pbtnSave.setIcon(MIcon("Images:save.png"))
        self.pbtnShowDetails = MPushButton(translate("Tables", "See Details"))
        self.tbCorrect = MToolButton()
        self.tbCorrect.setToolTip(translate("Tables", "Re Correct"))
        self.tbCorrect.setIcon(MIcon("Images:correct.png"))
        self.tbCorrect.setAutoRaise(True)
        self.tbIsRunOnDoubleClick = MToolButton()
        self.tbIsRunOnDoubleClick.setToolTip(translate("Tables", "Show Details Upon Double Click"))
        self.tbIsRunOnDoubleClick.setIcon(MIcon("Images:runOnDoubleClick.png"))
        self.tbIsRunOnDoubleClick.setCheckable(True)
        self.tbIsRunOnDoubleClick.setAutoRaise(True)
        self.isOpenDetailsOnNewWindow = MToolButton()
        self.isOpenDetailsOnNewWindow.setToolTip(translate("Tables", "Show Details In New Window"))
        self.isOpenDetailsOnNewWindow.setIcon(MIcon("Images:openDetailsOnNewWindow.png"))
        self.isOpenDetailsOnNewWindow.setCheckable(True)
        self.isOpenDetailsOnNewWindow.setAutoRaise(True)
        self.tbIsRunOnDoubleClick.setChecked(Universals.getBoolValue("isRunOnDoubleClick"))
        self.isOpenDetailsOnNewWindow.setChecked(Universals.getBoolValue("isOpenDetailsInNewWindow"))
        MObject.connect(self.pbtnShowDetails, SIGNAL("clicked()"), self.showDetails)
        self.actRefresh = MToolButton()
        self.actRefresh.setToolTip(translate("Tables", "Refresh"))
        self.actRefresh.setIcon(MIcon("Images:refresh.png"))
        self.actRefresh.setAutoRaise(True)
        MObject.connect(self.actRefresh, SIGNAL("clicked()"), refreshTable)
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
        MObject.connect(self.pbtnSave, SIGNAL("clicked()"), self.saveTable)
        MObject.connect(self.tbGoBack, SIGNAL("clicked()"), self.goBack)
        MObject.connect(self.tbGoForward, SIGNAL("clicked()"), self.goForward)
        MObject.connect(self.tbCreateHistoryPoint, SIGNAL("clicked()"), self.createHistoryPoint)
        MObject.connect(self.tbCorrect, SIGNAL("clicked()"), self.correct)
        _parent.MainLayout.addWidget(self, 10)
        self.mContextMenu = MMenu(self)
        self.hblBox = MHBoxLayout()
        if Universals.tableType==0:
            FolderTable.FolderTable(self)
        elif Universals.tableType==1:
            FileTable.FileTable(self)
        elif Universals.tableType==2:
            MusicTable.MusicTable(self)
        elif Universals.tableType==3:
            SubFolderTable.SubFolderTable(self)
        elif Universals.tableType==4:
            CoverTable.CoverTable(self)
            Universals.isShowOldValues = False
        self.hiddenTableColumns = Universals.getListFromStrint(Universals.MySettings[self.hiddenTableColumnsSettingKey])
        _parent.MainLayout.addLayout(self.hblBox)
        self.mContextMenuColumns = MMenu()
        self.mContextMenuColumns.setTitle(translate("Tables", "Show Fields"))
        self.mContextMenuOpenWith = MMenu()
        self.mContextMenuOpenWith.setTitle(translate("Tables", "Open With"))
        self.clickedContextMenuColumns = []
        refreshForTableColumns()
        self.mContextMenuActionNames = [translate("Tables", "Cut"),
                            translate("Tables", "Copy"),
                            translate("Tables", "Paste"),
                            translate("Tables", "Replace"), 
                            translate("Tables", "Remove From System")]
        for actName in self.mContextMenuActionNames:
            self.mContextMenu.addAction(actName).setObjectName(actName)
        self.mContextMenuOpenWithNames = [translate("Tables", "File Manager"),
                            translate("Tables", "Default Application"),
                            translate("Tables", "Konsole")]
        for actName in self.mContextMenuOpenWithNames:
            self.mContextMenuOpenWith.addAction(actName).setObjectName(actName)
        self.mContextMenu.addMenu(self.mContextMenuColumns)
        self.mContextMenu.addMenu(self.mContextMenuOpenWith)
        self.checkActionsStates()
    
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
            if self.currentRow()!=-1:
                if Universals.isShowOldValues==True:
                    rowNo = self.currentRow()/2
                else:
                    rowNo = self.currentRow()
                filePath = InputOutputs.IA.currentDirectoryPath+"/"+self.fileDetails[rowNo][1]
                isOpenedDetails = False
                if InputOutputs.IA.isExist(filePath):
                    isImage = False
                    isMusic = False
                    for fileExt in Universals.getListFromStrint(Universals.MySettings["imageExtensions"]):
                        if InputOutputs.IA.checkExtension(filePath, fileExt):
                            isImage = True
                            break
                    if isImage==False:
                        for fileExt in Universals.getListFromStrint(Universals.MySettings["musicExtensions"]):
                            if InputOutputs.IA.checkExtension(filePath, fileExt):
                                isMusic = True
                                break
                    if isImage:
                        from Details import ImageDetails
                        ImageDetails.ImageDetails(filePath)
                        isOpenedDetails = True
                    elif isMusic:
                        from Details import MusicDetails
                        MusicDetails.MusicDetails(filePath)
                        isOpenedDetails = True
                if isOpenedDetails==False:
                    self.subShowDetails(self, rowNo, self.currentColumn())
        except:
            error = ReportBug.ReportBug()
            error.show()
    
    def correct(self):
        try:
            self.correctSubTable(self)
        except:
            error = ReportBug.ReportBug()
            error.show()
    
    def goBack(self):
        self.future.append(self.createHistoryPoint(True))
        self.goActionPoint(self.history.pop())
        self.checkActionsStates()
        
    def goForward(self):
        self.history.append(self.createHistoryPoint(True))
        self.goActionPoint(self.future.pop())
        self.checkActionsStates()
        
    def createHistoryPoint(self, _isReturn=False):
        nokta=[]
        for rowNo in range(self.rowCount()):
            nokta.append([])
            for columnNo in range(self.columnCount()):
                nokta[-1].append(self.item(rowNo, columnNo).text())
            nokta[-1].append(self.isRowHidden(rowNo))
        if _isReturn==False:
            self.future = []
            self.history.append(nokta)
            self.checkActionsStates()
        else:
            return nokta
    
    def goActionPoint(self, _actionPoint):
        for rowNo, row in enumerate(_actionPoint):
            for columnNo, column in enumerate(row[:-1]):
                self.item(rowNo, columnNo).setText(column)
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
            
    def contextMenuEvent(self,_event):
        try:
            if self.currentItem()!=None:
                self.mContextMenu.setGeometry(_event.globalX(),_event.globalY(),1,1)
                selectedItem = self.mContextMenu.exec_()
                if selectedItem!=None:
                    if selectedItem.objectName()==self.mContextMenuActionNames[0]:
                        self.createHistoryPoint()
                        MApplication.clipboard().setText(self.currentItem().text())
                        self.currentItem().setText("")
                    elif selectedItem.objectName()==self.mContextMenuActionNames[1]:
                        MApplication.clipboard().setText(self.currentItem().text())
                    elif selectedItem.objectName()==self.mContextMenuActionNames[2]:
                        self.createHistoryPoint()
                        self.currentItem().setText(MApplication.clipboard().text())
                    elif selectedItem.objectName()==self.mContextMenuActionNames[3]:
                        self.editItem(self.currentItem())
                    elif selectedItem.objectName()==self.mContextMenuActionNames[4]:
                        self.createHistoryPoint()
                        for rowNo in self.getSelectedRows():
                            if Universals.isShowOldValues==True:
                                if float(rowNo)/float(2)==rowNo/2:
                                    self.hideRow(rowNo)
                                    self.hideRow(rowNo+1)
                                else:
                                    self.hideRow(rowNo-1)
                                    self.hideRow(rowNo)
                            else:
                                self.hideRow(rowNo)
                    elif selectedItem.objectName()==self.mContextMenuOpenWithNames[0]:
                        import Execute
                        Execute.open(InputOutputs.IA.getRealDirName(InputOutputs.IA.currentDirectoryPath + "/" + table.fileDetails[self.currentItem().row()][1]))
                    elif selectedItem.objectName()==self.mContextMenuOpenWithNames[1]:
                        import Execute
                        Execute.open(InputOutputs.IA.currentDirectoryPath + "/" + table.fileDetails[self.currentItem().row()][1])
                    elif selectedItem.objectName()==self.mContextMenuOpenWithNames[2]:
                        import Execute
                        Execute.execute("konsole --workdir " + Execute.correctForConsole(InputOutputs.IA.getRealDirName(InputOutputs.IA.currentDirectoryPath + "/" + table.fileDetails[self.currentItem().row()][1])))
        except:
            error = ReportBug.ReportBug()
            error.show()
    
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
    
    def clickedContextMenuColumns(_value):
        try:
            refreshShowedAndHiddenColumns()
        except:
            error = ReportBug.ReportBug()
            error.show()
    
    def refreshShowedAndHiddenColumns():
        table.hiddenTableColumns = []
        for x, act in enumerate(table.mContextMenuColumnsActions):
            if act.isChecked()==False:
                table.hiddenTableColumns.append(str(x))
        for c in range(len(table.tableColumns)):
            if table.hiddenTableColumns.count(str(c))>0:
                table.hideColumn(c)
            else:
                table.showColumn(c)
    
    def tableCellClicked(self,_row,_column):
        try:
            self.subTableCellClicked(self, _row, _column)
        except:
            error = ReportBug.ReportBug()
            error.show()
    
    def tableCellDoubleClicked(self,_row,_column):
        try:
            self.subTableCellDoubleClicked(self, _row, _column)
        except:
            error = ReportBug.ReportBug()
            error.show()
    
    def refreshForTableColumns():
        table.mContextMenuColumns.clear()
        table.refreshSubTableColumns(table)
        table.mContextMenuColumnsActions = []
        for columnName in table.tableColumns:
            table.mContextMenuColumnsActions.append(MAction(columnName,table.mContextMenuColumns))
        for key,act in enumerate(table.mContextMenuColumnsActions):
            act.setCheckable(True)
            if table.hiddenTableColumns.count(str(key))==0:
                act.setChecked(True)
            table.mContextMenuColumns.addAction(act)
            MObject.connect(act,SIGNAL("triggered(bool)"), clickedContextMenuColumns)
        refreshShowedAndHiddenColumns()
        
    def refreshTable(_path = ""):
        global isShowChanges, isAskShowHiddenColumn
        isAskShowHiddenColumn = True
        if InputOutputs.IA.isDir(_path)==False:
            _path = InputOutputs.IA.currentDirectoryPath
        isShowChanges=False
        table.clear()
        table.setColumnCount(len(table.tableColumns))
        table.setHorizontalHeaderLabels(table.tableColumns)
        columnWidth = (Universals.MainWindow.CentralWidget.width()-90)/len(table.tableColumns)
        if columnWidth>110:
            for x in range(len(table.tableColumns)):
                table.setColumnWidth(x,columnWidth)
        import MyThread
        myProcs = MyThread.MyThread(table.refreshSubTable, table.continueRefreshTable, (table, _path))
        myProcs.run()

    def continueRefreshTable(self, _returned=None):
        global isShowChanges
        isShowChanges=True
        for rowNo in range(table.rowCount()):
            if table.isRowHidden(rowNo):
                table.showRow(rowNo)
        refreshShowedAndHiddenColumns()
        
    def tableItemChanged(self, _item):
        global isShowChanges
        if isShowChanges==True:
            isShowChanges = False
            if _item.text()!=_item.statusTip():
                _item.setToolTip(_item.statusTip())
                _item.setStatusTip(_item.text())
                _item.setBackground(MBrush(MColor(142,199,255)))
            isShowChanges = True
            
                
    def saveTable(self):
        try:
            import Records
            Records.setTitle(Universals.tableTypesNames[Universals.tableType])
            if Universals.tableType!=4:
                InputOutputs.IA.activateSmartCheckIcon()
            if Universals.getBoolValue("isClearEmptyDirectoriesWhenSave"):
                if InputOutputs.IA.clearEmptyDirectories(InputOutputs.IA.currentDirectoryPath, True, True, Universals.getBoolValue("isAutoCleanSubFolderWhenSave")):
                    Universals.MainWindow.FileManager.makeRefresh(InputOutputs.IA.getDirName(InputOutputs.IA.currentDirectoryPath))
                    return True
            import MyThread
            myProcs = MyThread.MyThread(self.saveSubTable, self.continueSaveTable, (self))
            myProcs.run()
        except:
            error = ReportBug.ReportBug()
            error.show()      
        
    def continueSaveTable(self, _returned=None):
        import Records
        newCurrentDirectoryPath = _returned
        if Universals.tableType!=4:
            if Universals.getBoolValue("isAutoMakeIconToDirectoryWhenSave"):
                InputOutputs.IA.checkIcon(InputOutputs.IA.currentDirectoryPath)
        InputOutputs.IA.complateSmartCheckIcon()
        Records.saveAllRecords()
        if self.changedValueNumber==0:
            Dialogs.show(translate("Tables", "Did Not Change Any Things"), 
                         translate("Tables", "Did not change any things in this table.Please check the criteria you select."))
        else:
            if Universals.getBoolValue("isShowTransactionDetails"):
                Dialogs.show(translate("Tables", "Transaction Details"), 
                             str(translate("Tables", "%s value(s) changed.")) % self.changedValueNumber)
        if newCurrentDirectoryPath!=None and newCurrentDirectoryPath!=InputOutputs.IA.currentDirectoryPath:
            Universals.MainWindow.FileManager.makeRefresh(newCurrentDirectoryPath)
        else:
            Universals.MainWindow.FileManager.makeRefresh("", False)
        
    def checkUnSavedTableValues(self):
        isClose=True
        for rowNo in range(self.rowCount()):
            if isClose==False:
                break
            if self.isRowHidden(rowNo):
                isClose=False
                break
            for columnNo in range(len(table.tableColumns)):
                if self.isColumnHidden(columnNo)==False:
                    if self.item(rowNo,columnNo)!=None:
                        if self.item(rowNo,columnNo).background()==MBrush(MColor(142,199,255)):
                            isClose=False
                            break
                    else:break
        if isClose==False:
            answer = Dialogs.ask(translate("Tables", "There Are Unsaved Information"),
                        translate("Tables", "Do you want to save these information?"),
                        True, "There Are Unsaved Information")
            if answer==Dialogs.Yes:
                self.saveTable()
            elif answer==Dialogs.Cancel:
                return False
        return True

    def askHiddenColumn(_columnNo, _isYesToAll=True):
        global isChangeHiddenColumn,isAskShowHiddenColumn
        if _isYesToAll==False:
            isAskShowHiddenColumn = True
        if isAskShowHiddenColumn:
            if _isYesToAll==True:
                answer = Dialogs.askSpecial(translate("Tables", "Hidden Field"), 
                                str(translate("Tables", "\"%s\": you have hidden this field in the table.<br>Do you want to activate this field and perform the action?")) % (table.tableColumns[_columnNo]), 
                                translate("Tables", "Yes"), 
                                translate("Tables", "No"), 
                                translate("Tables", "Yes To All"))  
            else:
                answer = Dialogs.ask(translate("Tables", "Hidden Field"), 
                                str(translate("Tables", "\"%s\": you have hidden this field in the table.<br>Do you want to activate this field and perform the action?")) % (table.tableColumns[_columnNo]))   
            if answer==Dialogs.No or answer==translate("Tables", "No"):
                isChangeHiddenColumn=False
                Dialogs.showError(translate("Tables", "Action Cancelled"), 
                                translate("Tables", "You have cancelled the action.<br>You can make the necessary changes and reperform the action."))
                return False
            elif answer==translate("Tables", "Yes To All"):
                isAskShowHiddenColumn=False
        table.mContextMenuColumnsActions[_columnNo].setChecked(True)
        refreshShowedAndHiddenColumns()
        return True
    
    def checkHiddenColumn(_columnNo, _isYesToAll=True):
        if table.isColumnHidden(_columnNo)==True:
            return askHiddenColumn(_columnNo, _isYesToAll)
        return True
        
    def exportTableValues(_actionType="return",_formatType="html", _extInfo="no"):
        import os
        info = ""
        if _formatType=="html":
            if _extInfo=="no":
                pass
            elif _extInfo=="title":
                info += " \n<h3>%s : </h3>" % (str(translate("Tables", "Table Contents")))
            info += " \n<table border=1> \n<tr> \n<td>*</td> \n"
            for columnNo in range(table.columnCount()):
                if table.isColumnHidden(columnNo)==False:
                    info +="<td><b>"
                    info +=str(table.tableColumns[columnNo])
                    info +="</b></td> \n"
            info +="</tr> \n"
            for rowNo in range(table.rowCount()):
                if table.isRowHidden(rowNo)==False:
                    info +=" \n<tr> \n<td>" + str (rowNo) + "</td> \n"
                    for columnNo in range(table.columnCount()):
                        if table.isColumnHidden(columnNo)==False:
                            info +="<td>"
                            info +=str(unicode(table.item(rowNo,columnNo).text(),"utf-8"))
                            info +="</td> \n"
                    info +="</tr> \n"
            info+="</table> \n"
        elif _formatType=="plainText":
            if _extInfo=="no":
                pass
            elif _extInfo=="title":
                info +=" %s : \n" % (str(translate("Tables", "Table Contents")))
            info += "*\t"
            for columnNo in range(table.columnCount()):
                if table.isColumnHidden(columnNo)==False:
                    info +=str(table.tableColumns[columnNo])
                    info +="\t"
            info +="\n"
            for rowNo in range(table.rowCount()):
                info += str(rowNo)+"\t"
                if table.isRowHidden(rowNo)==False:
                    for columnNo in range(table.columnCount()):
                        if table.isColumnHidden(columnNo)==False:
                            info +=str(unicode(table.item(rowNo,columnNo).text(),"utf-8"))
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
            filePath = MFileDialog.getSaveFileName(table.parent(),translate("Tables", "Save As"),
                                    Variables.userDirectoryPath.decode("utf-8"),formatTypeName+(" (*."+fileExt).decode("utf-8")+")")
            if filePath!="":
                filePath = unicode(filePath, "utf-8")
                if _formatType=="html" and filePath[-5:]!=".html":
                    filePath += ".html"
                elif _formatType=="plainText" and filePath[-4:]!=".txt":
                    filePath += ".txt"
                InputOutputs.IA.writeToFile(filePath, info)
                Dialogs.show(translate("Tables", "Table Exported"),
                            str(translate("Tables", "Table contents are exported to file: \"%s\".")) % Organizer.getLink(filePath))
        elif _actionType=="dialog":
            dDialog = MDialog(Universals.MainWindow)
            if Universals.isActivePyKDE4==True:
                dDialog.setButtons(MDialog.None)
            dDialog.setWindowTitle(translate("Tables", "Table Contents"))
            mainPanel = MWidget(dDialog)
            vblMain = MVBoxLayout(mainPanel)
            if _formatType=="html":
                QtWebKit = getMyObject("QtWebKit")
                wvWeb = QtWebKit.QWebView()
                wvWeb.setHtml(info.decode("utf-8"))
            elif _formatType=="plainText":
                wvWeb = MTextEdit()
                wvWeb.setPlainText(info.decode("utf-8"))
            pbtnClose = MPushButton(translate("Tables", "OK"))
            MObject.connect(pbtnClose, SIGNAL("clicked()"), dDialog.close)
            vblMain.addWidget(wvWeb)
            vblMain.addWidget(pbtnClose)
            if Universals.isActivePyKDE4==True:
                dDialog.setMainWidget(mainPanel)
            else:
                dDialog.setLayout(vblMain)
            dDialog.setMinimumWidth(600)
            dDialog.setMinimumHeight(400)
            dDialog.show()
        elif _actionType=="clipboard":
            MApplication.clipboard().setText(info.decode("utf-8"))
            
