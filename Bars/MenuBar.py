## This file is part of HamsiManager.
##
## Copyright (c) 2010 - 2014 Murat Demir <mopened@gmail.com>
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


from Core import Universals as uni
from Core.MyObjects import *
from Core import ReportBug
from Options import QuickOptions


class MenuBar(MMenuBar):
    def __init__(self, _parent):
        MMenuBar.__init__(self, _parent)
        self.mTableTools = None
        self.mQuickOptions = None
        self.mFile = self.addMenu(translate("MenuBar", "File"))
        self.mFile.setObjectName(translate("MenuBar", "File"))
        self.mEdit = self.addMenu(translate("MenuBar", "Edit"))
        self.mEdit.setObjectName(translate("MenuBar", "Edit"))
        self.mView = self.addMenu(translate("MenuBar", "View"))
        self.mView.setObjectName(translate("MenuBar", "View"))
        self.mSettings = self.addMenu(translate("MenuBar", "Settings"))
        self.mSettings.setObjectName(translate("MenuBar", "Settings"))
        if isActivePyKDE4:
            self.mHelpMenu = getMainWindow().helpMenu()
            self.mHelpMenu.setObjectName(self.mHelpMenu.title())
            self.aHelpMenu = self.addMenu(self.mHelpMenu)
        else:
            self.mHelpMenu = self.addMenu(translate("MenuBar", "Help"))
            self.mHelpMenu.setObjectName(translate("MenuBar", "Help"))
        mExport = MMenu(translate("MenuBar", "Export"), self.mEdit)
        mExport.setObjectName(translate("MenuBar", "Export"))
        mExportToFile = MMenu(translate("MenuBar", "Export To File"), self.mEdit)
        mExportToFile.setObjectName(translate("MenuBar", "Export To File"))
        mExportToFile.addAction(translate("MenuBar", "HTML Format")).setObjectName(translate("MenuBar", "HTML Format"))
        mExportToFile.addAction(translate("MenuBar", "Text Format")).setObjectName(translate("MenuBar", "Text Format"))
        mExportToFile.addAction(translate("MenuBar", "HTML Format (File Tree)")).setObjectName(
            translate("MenuBar", "HTML Format (File Tree)"))
        mExportToFile.addAction(translate("MenuBar", "Text Format (File Tree)")).setObjectName(
            translate("MenuBar", "Text Format (File Tree)"))
        mShowInWindow = MMenu(translate("MenuBar", "Show In New Window"), self.mEdit)
        mShowInWindow.setObjectName(translate("MenuBar", "Show In New Window"))
        mShowInWindow.addAction(translate("MenuBar", "HTML Format")).setObjectName(translate("MenuBar", "HTML Format"))
        mShowInWindow.addAction(translate("MenuBar", "Text Format")).setObjectName(translate("MenuBar", "Text Format"))
        mShowInWindow.addAction(translate("MenuBar", "HTML Format (File Tree)")).setObjectName(
            translate("MenuBar", "HTML Format (File Tree)"))
        mShowInWindow.addAction(translate("MenuBar", "Text Format (File Tree)")).setObjectName(
            translate("MenuBar", "Text Format (File Tree)"))
        mCopyToClipBoard = MMenu(translate("MenuBar", "Copy To Clipboard"), self.mEdit)
        mCopyToClipBoard.setObjectName(translate("MenuBar", "Copy To Clipboard"))
        mCopyToClipBoard.addAction(translate("MenuBar", "HTML Format")).setObjectName(
            translate("MenuBar", "HTML Format"))
        mCopyToClipBoard.addAction(translate("MenuBar", "Text Format")).setObjectName(
            translate("MenuBar", "Text Format"))
        mCopyToClipBoard.addAction(translate("MenuBar", "HTML Format (File Tree)")).setObjectName(
            translate("MenuBar", "HTML Format (File Tree)"))
        mCopyToClipBoard.addAction(translate("MenuBar", "Text Format (File Tree)")).setObjectName(
            translate("MenuBar", "Text Format (File Tree)"))
        mExport.addMenu(mExportToFile)
        mExport.addMenu(mShowInWindow)
        mExport.addMenu(mCopyToClipBoard)
        self.mFile.addAction(translate("MenuBar", "Open State")).setObjectName(translate("MenuBar", "Open State"))
        self.mFile.addAction(translate("MenuBar", "Save State")).setObjectName(translate("MenuBar", "Save State"))
        if uni.isRunableAsRoot():
            mRunAsRoot = MMenu(translate("MenuBar", "Run As Root"), self.mFile)
            mRunAsRoot.addAction(translate("MenuBar", "With This Profile (My Settings)")).setObjectName(
                translate("MenuBar", "With This Profile (My Settings)"))
            mRunAsRoot.addAction(translate("MenuBar", "With Root Profile (Own Settings)")).setObjectName(
                translate("MenuBar", "With Root Profile (Own Settings)"))
            self.mFile.addMenu(mRunAsRoot)
        self.mFile.addAction(translate("MenuBar", "Quit")).setObjectName(translate("MenuBar", "Quit"))
        self.mEdit.addMenu(mExport)
        actOptions = self.mSettings.addAction(translate("MenuBar", "Options"))
        actOptions.setObjectName(translate("MenuBar", "Options"))
        actOptions.setIcon(MIcon("Images:options.png"))
        self.mSettings.addAction(translate("MenuBar", "My Plugins")).setObjectName(translate("MenuBar", "My Plugins"))
        self.mSettings.addAction(translate("MenuBar", "Reconfigure")).setObjectName(translate("MenuBar", "Reconfigure"))
        if uni.isRunableAsRoot():
            self.mSettings.addAction(translate("MenuBar", "My Plugins (System)")).setObjectName(
                translate("MenuBar", "My Plugins (System)"))
            self.mSettings.addAction(translate("MenuBar", "Reconfigure (System)")).setObjectName(
                translate("MenuBar", "Reconfigure (System)"))
        if isActivePyKDE4:
            actReportBug = MAction(translate("MenuBar", "Report Bug"), self.mHelpMenu)
            actReportBug.setObjectName(translate("MenuBar", "Report Bug"))
            self.mHelpMenu.insertAction(self.mHelpMenu.actions()[3], actReportBug)
            actSuggestIdea = MAction(translate("MenuBar", "Suggest Idea"), self.mHelpMenu)
            actSuggestIdea.setObjectName(translate("MenuBar", "Suggest Idea"))
            self.mHelpMenu.insertAction(self.mHelpMenu.actions()[3], actSuggestIdea)
            actUNo = 9
            while actUNo > 0:
                try:
                    actUpdate = MAction(translate("MenuBar", "Update"), self.mHelpMenu)
                    actUpdate.setObjectName(translate("MenuBar", "Update"))
                    self.mHelpMenu.insertAction(self.mHelpMenu.actions()[actUNo], actUpdate)
                    break
                except:
                    actUNo -= 3
        else:
            self.mHelpMenu.addAction(translate("MenuBar", "Report Bug")).setObjectName(
                translate("MenuBar", "Report Bug"))
            self.mHelpMenu.addAction(translate("MenuBar", "Suggest Idea")).setObjectName(
                translate("MenuBar", "Suggest Idea"))
            self.mHelpMenu.addAction(translate("MenuBar", "Update")).setObjectName(translate("MenuBar", "Update"))
            self.mHelpMenu.addAction(translate("MenuBar", "About Hamsi Manager")).setObjectName(
                translate("MenuBar", "About Hamsi Manager"))
        self.mHelpMenu.addAction(translate("MenuBar", "About QT")).setObjectName(translate("MenuBar", "About QT"))

        MObject.connect(self, SIGNAL("triggered(QAction *)"), getMainWindow().Bars.click)

    def refreshForTableType(self):
        #self.mView.clear()
        self.mView.addActions(getMainWindow().createPopupMenu().actions())
        self.refreshQuickOptions()

    def refreshQuickOptions(self):
        if getMainWindow().Menu.mQuickOptions is not None:
            getMainWindow().Menu.removeAction(getMainWindow().Menu.mQuickOptions.menuAction())
        getMainWindow().Menu.mQuickOptions = QuickOptions.QuickOptions(self)
        getMainWindow().Menu.insertMenu(getMainWindow().Menu.mSettings.menuAction(), getMainWindow().Menu.mQuickOptions)
        
