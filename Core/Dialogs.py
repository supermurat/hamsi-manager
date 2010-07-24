# -*- coding: utf-8 -*-

from MyObjects import *
import Universals

class Dialogs():
    global show, showError, ask, askSpecial, showState, pnlState, prgbState, lblState, Ok, Cancel, Yes, No, Continue, select, pbtnCancel
    pnlState, prgbState, lblState, pbtnCancel = None, None, None, None
    Ok, Cancel, Yes, No, Continue = 1, 2, 3, 4, 5
    
    def show(_title="Hamsi Manager", _detail="", _btnString=translate("Dialogs", "OK")):
        MApplication.processEvents()
        if _detail=="": 
            _detail = _title
            _title = "Hamsi Manager"
        import Organizer
        if len(Universals.MySettings)>0 and Universals.isActivePyKDE4==True:
            MMessageBox.information(Universals.activeWindow(), Organizer.showWithIncorrectChars("<b>" + str(_title) + " : </b><br>" + str(_detail)).decode("utf-8"), Organizer.showWithIncorrectChars(str(_title)+"!..").decode("utf-8"))
        else:
            MMessageBox.information(Universals.activeWindow(),Organizer.showWithIncorrectChars(str(_title)+"!..").decode("utf-8"),Organizer.showWithIncorrectChars("<b>" + str(_title) + " : </b><br>" + str(_detail)).decode("utf-8"),_btnString)
        return True
        
    def showError(_title="Hamsi Manager", _detail="", _btnString=translate("Dialogs", "OK")):
        MApplication.processEvents()
        if _detail=="": 
            _detail = _title
            _title = "Hamsi Manager"
        import Organizer
        if len(Universals.MySettings)>0 and Universals.isActivePyKDE4==True:
            MMessageBox.error(Universals.activeWindow(), Organizer.showWithIncorrectChars("<b>" + str(_title) + " : </b><br>" + str(_detail)).decode("utf-8"), Organizer.showWithIncorrectChars(str(_title)+"!..").decode("utf-8"))
        else:
            MMessageBox.critical(Universals.activeWindow(),Organizer.showWithIncorrectChars(str(_title)+"!..").decode("utf-8"),Organizer.showWithIncorrectChars("<b>" + str(_title) + " : </b><br>" + str(_detail)).decode("utf-8"),_btnString)
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
                            Organizer.showWithIncorrectChars("<b>" + str(_title) + " : </b><br>" + str(_detail)).decode("utf-8"), 
                            Organizer.showWithIncorrectChars(_title).decode("utf-8"), 
                            MStandardGuiItem.yes(), MStandardGuiItem.no(), MStandardGuiItem.cancel(), 
                            Organizer.showWithIncorrectChars(_showAgainKeyName).decode("utf-8"), 
                            MMessageBox.AllowLink )
                else:
                    return MMessageBox.questionYesNoCancel(Universals.activeWindow(), 
                            Organizer.showWithIncorrectChars("<b>" + str(_title) + " : </b><br>" + str(_detail)).decode("utf-8"), 
                            Organizer.showWithIncorrectChars(_title).decode("utf-8"), 
                            MStandardGuiItem.yes(), MStandardGuiItem.no(), MStandardGuiItem.cancel(), "", 
                            MMessageBox.AllowLink )
            else:
                if _showAgainKeyName!="":
                    return MMessageBox.messageBox(Universals.activeWindow(), 
                            MMessageBox.QuestionYesNo, 
                            Organizer.showWithIncorrectChars("<b>" + str(_title) + " : </b><br>" + str(_detail)).decode("utf-8"), 
                            Organizer.showWithIncorrectChars(_title).decode("utf-8"), 
                            MStandardGuiItem.yes(), MStandardGuiItem.no(), MStandardGuiItem.cancel(), 
                            Organizer.showWithIncorrectChars(_showAgainKeyName).decode("utf-8"), 
                            MMessageBox.AllowLink )
                else:
                    return MMessageBox.questionYesNo(Universals.activeWindow(), 
                            Organizer.showWithIncorrectChars("<b>" + str(_title) + " : </b><br>" + str(_detail)).decode("utf-8"), 
                            Organizer.showWithIncorrectChars(_title).decode("utf-8"), 
                            MStandardGuiItem.yes(), MStandardGuiItem.no(), "", 
                            MMessageBox.AllowLink )
        else:
            if _isShowCancel:
                try:mboxDialog = MMessageBox(Universals.activeWindow())
                except:mboxDialog = MMessageBox(None)
                mboxDialog.setWindowTitle(Organizer.showWithIncorrectChars(_title).decode("utf-8"))
                mboxDialog.setText(Organizer.showWithIncorrectChars("<b>" + str(_title) + " : </b><br>" + str(_detail)).decode("utf-8"))
                mboxDialog.setStandardButtons(MMessageBox.Yes | MMessageBox.No | MMessageBox.Cancel)
                pressedButtonNo = mboxDialog.exec_()
            else:
                try:mboxDialog = MMessageBox(Universals.activeWindow())
                except:mboxDialog = MMessageBox(None)
                mboxDialog.setWindowTitle(Organizer.showWithIncorrectChars(_title).decode("utf-8"))
                mboxDialog.setText(Organizer.showWithIncorrectChars("<b>" + str(_title) + " : </b><br>" + str(_detail)).decode("utf-8"))
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
        mboxDialog.setWindowTitle(Organizer.showWithIncorrectChars(_title).decode("utf-8"))
        mboxDialog.setText(Organizer.showWithIncorrectChars("<b>" + str(_title) + " : </b><br>" + str(_detail)).decode("utf-8"))
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
        if Universals.windowMode==Universals.windowModeKeys[1] and Universals.isCanBeShowOnMainWindow:
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
            
    def select(_title="Hamsi Cover", _detail="", _itemList=[u""], _currentItem=0):
        if _detail=="": 
            _detail = _title
            _title = "Hamsi Cover"
        import Organizer
        if len(Universals.MySettings)>0 and Universals.isActivePyKDE4==True:
            selectedValue, isSelected = MInputDialog.getItem(Organizer.showWithIncorrectChars(str(_title)+"!..").decode("utf-8"), Organizer.showWithIncorrectChars(str(_detail)).decode("utf-8"), [Organizer.showWithIncorrectChars(str(x)).decode("utf-8") for x in _itemList], _currentItem, False)
        else:
            selectedValue, isSelected = MInputDialog.getItem(Universals.activeWindow(), Organizer.showWithIncorrectChars(str(_title)+"!..").decode("utf-8"), Organizer.showWithIncorrectChars(str(_detail)).decode("utf-8"), [Organizer.showWithIncorrectChars(str(x)).decode("utf-8") for x in _itemList], _currentItem, False)
        if isSelected==False:
            return None
        return selectedValue
                
        

        
        
        
        
        
        
        
        
        
        
        
