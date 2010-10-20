# -*- coding: utf-8 -*-

import sys,os
import Variables
from MyObjects import *
import Universals
import Settings

class SuggestIdea(MDialog):
    def __init__(self):
        global errorDetails
        MDialog.__init__(self, Universals.MainWindow)
        QtWebKit = getMyObject("QtWebKit")
        if Universals.isActivePyKDE4==True:
            self.setButtons(MDialog.None)
        pnlMain = MWidget(self)
        self.vblMain = MVBoxLayout(pnlMain)
        self.pbtnClose = MPushButton(translate("SuggestIdea", "Close (Please Suggest Idea First.)"))
        self.wvWeb = QtWebKit.QWebView()
        self.connect(self.pbtnClose,SIGNAL("clicked()"),self.close)
        self.vblMain.addWidget(self.wvWeb, 10) 
        self.createIdeaPage()
        hbox0 = MHBoxLayout()
        hbox0.addStretch(2)
        hbox0.addWidget(self.pbtnClose,1)
        self.vblMain.addLayout(hbox0, 1)
        try:
            if Universals.isActivePyKDE4==True:
                self.setMainWidget(pnlMain)
            else:
                self.setLayout(self.vblMain)
        except:
            self.setLayout(self.vblMain)
        self.setWindowTitle(translate("SuggestIdea", "Please Suggest Idea"))
        self.setMaximumSize(600, 375)  
        self.wvWeb.setMinimumHeight(272)
        self.show()
        self.setMaximumSize(10000, 10000)
    
    def createIdeaPage(self):
        htmlString=('<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">'+
                    '<html xmlns="http://www.w3.org/1999/xhtml"><head><meta http-equiv="Content-Type" content="text/html; charset=utf-8" /><title>Hamsi Manager</title></head><body>'+
                    '<center>'+
                    '<form action="http://hamsiapps.com/ForMyProjects/SuggestIdea.php" method="post">'+
                    '<TABLE><TR><TD valign="top">%s'
                    '</TD><TD colspan=2><textarea ROWS="7" COLS="40" name="userNotes"></textarea></TD></TR></TABLE>'+
                    '<TABLE><TR><TD valign="top" colspan=2>%s</TD><TD align="right"><input type="search" name="nameAndSurname" value=""></input></TD></TR>'+
                    '<TR><TD valign="top" colspan=2>%s</TD><TD align="right"><input type="search" name="mail" value=""></input></TD></TR></TABLE>'+
                    '<TABLE><TR><TD align="right"><input name="send" type="submit" value="&nbsp;&nbsp;&nbsp;%s&nbsp;&nbsp;&nbsp;&nbsp;"></TD></TR></TABLE>'+
                    '<INPUT TYPE="hidden" name="thankYouMessages" value="%s" />'+
                    '<INPUT TYPE="hidden" name="p" value="HamsiManager" />'+
                    '<INPUT TYPE="hidden" name="l" value="' + str(Universals.MySettings["language"]) + '" />'+
                    '<INPUT TYPE="hidden" name="v" value="' + str(Variables.intversion) + '" /></form>'+
                    '</center></body></html>'
                    ) % (
                    str(translate("SuggestIdea", "<b>Idea :</b>")), 
                    str(translate("SuggestIdea", "<b>Name and Surname :</b>")), 
                    str(translate("SuggestIdea", "<b>E-mail address :</b><br><b>Note:</b>Will be kept strictly confidential. It will be used solely to learn information about of your idea.")), 
                    str(translate("SuggestIdea", "Suggest Idea")), 
                    str(translate("SuggestIdea", "Thank you for sending us your idea. You have contributed a lot to make the next release even better.<br>")))
        self.wvWeb.setHtml(htmlString.decode("utf-8"))
        
        
        
        
        