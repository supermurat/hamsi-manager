# This file is part of HamsiManager.
#
# Copyright (c) 2010 - 2015 Murat Demir <mopened@gmail.com>
#
# Hamsi Manager is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# Hamsi Manager is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with HamsiManager; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA


from Core.MyObjects import *
from Core import Universals as uni
from Core import Dialogs
import FileUtils as fu
import Options
from Options import OptionsForm
from Core import ReportBug

MyDialog, MyDialogType, MyParent = getMyDialog()


class FileTreeBuilder(MyDialog):
    def __init__(self, _directory):
        MyDialog.__init__(self, MyParent)
        if MyDialogType == "MDialog":
            if isActivePyKDE4:
                self.setButtons(MyDialog.NoDefault)
        elif MyDialogType == "MMainWindow":
            self.setObjectName("Packager")
            setMainWindow(self)
        newOrChangedKeys = uni.newSettingsKeys + uni.changedDefaultValuesKeys
        wOptionsPanel = OptionsForm.OptionsForm(None, "fileTree", None, newOrChangedKeys)
        lblDirectory = MLabel(translate("FileTreeBuilder", "Directory : "))
        lblOutputTarget = MLabel(translate("FileTreeBuilder", "Output Target : "))
        lblOutputType = MLabel(translate("FileTreeBuilder", "Output Type : "))
        lblContentType = MLabel(translate("FileTreeBuilder", "Content Type : "))
        lblSubDirectoryDeepDetails = translate("FileTreeBuilder",
                                               "You can select sub directory deep.<br><font color=blue>You can select \"-1\" for all sub directories.</font>")
        lblSubDirectoryDeep = MLabel(translate("FileTreeBuilder", "Deep : "))
        self.cbSubDirectoryDeep = Options.MyComboBox(self,
                                                     [str(x) for x in range(-1, 10)],
                                                     0, "subDirectoryDeep")
        self.cbSubDirectoryDeep.setToolTip(lblSubDirectoryDeepDetails)
        self.cbOutputType = Options.MyComboBox(self,
                                               [translate("FileTreeBuilder", "HTML"),
                                                translate("FileTreeBuilder", "Plain Text")], 0,
                                               "FileTreeBuilderOutputType")
        self.cbOutputTarget = Options.MyComboBox(self,
                                                 [translate("FileTreeBuilder", "File"),
                                                  translate("FileTreeBuilder", "Dialog"),
                                                  translate("FileTreeBuilder", "Clipboard")],
                                                 0, "FileTreeBuilderOutputTarget")
        self.cbContentType = Options.MyComboBox(self,
                                                [translate("FileTreeBuilder", "File Tree"),
                                                 translate("FileTreeBuilder", "File List (With Full Path)")],
                                                0, "FileTreeBuilderContentType")
        self.cckbIsShowHiddens = Options.MyCheckBox(self,
                                                    translate("FileTreeBuilder", "Show Hidden Files / Directories"),
                                                    None, "isShowHiddensInFileTree")
        self.cckbFileSize = Options.MyCheckBox(self, translate("FileTreeBuilder", "File Size"), None,
                                               "isAppendFileSizeToFileTree")
        self.cckbLastModified = Options.MyCheckBox(self, translate("FileTreeBuilder", "Last Modified"), None,
                                                   "isAppendLastModifiedToFileTree")
        pbtnBuild = MPushButton(translate("FileTreeBuilder", "Build"))
        pbtnClose = MPushButton(translate("FileTreeBuilder", "Close"))
        self.lePath = MLineEdit(str(_directory))
        pbtnSelectPath = MPushButton(translate("FileTreeBuilder", "Browse"))
        self.connect(pbtnSelectPath, SIGNAL("clicked()"), self.selectPath)
        self.connect(pbtnBuild, SIGNAL("clicked()"), self.build)
        self.connect(pbtnClose, SIGNAL("clicked()"), self.close)
        pnlMain = MWidget(self)
        tabwTabs = MTabWidget()
        vblMain = MVBoxLayout(pnlMain)
        pnlMain2 = MWidget(tabwTabs)
        vblMain2 = MVBoxLayout(pnlMain2)
        HBox = MHBoxLayout()
        HBox.addWidget(self.lePath)
        HBox.addWidget(pbtnSelectPath)
        HBox1 = MHBoxLayout()
        HBox1.addWidget(pbtnBuild)
        HBox1.addWidget(pbtnClose)
        HBox2 = MHBoxLayout()
        HBox2.addWidget(lblOutputTarget)
        HBox2.addWidget(self.cbOutputTarget)
        HBox3 = MHBoxLayout()
        HBox3.addWidget(lblOutputType)
        HBox3.addWidget(self.cbOutputType)
        HBox7 = MHBoxLayout()
        HBox7.addWidget(lblContentType)
        HBox7.addWidget(self.cbContentType)
        HBox4 = MHBoxLayout()
        HBox4.addWidget(lblSubDirectoryDeep)
        HBox4.addWidget(self.cbSubDirectoryDeep)
        HBox5 = MHBoxLayout()
        HBox5.addWidget(self.cckbIsShowHiddens)
        HBox6 = MHBoxLayout()
        HBox6.addWidget(self.cckbFileSize)
        HBox6.addWidget(self.cckbLastModified)
        vblMain2.addWidget(lblDirectory)
        vblMain2.addLayout(HBox)
        vblMain2.addLayout(HBox2)
        vblMain2.addLayout(HBox3)
        vblMain2.addLayout(HBox7)
        vblMain2.addLayout(HBox4)
        gboxFilters = MGroupBox(translate("FileTreeBuilder", "Filters"))
        gboxFilters.setLayout(HBox5)
        vblMain2.addWidget(gboxFilters)
        gboxDetails = MGroupBox(translate("FileTreeBuilder", "Details"))
        gboxDetails.setLayout(HBox6)
        vblMain2.addWidget(gboxDetails)
        vblMain2.addStretch(1)
        vblMain2.addLayout(HBox1)
        tabwTabs.addTab(pnlMain2, translate("FileTreeBuilder", "File Tree"))
        tabwTabs.addTab(wOptionsPanel, translate("FileTreeBuilder", "Quick Options"))
        vblMain.addWidget(tabwTabs)
        if MyDialogType == "MDialog":
            if isActivePyKDE4:
                self.setMainWidget(pnlMain)
            else:
                self.setLayout(vblMain)
        elif MyDialogType == "MMainWindow":
            self.setCentralWidget(pnlMain)
            moveToCenter(self)
        self.setWindowTitle(translate("FileTreeBuilder", "File Tree Builder"))
        self.setWindowIcon(MIcon("Images:fileTree.png"))
        self.setMinimumWidth(450)
        self.show()

    def closeEvent(self, _event):
        MApplication.setQuitOnLastWindowClosed(True)

    def build(self):
        try:
            uni.isCanBeShowOnMainWindow = False
            outputTarget = "file"
            outputType = "html"
            contentType = "fileTree"
            if self.cbOutputTarget.currentIndex() == 1:
                outputTarget = "dialog"
            elif self.cbOutputTarget.currentIndex() == 2:
                outputTarget = "clipboard"
            if self.cbOutputType.currentIndex() == 1:
                outputType = "plainText"
            if self.cbContentType.currentIndex() == 1:
                contentType = "fileList"
            fu.getFileTree(str(self.lePath.text()),
                           self.cbSubDirectoryDeep.currentText(),
                           outputTarget, outputType, contentType, "title")
            if self.cbOutputTarget.currentIndex() == 2:
                Dialogs.show(translate("FileTreeBuilder", "Builded File Tree"),
                             translate("FileTreeBuilder", "File tree copied to clipboard."))
            uni.isCanBeShowOnMainWindow = True
        except:
            ReportBug.ReportBug()

    def selectPath(self):
        try:
            dirPath = Dialogs.getExistingDirectory(translate("FileTreeBuilder", "Please Select"), self.lePath.text(), 0)
            if dirPath is not None:
                self.lePath.setText(str(dirPath))
        except:
            ReportBug.ReportBug()
    
    
                
