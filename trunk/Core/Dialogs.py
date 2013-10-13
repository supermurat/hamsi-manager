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
from Core.MyObjects import *
from Core import Universals
from datetime import datetime

class Dialogs():
    global show, showError, ask, askSpecial, showState, Ok, Cancel, Yes, No, Continue, getItem, sleep, getText, getSaveFileName, getOpenFileName, getOpenFileNames, getExistingDirectory, lastInfoTime
    Ok, Cancel, Yes, No, Continue = 1, 2, 3, 4, 5
    lastInfoTime = (datetime.now().microsecond / 60000)
    
    def show(_title="Hamsi Manager", _detail="", _btnString=translate("Dialogs", "OK")):
        MApplication.processEvents()
        if _detail=="": 
            _detail = _title
            _title = "Hamsi Manager"
        from Core import Organizer
        if len(Universals.MySettings)>0 and Universals.isActivePyKDE4==True:
            MMessageBox.information(Universals.activeWindow(), trForUI("<b>" + str(_title) + " : </b><br>" + str(_detail)), trForUI(str(_title)+"!.."))
        else:
            MMessageBox.information(Universals.activeWindow(), trForUI(str(_title)+"!.."), trForUI("<b>" + str(_title) + " : </b><br>" + str(_detail)),_btnString)
        return True
        
    def showError(_title="Hamsi Manager", _detail="", _btnString=translate("Dialogs", "OK")):
        MApplication.processEvents()
        if _detail=="": 
            _detail = _title
            _title = "Hamsi Manager"
        from Core import Organizer
        if len(Universals.MySettings)>0 and Universals.isActivePyKDE4==True:
            MMessageBox.error(Universals.activeWindow(), trForUI("<b>" + str(_title) + " : </b><br>" + str(_detail)), trForUI(str(_title)+"!.."))
        else:
            MMessageBox.critical(Universals.activeWindow(),trForUI(str(_title)+"!.."),trForUI("<b>" + str(_title) + " : </b><br>" + str(_detail)),_btnString)
        return True
     
    def ask(_title="Hamsi Manager", _detail="", _isShowCancel=False, _showAgainKeyName=""):
        MApplication.processEvents()
        if _detail=="": 
            _detail = _title
            _title = "Hamsi Manager"
        from Core import Organizer
        if len(Universals.MySettings)>0 and Universals.isActivePyKDE4==True:
            if _isShowCancel:
                if _showAgainKeyName!="":
                    return MMessageBox.messageBox(Universals.activeWindow(), 
                            MMessageBox.QuestionYesNoCancel, 
                            trForUI("<b>" + str(_title) + " : </b><br>" + str(_detail)), 
                            trForUI(_title), 
                            MStandardGuiItem.yes(), MStandardGuiItem.no(), MStandardGuiItem.cancel(), 
                            trForUI(_showAgainKeyName), 
                            MMessageBox.AllowLink )
                else:
                    return MMessageBox.questionYesNoCancel(Universals.activeWindow(), 
                            trForUI("<b>" + str(_title) + " : </b><br>" + str(_detail)), 
                            trForUI(_title), 
                            MStandardGuiItem.yes(), MStandardGuiItem.no(), MStandardGuiItem.cancel(), "", 
                            MMessageBox.AllowLink )
            else:
                if _showAgainKeyName!="":
                    return MMessageBox.messageBox(Universals.activeWindow(), 
                            MMessageBox.QuestionYesNo, 
                            trForUI("<b>" + str(_title) + " : </b><br>" + str(_detail)), 
                            trForUI(_title), 
                            MStandardGuiItem.yes(), MStandardGuiItem.no(), MStandardGuiItem.cancel(), 
                            trForUI(_showAgainKeyName), 
                            MMessageBox.AllowLink )
                else:
                    return MMessageBox.questionYesNo(Universals.activeWindow(), 
                            trForUI("<b>" + str(_title) + " : </b><br>" + str(_detail)), 
                            trForUI(_title), 
                            MStandardGuiItem.yes(), MStandardGuiItem.no(), "", 
                            MMessageBox.AllowLink )
        else:
            if _isShowCancel:
                try:mboxDialog = MMessageBox(Universals.activeWindow())
                except:mboxDialog = MMessageBox(None)
                mboxDialog.setWindowTitle(trForUI(_title))
                mboxDialog.setText(trForUI("<b>" + str(_title) + " : </b><br>" + str(_detail)))
                mboxDialog.setStandardButtons(MMessageBox.Yes | MMessageBox.No | MMessageBox.Cancel)
                pressedButtonNo = mboxDialog.exec_()
            else:
                try:mboxDialog = MMessageBox(Universals.activeWindow())
                except:mboxDialog = MMessageBox(None)
                mboxDialog.setWindowTitle(trForUI(_title))
                mboxDialog.setText(trForUI("<b>" + str(_title) + " : </b><br>" + str(_detail)))
                mboxDialog.setStandardButtons(MMessageBox.Yes | MMessageBox.No)
                pressedButtonNo = mboxDialog.exec_()
            if pressedButtonNo==16384 : return Yes
            elif pressedButtonNo==65536 : return No
            elif pressedButtonNo==4194304 : return Cancel
            else : return Cancel
            
            
    def askSpecial(_title="Hamsi Manager", _detail="", _btnString=translate("Dialogs", "Yes"), _btnString1=translate("Dialogs", "No"), _btnString2=translate("Dialogs", "Cancel"), _btnString3=None):
        from Core import Organizer
        MApplication.processEvents()
        MyMessageBox = MMessageBox
        if len(Universals.MySettings)>0 and Universals.isActivePyKDE4==True:
            MyMessageBox = QMessageBox
        try:mboxDialog = MyMessageBox(Universals.activeWindow())
        except:mboxDialog = MyMessageBox(None)
        mboxDialog.setWindowTitle(trForUI(_title))
        mboxDialog.setText(trForUI("<b>" + str(_title) + " : </b><br>" + str(_detail)))
        btn = mboxDialog.addButton(_btnString, MyMessageBox.ActionRole)
        if _btnString2!=None:
            btn2 = mboxDialog.addButton(_btnString2, MyMessageBox.ActionRole)
        btn1 = mboxDialog.addButton(_btnString1,MyMessageBox.ActionRole)
        if _btnString3!=None:
            btn3 = mboxDialog.addButton(_btnString3, MyMessageBox.ActionRole)
        else:
            btn3 = None
        mboxDialog.exec_()
        if mboxDialog.clickedButton() == btn:
            return _btnString
        elif mboxDialog.clickedButton() == btn1:
            return _btnString1
        elif mboxDialog.clickedButton() == btn2:
            return _btnString2
        elif mboxDialog.clickedButton() == btn3:
            return _btnString3
        else:
            if btn3!=None:
                return _btnString3
            elif btn2!=None:
                return _btnString2
            elif btn1!=None:
                return _btnString1
            elif btn!=None:
                return _btnString
                
    def showState(_title, _value=0, _maxValue=100, _isShowCancel=False, _connectToCancel=None, _isCheckLastShowTime=True):
        global lastInfoTime
        if _isCheckLastShowTime:
            if lastInfoTime == (datetime.now().microsecond / 60000) and _maxValue != _value:
                return None
            else:
                lastInfoTime = (datetime.now().microsecond / 60000)
        if Universals.windowMode==Variables.windowModeKeys[1] and Universals.isCanBeShowOnMainWindow:
            return Universals.MainWindow.StatusBar.showState(_title, _value, _maxValue, _isShowCancel, _connectToCancel)
        MApplication.processEvents()
        if Universals.MainWindow.StateDialog==None:
            Universals.MainWindow.StateDialogStateBar = MProgressBar()
            HBoxs=[]
            if Universals.getBoolValue("isMinimumWindowMode") and Universals.isCanBeShowOnMainWindow:
                if Universals.MainWindow.isLockedMainForm==False:
                    Universals.MainWindow.lockForm()
                Universals.MainWindow.StateDialog = MDockWidget(translate("Dialogs", "Progress Bar"))
                Universals.MainWindow.StateDialog.setObjectName(translate("Dialogs", "Progress Bar"))
                pnlState2 = MWidget(Universals.MainWindow.StateDialog)
                Universals.MainWindow.StateDialogTitle = MLabel()
                HBoxs.append(MHBoxLayout(pnlState2))
                HBoxs[0].addWidget(Universals.MainWindow.StateDialogTitle) 
                HBoxs[0].addWidget(Universals.MainWindow.StateDialogStateBar) 
                Universals.MainWindow.StateDialog.setWidget(pnlState2)
                Universals.MainWindow.StateDialog.setAllowedAreas(Mt.AllDockWidgetAreas)
                Universals.MainWindow.StateDialog.setFeatures(MDockWidget.AllDockWidgetFeatures)
                Universals.MainWindow.addDockWidget(Mt.TopDockWidgetArea, Universals.MainWindow.StateDialog)
                Universals.MainWindow.StateDialog.setMaximumHeight(60)
            else:
                Universals.MainWindow.StateDialog = MDialog(Universals.MainWindow)
                if len(Universals.MySettings)>0 and Universals.isActivePyKDE4==True:
                    Universals.MainWindow.StateDialog.setButtons(MDialog.NoDefault)
                Universals.MainWindow.StateDialog.setModal(True)
                Universals.MainWindow.StateDialog.setMinimumWidth(500) 
                pnlMain = MWidget(Universals.MainWindow.StateDialog)
                HBoxs.append(MHBoxLayout(pnlMain))
                HBoxs[0].addWidget(Universals.MainWindow.StateDialogStateBar)
                if len(Universals.MySettings)>0 and Universals.isActivePyKDE4==True:
                    Universals.MainWindow.StateDialog.setMainWidget(pnlMain)
                else:
                    Universals.MainWindow.StateDialog.setLayout(HBoxs[0])
                Universals.MainWindow.StateDialog.show()
            if _isShowCancel:
                pbtnCancel = MPushButton(translate("Dialogs", "Cancel"), Universals.MainWindow.StateDialog)
                if _connectToCancel==None:
                    MObject.connect(pbtnCancel, SIGNAL("clicked()"), Universals.cancelThreadAction)
                else:
                    MObject.connect(pbtnCancel, SIGNAL("clicked()"), _connectToCancel)
                HBoxs[0].addWidget(pbtnCancel) 
        Universals.MainWindow.StateDialogStateBar.setRange(0, _maxValue)
        Universals.MainWindow.StateDialogStateBar.setValue(_value)
        if Universals.getBoolValue("isMinimumWindowMode") and Universals.isCanBeShowOnMainWindow:
            Universals.MainWindow.StateDialog.setVisible(True)
            Universals.MainWindow.StateDialogTitle.setText(_title+" ( "+str(_value)+" / "+str(_maxValue)+" )")
        else:
            Universals.MainWindow.StateDialog.open()
            Universals.MainWindow.StateDialog.setModal(True)
            Universals.MainWindow.StateDialog.setWindowTitle(_title+" ( "+str(_value)+" / "+str(_maxValue)+" )")
        if _value==_maxValue:
            if Universals.getBoolValue("isMinimumWindowMode") and Universals.isCanBeShowOnMainWindow:
                if Universals.MainWindow.isLockedMainForm:
                    Universals.MainWindow.unlockForm()
                Universals.MainWindow.StateDialog.setVisible(False)
                Universals.MainWindow.removeDockWidget(Universals.MainWindow.StateDialog)
            else:
                Universals.MainWindow.StateDialog.setModal(False)
                Universals.MainWindow.StateDialog.close()
            Universals.MainWindow.StateDialog = None
    
    def sleep(_title, _value=0, _isShowCancel=False):
        import time
        maxTime = _value*4
        step = 0
        while step<=maxTime:
            showState(_title, step, maxTime, _isShowCancel)
            step += 1
            time.sleep(0.25)
            
    def getItem(_title="Hamsi Cover", _detail="", _itemList=[""], _currentItem=0):
        if _detail=="": 
            _detail = _title
            _title = "Hamsi Cover"
        from Core import Organizer
        if len(Universals.MySettings)>0 and Universals.isActivePyKDE4==True:
            selectedValue, isSelected = MInputDialog.getItem(trForUI(str(_title)+"!.."), trForUI(str(_detail)), [trForUI(str(x)) for x in _itemList], _currentItem, False)
        else:
            selectedValue, isSelected = MInputDialog.getItem(Universals.activeWindow(), trForUI(str(_title)+"!.."), trForUI(str(_detail)), [trForUI(str(x)) for x in _itemList], _currentItem, False)
        if isSelected==False:
            return None
        return str(selectedValue)
    
    def getText(_title="Hamsi Cover", _detail="", _default=""):
        if _detail=="": 
            _detail = _title
            _title = "Hamsi Cover"
        from Core import Organizer
        if len(Universals.MySettings)>0 and Universals.isActivePyKDE4==True:
            selectedValue, isSelected = MInputDialog.getText(trForUI(str(_title)+"!.."), trForUI(str(_detail)), trForUI(_default))
        else:
            selectedValue, isSelected = MInputDialog.getText(Universals.activeWindow(), trForUI(str(_title)+"!.."), trForUI(str(_detail)), MLineEdit.Normal, trForUI(_default))
        if isSelected==False:
            return None
        return str(selectedValue)
        
    def getSaveFileName(_caption, _directory, _filter=None, _isUseLastPathKeyType=1, _lastPathKey=None):
        if _filter is None:
            import InputOutputs
            if InputOutputs.isFile(_directory):
                fileExt = InputOutputs.getFileExtension(_directory)
                if fileExt != "":
                    _filter = "*.%s (*.%s)" % (fileExt,fileExt)
                else:
                    _filter = "*.* (*.*)"
            else:
                _filter = "*.* (*.*)"
        pathKey = Universals.getLastPathKey(_caption, _directory, _filter, _isUseLastPathKeyType, _lastPathKey)
        if pathKey is not None: _directory = Universals.getLastPathByEvent(pathKey, _directory)
        filePath = QFileDialog.getSaveFileName(Universals.activeWindow(), trForUI(_caption),
                                    trForUI(_directory), trForUI(_filter))
        if filePath=="":
            return None
        if pathKey is not None: Universals.setLastPathByEvent(pathKey, str(filePath))
        return str(filePath)
        
    def getOpenFileName(_caption, _directory, _filter, _isUseLastPathKeyType=1, _lastPathKey=None):
        pathKey = Universals.getLastPathKey(_caption, _directory, _filter, _isUseLastPathKeyType, _lastPathKey)
        if pathKey is not None: _directory = Universals.getLastPathByEvent(pathKey, _directory)
        filePath = QFileDialog.getOpenFileName(Universals.activeWindow(), trForUI(_caption),
                                    trForUI(_directory), trForUI(_filter))
        if filePath=="":
            return None
        if pathKey is not None: Universals.setLastPathByEvent(pathKey, str(filePath))
        return str(filePath)
        
    def getOpenFileNames(_caption, _directory, _filter, _isUseLastPathKeyType=1, _lastPathKey=None):
        pathKey = Universals.getLastPathKey(_caption, _directory, _filter, _isUseLastPathKeyType, _lastPathKey)
        if pathKey is not None: _directory = Universals.getLastPathByEvent(pathKey, _directory)
        filePaths = QFileDialog.getOpenFileNames(Universals.activeWindow(), trForUI(_caption),
                                    trForUI(_directory), trForUI(_filter))
        if filePaths==[]:
            return None
        if pathKey is not None: Universals.setLastPathByEvent(pathKey, str(filePath))
        return list(filePaths)
        
    def getExistingDirectory(_caption, _directory, _isUseLastPathKeyType=1, _lastPathKey=None):
        pathKey = Universals.getLastPathKey(_caption, _directory, "", _isUseLastPathKeyType, _lastPathKey)
        if pathKey is not None: _directory = Universals.getLastPathByEvent(pathKey, _directory)
        filePath = QFileDialog.getExistingDirectory(Universals.activeWindow(), trForUI(_caption),
                                    trForUI(_directory))
        if filePath=="":
            return None
        if pathKey is not None: Universals.setLastPathByEvent(pathKey, str(filePath))
        return str(filePath)
        
class MyStateDialog(MDialog):
    
    def __init__(self, _title="", _isShowCancel=False, _connectToCancel=None, _isCheckLastShowTime=True):
        MDialog.__init__(self, Universals.MainWindow)
        if len(Universals.MySettings)>0 and Universals.isActivePyKDE4==True:
            self.setButtons(MDialog.NoDefault)
        self.title = _title
        self.isShowCancel = _isShowCancel
        self.connectToCancel = _connectToCancel
        self.isCheckLastShowTime = _isCheckLastShowTime
        self.connect(self, SIGNAL("setState"), self.setState)
        
    def setTitle(self, _title):
        self.title = _title
    
    def setState(self, _value=0, _maxValue=100):
        showState(self.title, _value, _maxValue, self.isShowCancel, self.connectToCancel, self.isCheckLastShowTime)
        
        
        
        
        
        
        
        
        
