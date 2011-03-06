## This file is part of HamsiManager.
## 
## Copyright (c) 2010 Murat Demir <mopened@gmail.com>      
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


import Variables
from MyObjects import *
import Universals

class Dialogs():
    global show, showError, ask, askSpecial, showState, pnlState, prgbState, lblState, Ok, Cancel, Yes, No, Continue, select, pbtnCancel, sleep
    pnlState, prgbState, lblState, pbtnCancel = None, None, None, None
    Ok, Cancel, Yes, No, Continue = 1, 2, 3, 4, 5
    
    def show(_title="Hamsi Manager", _detail="", _btnString=translate("Dialogs", "OK")):
        MApplication.processEvents()
        if _detail=="": 
            _detail = _title
            _title = "Hamsi Manager"
        import Organizer
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
        import Organizer
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
        import Organizer
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
        import Organizer
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
                
    def showState(_title, _value=0, _maxValue=100, _isShowCancel=False):
        if Universals.windowMode==Variables.windowModeKeys[1] and Universals.isCanBeShowOnMainWindow:
            return Universals.MainWindow.StatusBar.showState(_title, _value, _maxValue, _isShowCancel)
        MApplication.processEvents()
        global pnlState, prgbState, lblState, pbtnCancel
        if pnlState==None:
            prgbState = MProgressBar()
            pbtnCancel = MPushButton(translate("Dialogs", "Cancel"))
            pbtnCancel.setVisible(False)
            MObject.connect(pbtnCancel, SIGNAL("clicked()"), Universals.cancelThreadAction)
            HBoxs=[]
            if Universals.getBoolValue("isMinimumWindowMode") and Universals.isCanBeShowOnMainWindow:
                Universals.MainWindow.lockForm()
                pnlState = MDockWidget(translate("Dialogs", "Progress Bar"))
                pnlState.setObjectName(translate("Dialogs", "Progress Bar"))
                pnlState2 = MWidget(pnlState)
                lblState = MLabel()
                HBoxs.append(MHBoxLayout(pnlState2))
                HBoxs[0].addWidget(lblState) 
                HBoxs[0].addWidget(prgbState) 
                HBoxs[0].addWidget(pbtnCancel) 
                pnlState.setWidget(pnlState2)
                pnlState.setAllowedAreas(Mt.AllDockWidgetAreas)
                pnlState.setFeatures(MDockWidget.AllDockWidgetFeatures)
                Universals.MainWindow.addDockWidget(Mt.TopDockWidgetArea, pnlState)
                pnlState.setMaximumHeight(60)
            else:
                pnlState = MDialog(Universals.MainWindow)
                if len(Universals.MySettings)>0 and Universals.isActivePyKDE4==True:
                    pnlState.setButtons(MDialog.None)
                pnlState.setModal(True)
                pnlState.setMinimumWidth(500) 
                pnlMain = MWidget(pnlState)
                HBoxs.append(MHBoxLayout(pnlMain))
                HBoxs[0].addWidget(prgbState) 
                HBoxs[0].addWidget(pbtnCancel) 
                if len(Universals.MySettings)>0 and Universals.isActivePyKDE4==True:
                    pnlState.setMainWidget(pnlMain)
                else:
                    pnlState.setLayout(HBoxs[0])
                pnlState.show()
        prgbState.setRange(0, _maxValue)
        prgbState.setValue(_value)
        if pbtnCancel!=None:
            if _isShowCancel:
                pbtnCancel.setVisible(True)
            else:
                pbtnCancel.setVisible(False)
        if Universals.getBoolValue("isMinimumWindowMode") and Universals.isCanBeShowOnMainWindow:
            lblState.setText(_title+" ( "+str(_value)+" / "+str(_maxValue)+" )")
        else:
            pnlState.setWindowTitle(_title+" ( "+str(_value)+" / "+str(_maxValue)+" )")
        if _value==_maxValue:
            if Universals.getBoolValue("isMinimumWindowMode") and Universals.isCanBeShowOnMainWindow:
                Universals.MainWindow.unlockForm()
                Universals.MainWindow.removeDockWidget(pnlState)
            else:
                pnlState.setModal(False)
                pnlState.close()
            if pbtnCancel!=None:
                pbtnCancel.setVisible(False)
            pnlState.deleteLater()
            prgbState.deleteLater()
            pnlState, prgbState, lblState, pbtnCancel = None, None, None, None
    
    def sleep(_title, _value=0, _isShowCancel=False):
        import time
        maxTime = _value*4
        step = 0
        while step<=maxTime:
            showState(_title, step, maxTime, _isShowCancel)
            step += 1
            time.sleep(0.25)
            
    def select(_title="Hamsi Cover", _detail="", _itemList=[""], _currentItem=0):
        if _detail=="": 
            _detail = _title
            _title = "Hamsi Cover"
        import Organizer
        if len(Universals.MySettings)>0 and Universals.isActivePyKDE4==True:
            selectedValue, isSelected = MInputDialog.getItem(trForUI(str(_title)+"!.."), trForUI(str(_detail)), [trForUI(str(x)) for x in _itemList], _currentItem, False)
        else:
            selectedValue, isSelected = MInputDialog.getItem(Universals.activeWindow(), trForUI(str(_title)+"!.."), trForUI(str(_detail)), [trForUI(str(x)) for x in _itemList], _currentItem, False)
        if isSelected==False:
            return None
        return selectedValue
                
        

        
        
        
        
        
        
        
        
        
        
        
