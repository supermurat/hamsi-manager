# -*- coding: utf-8 -*-
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


import sys,os

import Variables
from MyObjects import *
import Universals
import Settings
import InputOutputs, Records
import traceback
import logging
from RoutineChecks import isQuickMake, QuickMakeParameters, myArgvs
iSClosingInErrorReporting = False

class ReportBug(MDialog):
    global isClose
    isClose=False
    def __init__(self, _isOnlyReport=False, _hideFixMe=False):
        global errorDetails, isClose
        lastErrorDetails = str(sys.exc_info())
        lastErrorDetailsValues = sys.exc_info()
        MainWindow = Universals.MainWindow
        if Universals.isStartingSuccessfully==True:
            isShowFixMe = False
        else:
            isShowFixMe = True
        try:MDialog.__init__(self, MainWindow)
        except:MDialog.__init__(self, None)
        QtWebKit = getMyObject("QtWebKit")
        self.pathOfReportFile = ""
        self.isOnlyReport=True
        isClose=False
        self.isLoading=True
        errorDetails = "<b>" + str(translate("ReportBug", "Please check your personal information from this table."))+"</b><br>"
        if _isOnlyReport==False:
            Universals.isRaisedAnError = True
            realErrorDetails = str(self.formatExceptionInfo())
            realErrorDetails += "<hr>"
            self.isOnlyReport=False
            realErrorDetails += lastErrorDetails
            cla, error, trbk = lastErrorDetailsValues
            try:
                excArgs = error.__dict__["args"]
            except:
                excArgs = ""
            try:realErrorDetails += "<p><b>" + str(translate("ReportBug", "Error : ")) + "</b>" + traceback.format_tb(trbk, 5) + "</p>"
            except:pass
            realErrorDetails += ("<p><b>" + str(translate("ReportBug", "Error Name : ")) + "</b>" + str(cla.__name__) + "<br><b>" +
                            str(translate("ReportBug", "Error : ")) + "</b>"+str(error)+"<br><b>" +
                            str(translate("ReportBug", "Error arguments : ")) + "</b>"+str(excArgs)+"</p><hr><p><b>" +
                            str(translate("ReportBug", "Last Signal Sender (Object Name,Object Text) : ")) + "</b>\"")
            try:realErrorDetails +=unicode(self.sender().objectName())+"&quot;,&quot;"
            except:realErrorDetails +="&quot;,&quot;"
            try:realErrorDetails +=unicode(self.sender().text())+"&quot;"
            except:realErrorDetails +="&quot;"
            realErrorDetails = realErrorDetails.replace("\\n", "<br>").replace("\'", "&#39;")
        try:Records.saveAllRecords()
        except:pass
        try:Universals.saveSettings()
        except:pass
        try:
            if Universals.isActivePyKDE4==True:
                self.setButtons(MDialog.None)
        except:pass
        try:
            try:
                errorDetails+="<p><b>"+str(translate("ReportBug", "Contents Directory : "))+"</b>" + InputOutputs.currentDirectoryPath+"</p>"
            except:pass
            errorDetails +="<hr><p><h3>"+str(translate("ReportBug", "Table Contents : "))+"</h3>"
            import Tables
            errorDetails += Tables.exportValues("return", "html", "no")
        except:pass
        try:
            errorDetails +="</p><hr><p><h3>"+str(translate("ReportBug", "File Information : "))+"</h3><table border=1>"
            for rowNo in range(len(Universals.MainWindow.Table.currentTableContentValues)):
                filePath = Universals.MainWindow.Table.currentTableContentValues[rowNo]["path"]
                errorDetails +="<tr><td>" 
                try:errorDetails += str(unicode(filePath, InputOutputs.fileSystemEncoding))
                except:
                    try:errorDetails += str(filePath) 
                    except:errorDetails += filePath
                errorDetails +="</td></tr>"
            errorDetails +="</table></p><hr><p><h3>"+str(translate("ReportBug", "File Details : "))+"</h3><table border=1>"
            for rowNo in range(len(Universals.MainWindow.Table.currentTableContentValues)):
                errorDetails +="<tr>"
                for key, value in Universals.MainWindow.Table.currentTableContentValues[rowNo]:
                    errorDetails +="<td>"
                    try:errorDetails +=str(value)
                    except:errorDetails +=value
                    errorDetails +="</td>"
                errorDetails +="</tr>"
            errorDetails+="</table></p>"
        except:pass
        errorDetails += "<b>" + str(translate("ReportBug", "Active Dialog`s Titles : ")) + "</b>"
        try:errorDetails += str(Universals.HamsiManagerApp.activeModalWidget().windowTitle())+","
        except:errorDetails += "<br>"
        try:errorDetails += str(Universals.HamsiManagerApp.activePopupWidget().windowTitle())+","
        except:errorDetails += "<br>"
        try:errorDetails += str(Universals.HamsiManagerApp.activeWindow().windowTitle())+","
        except:errorDetails += "<br>"
        errorDetails += "<br>"
        try:
            errorDetails += "<b>" + str(translate("ReportBug", "Application Version : ")) + "</b>"
            errorDetails += str(Universals.HamsiManagerApp.applicationVersion())+"<br>"
        except:
            errorDetails += "<br>"
        try:
            errorDetails += "<b>" + str(translate("ReportBug", "Is Starting Successfully : ")) + "</b>"
            errorDetails += str(Universals.isStartingSuccessfully) + "<br>"
            errorDetails += "<b>" + str(translate("ReportBug", "Is Reporting Manuel : ")) + "</b>"
            errorDetails += str(_isOnlyReport) + "<br>"
            errorDetails += "<b>" + str(translate("ReportBug", "Is Quick Make : ")) + "</b>"
            errorDetails += str(isQuickMake) + "<br>"
            errorDetails += "<b>" + str(translate("ReportBug", "Quick Make Parameters : ")) + "</b>"
            errorDetails += str(QuickMakeParameters) + "<br>"
            errorDetails += "<b>" + str(translate("ReportBug", "My Parameters : ")) + "</b>"
            errorDetails += str(myArgvs) + "<br>"
            errorDetails += "<b>FileSystemCharSet : </b>"
            errorDetails += str(Variables.defaultFileSystemEncoding) + "<br>"
            errorDetails += "<b>SystemCharSet : </b>"
            errorDetails += str(sys.getdefaultencoding().lower()) + "<br>"
            try:
                errorDetails += "<b>OS Name : </b>"
                errorDetails += str(os.name) + "<br>"
            except:
                errorDetails += "<br>"
            try:
                import platform
                errorDetails += "<b>Python Version : </b>"
                errorDetails += str(platform.python_version()) + "<br>"
                errorDetails += "<b>uname : </b>"
                errorDetails += str(platform.uname()) + "<br>"
                try:
                    errorDetails += "<b>Linux Distribution : </b>"
                    errorDetails += str(platform.linux_distribution()) + "<br>"
                except:
                    errorDetails += "<br>"
            except:
                errorDetails += "<br>"
            if Variables.MyObjectName == "PyQt4":
                try:
                    errorDetails += "<b>PyQt4 (Qt) Version : </b>"
                    errorDetails += str(PYQT_VERSION_STR) + " ("+ str(MT_VERSION_STR) + ")<br>"
                except:
                    errorDetails += "<br>"
                try:
                    from PySide import QtCore
                    errorDetails += "<b>PySide (Qt) Version : </b>"
                    errorDetails += str(QtCore.qVersion()) + " (" + QtCore.QT_VERSION_STR +")<br>"
                except:
                    errorDetails += "<br>"
            elif Variables.MyObjectName == "PySide":
                try:
                    errorDetails += "<b>PySide (Qt) Version : </b>"
                    errorDetails += str(PYQT_VERSION_STR) + " ("+ str(MT_VERSION_STR) + ")<br>"
                except:
                    errorDetails += "<br>"
                try:
                    from PyQt4 import QtCore
                    errorDetails += "<b>PyQt4 (Qt) Version : </b>"
                    errorDetails += str(QtCore.qVersion()) + " (" + QtCore.QT_VERSION_STR +")<br>"
                except:
                    errorDetails += "<br>"
            try:
                from PyKDE4 import kdecore
                errorDetails += "<b>PyKDE4 Version : </b>"
                errorDetails += str(kdecore.versionString()) + "<br>"
            except:
                errorDetails += "<br>"
            for keyName in Universals.MySettings:
                if Variables.willNotReportSettings.count(keyName)==0:
                    errorDetails += "<b>" + str(keyName) + " : " + "</b>"
                    errorDetails += str(Universals.MySettings[keyName]) + "<br>"
        except:pass
        try:
            import Tables
            errorDetails += "<b>" + str(translate("ReportBug", "Table Type No : ")) + "</b>" + str(Universals.tableType) +"<br>"
        except:pass
        if _isOnlyReport==False:
            errorDetails += str(realErrorDetails)
        try:
            import Dialogs
            if Dialogs.pnlState!=None:
                Dialogs.showState("", 1, 1)
        except:pass
        pnlMain = MWidget(self)
        self.vblMain = MVBoxLayout(pnlMain)
        self.pbtnClose = MPushButton(translate("ReportBug", "Close (Please Report This Bug First.)"))
        self.pbtnShowDetailsPage = MPushButton(translate("ReportBug", "Show Details File"))
        self.pbtnCheckUpdate = MPushButton(translate("ReportBug", "Check Update"))
        self.teErrorDetails = MTextEdit()  
        self.wvWeb = QtWebKit.QWebView()
        self.createErrorPage(errorDetails)
        self.connect(self.wvWeb,SIGNAL("loadProgress(int)"),self.loading)
        try:
            self.teErrorDetails.setHtml(trForUI(errorDetails.replace("<hr>", "")))
        except:
            self.teErrorDetails.setHtml(translate("ReportBug", "I cannot send the error details due to some character errors.<br>To see the details, please click on the \"Show details file\" button."))
            self.teErrorDetails.setEnabled(False)
        self.connect(self.teErrorDetails,SIGNAL("textChanged()"), self.errorDetailsChanged)
        self.connect(self.pbtnClose,SIGNAL("clicked()"), self.close)
        self.connect(self.pbtnShowDetailsPage,SIGNAL("clicked()"), self.showDetailsPage)
        self.connect(self.pbtnCheckUpdate,SIGNAL("clicked()"), self.checkUpdate)
        self.teErrorDetails.setMinimumHeight(220)
        self.vblMain.addWidget(self.teErrorDetails, 10) 
        self.vblMain.addWidget(self.wvWeb, 10) 
        hbox0 = MHBoxLayout()
        hbox0.addWidget(self.pbtnShowDetailsPage,1)
        hbox0.addStretch(2)
        hbox0.addWidget(self.pbtnCheckUpdate,1)
        hbox0.addWidget(self.pbtnClose,1)
        self.vblMain.addLayout(hbox0, 1)
        try:
            if Universals.isActivePyKDE4==True:
                self.setMainWidget(pnlMain)
            else:
                self.setLayout(self.vblMain)
        except:
            self.setLayout(self.vblMain)
        self.setWindowTitle(translate("ReportBug", "Please Report This Bug!.."))
        self.setMaximumSize(600, 375)  
        self.wvWeb.setMinimumHeight(272)
        self.show()
        self.setMaximumSize(10000, 10000)
        if isShowFixMe == True and isQuickMake==False and _hideFixMe==False and Universals.loggingLevel!=logging.DEBUG:
            try:
                import Dialogs
                answer = Dialogs.askSpecial(translate("ReportBug", "I Have A Suggestion!"),
                            translate("ReportBug", "<b>Please check the following: ;</b><br>"+
                            "<b>1-)</b>If you have received this error when you were checking the last folder, reset the \"Last Directory\",<br>"+
                            "<b>2-)</b>If you have received this error due to your changed settings, reset the \"Settings\",<br>"+
                            "<b>3-)</b>If you continue to receive this error even after resetting the settings, reset \"All\".<br>"+
                            "<br><b>You can enable Hamsi Manager to run as normal.<br>Please take a moment to send us the error report.</b>"), 
                            translate("ReportBug", "Last Directory"), 
                            translate("ReportBug", "All"), 
                            translate("ReportBug", "Settings"), 
                            translate("ReportBug", "Ignore"))
                if answer==translate("ReportBug", "Last Directory"):
                    Settings.setting().setValue("lastDirectory", MVariant(Variables.userDirectoryPath.decode("utf-8")))
                elif answer==translate("ReportBug", "Settings"):
                    Settings.reFillSettings(True)
                elif answer==translate("ReportBug", "All"):
                    Settings.reFillAll(True)
            except:pass
    
    def formatExceptionInfo(self, maxTBlevel=5):
        cla, exc, trbk = sys.exc_info()
        excName = cla.__name__
        try:
            excArgs = exc.__dict__["args"]
        except:
            excArgs = "<no args>"
        excTb = traceback.format_tb(trbk, maxTBlevel)
        return (excName, excArgs, excTb)
    
    def createErrorPage(self, _errorDetails, _userNote="", _userName="", _mail=""):
        _errorDetails = _errorDetails.replace("\"", "&quot;").replace("\'", "&#39;")
        self.isLoading=False
        language = "en_GB"
        if "language" in Universals.MySettings:
            language = Universals.MySettings["language"]
        htmlString=('<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">'+
                    '<html xmlns="http://www.w3.org/1999/xhtml"><head><meta http-equiv="Content-Type" content="text/html; charset=utf-8" /><title>Hamsi Manager</title></head><body>'+
                    '<center>'+
                    '<form action="http://hamsiapps.com/ForMyProjects/ReportBug.php" method="post">'+
                    '<TABLE><TR><TD valign="top">%s'
                    '</TD><TD colspan=2><textarea ROWS="7" COLS="40" name="userNotes">%s</textarea></TD></TR></TABLE>'+
                    '<TABLE><TR><TD valign="top" colspan=2>%s</TD><TD align="right"><input type="search" name="nameAndSurname" value="%s"></input></TD></TR>'+
                    '<TR><TD valign="top" colspan=2>%s</TD><TD align="right"><input type="search" name="mail" value="%s"></input></TD></TR></TABLE>'+
                    '<TABLE><TR><TD align="right"><input name="send" type="submit" value="&nbsp;&nbsp;&nbsp;%s&nbsp;&nbsp;&nbsp;&nbsp;"></TD></TR></TABLE>'+
                    '<INPUT TYPE="hidden" name="error" value="~ERRORDETAILS~" />'+
                    '<INPUT TYPE="hidden" name="thankYouMessages" value="%s" />'+
                    '<INPUT TYPE="hidden" name="p" value="HamsiManager" />'+
                    '<INPUT TYPE="hidden" name="l" value="' + str(language) + '" />'+
                    '<INPUT TYPE="hidden" name="v" value="' + str(Variables.intversion) + '" /></form>'+
                    '~ADDITIONALDETAILS~</center></body></html>'
                    ) % (
                    str(translate("ReportBug", "<b>Error description :</b> <br>(Be can null)<br><b>Note:</b>Please write what you did before you received the error here.")), 
                    _userNote, 
                    str(translate("ReportBug", "<b>Name and Surname :</b> (Be can null)")), 
                    _userName, 
                    str(translate("ReportBug", "<b>E-mail address :</b> (Be can null)<br><b>Note:</b>Will be kept strictly confidential. It will be used solely to report you back once the problem is solved..")), 
                    _mail, 
                    str(translate("ReportBug", "Report Bug")), 
                    str(translate("ReportBug", "Thank you for sending us your error report. You have already contributed a lot to make the next release even better..<br>")))
        self.createErrorFile(htmlString.replace("~ERRORDETAILS~", _errorDetails).replace("~ADDITIONALDETAILS~", _errorDetails))
        encodedType = ""
        try:
            errorDetails = _errorDetails.decode("utf-8")
            encodedType = "utf-8"
        except:
            try:
                errorDetails = str(unicode(_errorDetails, "iso-8859-9"))
                t = errorDetails.decode("utf-8")
                encodedType = "iso-8859-9"
            except:
                try:
                    errorDetails = str(unicode(_errorDetails, "cp-1254"))
                    t = errorDetails.decode("utf-8")
                    encodedType = "cp-1254"
                except:
                    for charName in Variables.getCharSets():
                        try:
                            errorDetails = str(unicode(_errorDetails, charName))
                            t = errorDetails.decode("utf-8")
                            encodedType = charName
                        except:pass
                    if encodedType=="":
                        errorDetails = ""
        htmlString = htmlString.replace("~ERRORDETAILS~", errorDetails).replace("~ADDITIONALDETAILS~", str(translate("ReportBug", "<b>(Is Encoded With %s.)</b>")) % (encodedType))
        try:self.wvWeb.setHtml(trForUI(htmlString))
        except:
            self.teErrorDetails.setVisible(False)   
            self.wvWeb.setUrl(MUrl(self.pathOfReportFile.decode("utf-8")))
        self.isLoading=True
    
    def errorDetailsChanged(self):
        self.createErrorPage(str(self.teErrorDetails.toHtml()))
        pass
    
    def loading(self, _value):
        if self.isLoading:
            if (_value==100):
                self.pbtnClose.setText(translate("ReportBug", "Close"))

    def closeEvent(self, _event):
        global isClose, iSClosingInErrorReporting
        isClose=True
        try:
            self.close()
            if self.isOnlyReport==False and Universals.loggingLevel!=logging.DEBUG:
                iSClosingInErrorReporting = True
                self.parent().close()
        except:pass
        
    def createErrorFile(self, _errorDetails):
        if self.pathOfReportFile=="":
            import tempfile, random
            self.pathOfReportFile = tempfile.gettempdir() + "/HamsiManager-ErrorOutput-"+ str(random.randrange(0, 1000000))+".html"
            InputOutputs.writeToFile(self.pathOfReportFile, _errorDetails)
    
    def showDetailsPage(self):
        self.teErrorDetails.setVisible(False)   
        self.wvWeb.setUrl(MUrl(self.pathOfReportFile.decode("utf-8")))
        
    def checkUpdate(self):
        import UpdateControl
        UpdateControl.UpdateControl(self)
        
        
        
