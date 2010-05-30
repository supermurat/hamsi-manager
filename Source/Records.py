# -*- coding: utf-8 -*-

import time
import Universals
import InputOutputs
import Settings

class Records():
    global add, create, read, setTitle, showInWindow, clearRecords, recordContents, isSetedTitle, saveAllRecords,recordContents, checkSize, recordType, lastRecordType, setRecordType, restoreRecordType
    recordContents = ""
    isSetedTitle = False
    recordType = 0
    lastRecordType = 0
    #recordType : 0=Normal, 1=Debug
    
    def create():
        global recordContents
        from MyObjects import translate
        recordContents += str(translate("Records", "Hamsi Manager Log File - Time Created : ")) + str(time.strftime("%d.%m.%Y %H:%M:%S"))+"\n"
    
    def setTitle(_title):
        global isSetedTitle, recordContents
        if Universals.MySettings.keys().count("isSaveActions")==0 or Universals.getBoolValue("isSaveActions"):
            recordContents += str(_title) + "\n"
        isSetedTitle = True
    
    def add(_action, _previous="", _now=""):
        global recordContents
        if Universals.MySettings.keys().count("isSaveActions")==0 or Universals.getBoolValue("isSaveActions"):
            if recordType==0 or (recordType==1 and Universals.isDebugMode):
                recordContents += str(_action + " ::::::: '") + str(_previous) + "' >>>>>>>> '" + str(_now) + "<<<<<<<" + str(time.strftime("%d.%m.%Y %H:%M:%S"))+"'\n"
        
    def setRecordType(_recordType):
        global lastRecordType, recordType
        lastRecordType = recordType
        recordType = _recordType
        
    def restoreRecordType():
        global recordType
        recordType = lastRecordType
        
    def saveAllRecords():
        global recordContents, isSetedTitle
        if Universals.MySettings.keys().count("isSaveActions")==0 or Universals.getBoolValue("isSaveActions"):
            if InputOutputs.isFile(Settings.recordFilePath)==False:
                create()
            setRecordType(1)
            InputOutputs.addToFile(Settings.recordFilePath, recordContents)
            restoreRecordType()
        recordContents = ""
        isSetedTitle = False
    
    def checkSize():
        setRecordType(1)
        InputOutputs.fixToSize(Settings.recordFilePath, (int(Universals.MySettings["maxRecordFileSize"])*1024))
        restoreRecordType()
        
    def read(_isShowErrorDialog=True):
        if InputOutputs.isFile(Settings.recordFilePath)==True:
            return InputOutputs.readFromFile(Settings.recordFilePath)
        else:
            if _isShowErrorDialog:
                import Dialogs
                from MyObjects import translate
                Dialogs.showError(translate("Records", "Cannot Find The Log File"), 
                            translate("Records", "No log files found."))
            return False
            
    def clearRecords():
        from MyObjects import translate
        InputOutputs.writeToFile(Settings.recordFilePath, unicode(translate("Records", "Hamsi Manager Log File - Time Clear : "), "utf-8") + str(time.strftime("%d.%m.%Y %H:%M:%S"))+"\n")
        try:dialog.close()
        except:pass
        
    def showInWindow():
        from MyObjects import MDialog, translate, MWidget, MVBoxLayout, MHBoxLayout, MTextEdit, MTextOption, MPushButton, SIGNAL, MObject
        import Organizer
        global dialog
        recordString = read()
        if recordString != False:
            dialog = MDialog(Universals.MainWindow)
            if Universals.isActivePyKDE4==True:
                dialog.setButtons(MDialog.None)
            dialog.setWindowTitle(translate("Records", "Last Action Logs"))
            pnlMain = MWidget(dialog)
            vblMain = MVBoxLayout(pnlMain)
            info = MTextEdit()
            info.setPlainText(Organizer.showWithIncorrectChars(recordString).decode("utf-8"))
            info.setWordWrapMode(MTextOption.ManualWrap)
            pbtnClose = MPushButton(translate("Records", "OK"))
            pbtnClear = MPushButton(translate("Records", "Clear"))
            MObject.connect(pbtnClose, SIGNAL("clicked()"), dialog.close)
            MObject.connect(pbtnClear, SIGNAL("clicked()"), clearRecords)
            vblMain.addWidget(info)
            hblBox = MHBoxLayout()
            hblBox.addWidget(pbtnClear)
            hblBox.addWidget(pbtnClose)
            vblMain.addLayout(hblBox)
            if Universals.isActivePyKDE4==True:
                dialog.setMainWidget(pnlMain)
            else:
                dialog.setLayout(vblMain)
            dialog.setMinimumSize(550, 400)
            dialog.show()
            
            
            
