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


import sys,os
from Core import Variables
from Core.MyObjects import *
from Core import Universals
from Core import Dialogs
from Core import ReportBug
import Options
from Options import OptionsForm
if Variables.isPython3k:
    from urllib.parse import unquote, quote
else:
    from urllib import unquote, quote

class SuggestIdea(MDialog):
    def __init__(self):
        MDialog.__init__(self, Universals.MainWindow)
        if isActivePyKDE4:
            self.setButtons(MDialog.NoDefault)
        pnlMain = MWidget(self)
        self.namMain = None
        self.nrqPost = None
        self.nrpBack = None
        self.vblMain = MVBoxLayout(pnlMain)
        self.pbtnSendAndClose = MPushButton(translate("SuggestIdea", "Send And Close"))
        self.pbtnCancel = MPushButton(translate("SuggestIdea", "Cancel"))
        self.cckbIsSendMySettings = Options.MyCheckBox(self, translate("SuggestIdea", "Send my settings for more better default settings."), 0, _stateChanged = self.isSendMySettings)
        self.connect(self.pbtnSendAndClose, SIGNAL("clicked()"), self.sendAndClose)
        self.connect(self.pbtnCancel, SIGNAL("clicked()"), self.cancel)
        lblIdea = MLabel(translate("SuggestIdea", "Idea : "))
        lblName = MLabel(translate("SuggestIdea", "Name And Surname : "))
        lblEMailAddress = MLabel(translate("SuggestIdea", "E-mail Address : "))
        lblAlert = MLabel(translate("SuggestIdea", "Note : Will be kept strictly confidential. It will be used solely to learn information about of your idea."))
        self.teIdea = MTextEdit(self)
        self.leName = MLineEdit(self)
        self.leEMailAddress = MLineEdit(self)
        hbox1 = MHBoxLayout()
        hbox1.addWidget(lblIdea, 1)
        hbox1.addWidget(self.teIdea, 20)
        hbox2 = MHBoxLayout()
        hbox2.addWidget(lblName, 1)
        hbox2.addWidget(self.leName, 20)
        hbox3 = MHBoxLayout()
        hbox3.addWidget(lblEMailAddress, 1)
        hbox3.addWidget(self.leEMailAddress, 20)
        hbox0 = MHBoxLayout()
        hbox0.addWidget(self.cckbIsSendMySettings,1)
        hbox0.addStretch(2)
        hbox0.addWidget(self.pbtnSendAndClose,1)
        hbox0.addWidget(self.pbtnCancel,1)
        VBox1 = MVBoxLayout()
        VBox1.addLayout(hbox2)
        VBox1.addLayout(hbox3)
        VBox1.addWidget(lblAlert)
        gboxContactInformations = MGroupBox(translate("SuggestIdea", "Contact Informations : "))
        gboxContactInformations.setLayout(VBox1)
        self.vblMain.addLayout(hbox1, 20)
        self.vblMain.addWidget(gboxContactInformations, 1)
        self.vblMain.addLayout(hbox0, 1)
        try:
            if isActivePyKDE4:
                self.setMainWidget(pnlMain)
            else:
                self.setLayout(self.vblMain)
        except:
            self.setLayout(self.vblMain)
        self.setWindowTitle(translate("SuggestIdea", "Please Suggest Idea"))
        self.setMaximumSize(600, 375)
        self.show()
        self.setMaximumSize(10000, 10000)
        
    def sendAndClose(self):
        try:
            Universals.isCanBeShowOnMainWindow = False
            self.namMain = MNetworkAccessManager(self)
            self.connect(self.namMain, SIGNAL("finished (QNetworkReply *)"), self.sendFinished)
            self.nrqPost = MNetworkRequest(MUrl("http://hamsiapps.com/ForMyProjects/SuggestIdea.php"))
            self.nrpBack = self.namMain.post(self.nrqPost, "p=HamsiManager&l=" + str(Universals.MySettings["language"]) + "&v=" + str(Variables.intversion) +
                                            "&thankYouMessages=new style" + 
                                            "&userNotes=" + quote(str(self.teIdea.toHtml())) + 
                                            "&nameAndSurname=" + quote(str(self.leName.text())) + 
                                            "&mail=" + quote(str(self.leEMailAddress.text()))
                                            )
            self.connect(self.nrpBack, SIGNAL("downloadProgress (qint64,qint64)"), self.sending)
            Dialogs.showState(translate("SuggestIdea", "Sending Your Idea"), 0, 100, True, self.cancelSending)
        except:
            ReportBug.ReportBug()
        
    def sending(self, _currentValue, _maxValue):
        Dialogs.showState(translate("SuggestIdea", "Sending Your Idea"), _currentValue, _maxValue, True, self.cancelSending)
    
    def cancelSending(self):
        if self.nrpBack is not None:
            self.nrpBack.abort()
        
    def sendFinished(self, _nrpBack):
        try:
            Dialogs.showState(translate("SuggestIdea", "Sending Your Idea"), 100, 100)
            if _nrpBack.error() == MNetworkReply.NoError:
                Dialogs.show(translate("SuggestIdea", "Suggestion Received Successfully"), translate("SuggestIdea", "Thank you for sending us your idea. You have contributed a lot to make the next release even better."))
                self.close()
            elif _nrpBack.error() == MNetworkReply.OperationCanceledError:
                Dialogs.show(translate("SuggestIdea", "Suggestion Canceled"), translate("SuggestIdea", "Suggestion canceled successfully."))
            else:
                Dialogs.show(translate("SuggestIdea", "An Error Has Occurred."), translate("SuggestIdea", "An unknown error has occurred. Please try again."))
            Universals.isCanBeShowOnMainWindow = True
            self.namMain = None
            self.nrqPost = None
            self.nrpBack = None
        except:
            ReportBug.ReportBug()
        
    def cancel(self):
        if self.nrpBack is not None:
            self.nrpBack.abort()
        self.close()
        
    def isSendMySettings(self):
        try:
            currenText = str(self.teIdea.toHtml())
            if self.cckbIsSendMySettings.checkState() == Mt.Checked:
                settingText = "<br><br>"
                for keyName in Universals.MySettings:
                    if Variables.willNotReportSettings.count(keyName)==0:
                        settingText += "<b>" + str(keyName) + " :</b> " + str(Universals.MySettings[keyName]) + "<br>"
                self.teIdea.setHtml(trForUI(currenText + "<br>----------------------////////----------------------<br><br><b>" + str(translate("SuggestIdea", "Note : You can check and delete your personal informations.")) + "</b>" + settingText))
            else:
                currenText = currenText.split("----------------------////////----------------------")[0]
                self.teIdea.setHtml(trForUI(currenText))
        except:
            ReportBug.ReportBug()
        
        
        
