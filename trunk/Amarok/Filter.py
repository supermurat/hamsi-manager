# This file is part of HamsiManager.
#
# Copyright (c) 2010 - 2014 Murat Demir <mopened@gmail.com>
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
from Core import ReportBug


class FilterWidget(MWidget):
    def __init__(self, _parent, _filterKeyName):
        MWidget.__init__(self, _parent)
        vblMain = MVBoxLayout(self)
        self.filterKeyName = _filterKeyName
        lblFilter = MLabel(translate("Amarok/FilterWidget", "Query:"))
        self.leFilter = MLineEdit(uni.MySettings[self.filterKeyName])
        self.tbEditFilter = MToolButton()
        self.tbEditFilter.setToolTip(translate("Amarok/FilterDialog", "Edit Query"))
        self.tbEditFilter.setIcon(MIcon("Images:edit-rename.png"))
        self.tbApply = MToolButton()
        self.tbApply.setToolTip(translate("Amarok/FilterDialog", "Apply Query"))
        self.tbApply.setIcon(MIcon("Images:view-filter.png"))
        _parent.connect(self.tbEditFilter, SIGNAL("clicked()"), self.editFilter)
        _parent.connect(self.tbApply, SIGNAL("clicked()"), self.apply)
        self.hblBox = MHBoxLayout()
        self.hblBox.addWidget(lblFilter, 1)
        self.hblBox.addWidget(self.leFilter, 20)
        self.hblBox.addWidget(self.tbEditFilter, 1)
        self.hblBox.addWidget(self.tbApply, 2)
        vblMain.addLayout(self.hblBox)
        self.setLayout(vblMain)

    def editFilter(self):
        try:
            self.dFilterEditor = FilterEditor(self, self.filterKeyName)
            self.dFilterEditor.show()
        except:
            ReportBug.ReportBug()

    def apply(self):
        try:
            uni.setMySetting(self.filterKeyName, str(self.leFilter.text()))
            getMainTable().refresh(getMainWindow().FileManager.getCurrentDirectoryPath())
        except:
            ReportBug.ReportBug()


class FilterEditor(MDialog):
    def __init__(self, _parent, _filterKeyName):
        MDialog.__init__(self, _parent)
        self.fWidget = _parent
        if isActivePyKDE4:
            self.setButtons(MDialog.NoDefault)
        pnlMain = MWidget(self)
        vblMain = MVBoxLayout(pnlMain)
        self.filterKeyName = _filterKeyName
        lblFilter = MLabel(translate("Amarok/FilterEditor", "Query"), self)
        self.leFilter = MLineEdit(uni.MySettings[self.filterKeyName], self)
        self.pbtnApply = MPushButton(translate("Amarok/FilterEditor", "Apply Query"), self)
        self.pbtnApply.setIcon(MIcon("Images:view-filter.png"))
        _parent.connect(self.pbtnApply, SIGNAL("clicked()"), self.apply)
        teUsableInformations = MTextEdit("")
        teUsableInformations.setHtml(translate("Amarok/FilterEditor", "filename: some file name (contains)") + "<br>" +
                                     translate("Amarok/FilterEditor", "title: some song title (contains)") + "<br>" +
                                     translate("Amarok/FilterEditor", "artist: some artist name (contains)") + "<br>" +
                                     translate("Amarok/FilterEditor", "album: some album name (contains)") + "<br>" +
                                     translate("Amarok/FilterEditor",
                                               "albumartist: some album artist name (contains)") + "<br>" +
                                     translate("Amarok/FilterEditor", "genre: some genre (contains)") + "<br>" +
                                     translate("Amarok/FilterEditor", "comment: some comment (contains)") + "<br>" +
                                     translate("Amarok/FilterEditor", "rating:5 (equals)") + "<br>" +
                                     translate("Amarok/FilterEditor", "rating:&lt;5 (less than)") + "<br>" +
                                     translate("Amarok/FilterEditor", "rating:&gt;5 (greater than)") + "<br>" +
                                     translate("Amarok/FilterEditor", "year:2000 (equals)") + "<br>" +
                                     translate("Amarok/FilterEditor", "year:&lt;2000 (less than)") + "<br>" +
                                     translate("Amarok/FilterEditor", "year:&gt;2000 (greater than)") + "<br>" +
                                     translate("Amarok/FilterEditor", "<b>Multiple Conditions : </b>") + "<br>" +
                                     translate("Amarok/FilterEditor",
                                               "x:y <b>and</b> t:s (match first and second conditions)") + "<br>" +
                                     translate("Amarok/FilterEditor",
                                               "x:y <b>or</b> t:s (match first or second conditions)"))
        gboxUsableInformations = MGroupBox(translate("Amarok/FilterEditor", "Conditions : "))
        vblBox1 = MVBoxLayout()
        vblBox1.addWidget(teUsableInformations)
        gboxUsableInformations.setLayout(vblBox1)
        self.hblBox = MHBoxLayout()
        self.hblBox.addWidget(lblFilter)
        self.hblBox.addWidget(self.leFilter)
        self.hblBox.addWidget(self.pbtnApply)
        vblMain.addLayout(self.hblBox)
        vblMain.addWidget(gboxUsableInformations)
        if isActivePyKDE4:
            self.setMainWidget(pnlMain)
        else:
            self.setLayout(vblMain)
        self.setWindowTitle(translate("Amarok/FilterEditor", "Edit Query"))
        self.show()
        self.setMinimumWidth(500)
        self.setMinimumHeight(350)
        self.setWindowIcon(MIcon("Images:amarokFilter.png"))

    def apply(self):
        try:
            self.fWidget.leFilter.setText(self.leFilter.text())
            self.fWidget.apply()
        except:
            ReportBug.ReportBug()
        
        
            
    
            
            
            
            
            
            

