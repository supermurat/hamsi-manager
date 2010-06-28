# -*- coding: utf-8 -*-

from MyObjects import *
from PyQt4.Qsci import QsciScintilla, QsciLexerPython, QsciAPIs
import sys
import Settings
import Dialogs
import Universals

class RunCommand(MDialog):
    def __init__(self, _parent):
        MDialog.__init__(self, _parent)
        if Universals.isActivePyKDE4==True:
            self.setButtons(MDialog.None)
        self.sciCommand = QsciScintilla()
        self.sciCommand.setUtf8(True)
        self.sciCommand.setText(Settings.codesOfUser().decode("utf-8"))
        self.sciCommand.setAutoIndent(True)
        self.sciCommand.setAutoCompletionThreshold(2)
        self.sciCommand.setAutoCompletionSource(QsciScintilla.AcsDocument)
        self.sciCommand.setLexer(QsciLexerPython(self))
        pbtnRunCommandAndClose = MPushButton(translate("RunCommand", "Run And Close"))
        pbtnRunCommand = MPushButton(translate("RunCommand", "Run"))
        pbtnClose = MPushButton(translate("RunCommand", "Close"))
        pbtnClear = MPushButton(translate("RunCommand", "Clear"))
        self.connect(pbtnRunCommandAndClose,SIGNAL("clicked()"),self.runCommandAndClose)
        self.connect(pbtnRunCommand,SIGNAL("clicked()"),self.runCommand)
        self.connect(pbtnClose,SIGNAL("clicked()"),self.close)
        self.connect(pbtnClear,SIGNAL("clicked()"),self.clear)
        pnlMain = MWidget(self)
        vblMain = MVBoxLayout(pnlMain)
        hbox = MHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(pbtnClear,1)
        hbox.addWidget(pbtnRunCommand,1)
        hbox.addWidget(pbtnRunCommandAndClose,1)
        hbox.addWidget(pbtnClose,1)
        vblMain.addWidget(self.sciCommand)
        vblMain.addLayout(hbox)
        if Universals.isActivePyKDE4==True:
            self.setMainWidget(pnlMain)
        else:
            self.setLayout(vblMain)
        self.setWindowTitle(translate("RunCommand", "Run Command"))
        self.setWindowIcon(MIcon("Images:runCommand.png"))
        self.setMinimumWidth(500)
        self.setMinimumHeight(450)
        self.show()

    def closeEvent(self, _event):
        if self.saveCommand()==False:
            _event.ignore() 

    def runCommandAndClose(self):
        if self.runCommand():
            self.close()
        
    def runCommand(self):
        try:
            exec str(self.sciCommand.text())
            return True
        except Exception , error:
            import traceback
            cla, error, trbk = sys.exc_info()
            errorName = cla.__name__
            try:
                excArgs = error.__dict__["args"]
            except KeyError:
                excArgs = "<no args>"
            errorDetail = traceback.format_tb(trbk, 5)
            errorDetails = str(errorName)+"\n"+str(error)+"\n"+str(excArgs)+"\n"+str(errorDetail[0])
            Dialogs.showError(translate("RunCommand", "Error: Failed To Run The Query"),
                        str(translate("RunCommand", "Error details: <br> \"%s\"")) % (errorDetails))
            return False
    
    def saveCommand(self):
        if str(Settings.codesOfUser())!=str(unicode(self.sciCommand.text(), "utf-8")):
            answer = Dialogs.ask(translate("RunCommand", "Do You Wish To Save Your Codes?"), 
                            translate("RunCommand", "Do you wish to save your codes so that you can continue later?"), True)
            if answer==Dialogs.Yes:
                Settings.codesOfUser(unicode(self.sciCommand.text(), "utf-8"))
            elif answer==Dialog.Cancel:
                return False
        return True

    def clear(self):
        answer = Dialogs.ask(translate("RunCommand", "Your Codes Will Be Deleted!.."), 
                            translate("RunCommand", "Your codes will be deleted and the default codes will be installed. Do you wish to clear the current codes?"))
        if answer==Dialogs.Yes:
            Settings.reFillCodesOfUser()
            self.sciCommand.setText(Settings.codesOfUser().decode("utf-8"))
        
        
        