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
from InputOutputs import Musics
import InputOutputs
import os,sys
from MyObjects import *
import Dialogs
import Organizer
import Universals
import ReportBug
import Amarok
from Amarok import Operations, Commands

class AmarokArtistDetails(MDialog):
    global amarokArtistDialogs, closeAllAmarokArtistDialogs
    amarokArtistDialogs =[]
    def __init__(self, _artistId, _isOpenDetailsOnNewWindow=True):
        global amarokArtistDialogs
        if Commands.getArtistName(_artistId)!=None:
            if _isOpenDetailsOnNewWindow==False:
                isHasOpenedDialog=False
                for dialog in amarokArtistDialogs:
                    if dialog.isVisible()==True:
                        isHasOpenedDialog=True
                        self = dialog
                        self.changeArtist(_artistId)
                        self.activateWindow()
                        self.raise_()
                        break
                if isHasOpenedDialog==False:
                    _isOpenDetailsOnNewWindow=True
            if _isOpenDetailsOnNewWindow==True:
                amarokArtistDialogs.append(self)
                MDialog.__init__(self, MApplication.activeWindow())
                if Universals.isActivePyKDE4==True:
                    self.setButtons(MDialog.NoDefault)
                self.infoLabels = {}
                self.infoValues = {}
                self.artistValues = {}
                self.pbtnClose = MPushButton(translate("AmarokArtistDetails", "Close"))
                self.pbtnSave = MPushButton(translate("AmarokArtistDetails", "Save Changes"))
                self.pbtnSave.setIcon(MIcon("Images:save.png"))
                MObject.connect(self.pbtnClose, SIGNAL("clicked()"), self.close)
                MObject.connect(self.pbtnSave, SIGNAL("clicked()"), self.save)
                self.labels = [translate("AmarokArtistDetails", "Current Artist: "),
                                translate("AmarokArtistDetails", "Corrected Artist: ")]
                self.songTableColumns = [translate("AmarokArtistDetails", "File Path"), 
                    translate("AmarokArtistDetails", "Artist"), 
                    translate("AmarokArtistDetails", "Title"), 
                    translate("AmarokArtistDetails", "Album"), 
                    translate("AmarokArtistDetails", "Album Artist"), 
                    translate("AmarokArtistDetails", "Track No"), 
                    translate("AmarokArtistDetails", "Year"), 
                    translate("AmarokArtistDetails", "Genre"), 
                    translate("AmarokArtistDetails", "Comment")]
                self.pnlMain = MWidget()
                self.vblMain = MVBoxLayout(self.pnlMain)
                self.pnlClearable = None
                self.changeArtist(_artistId, True)
                
                buttonHBOXs=MHBoxLayout()
                buttonHBOXs.addWidget(self.pbtnSave)
                buttonHBOXs.addWidget(self.pbtnClose)
                self.vblMain.addLayout(buttonHBOXs)
                if Universals.isActivePyKDE4==True:
                    self.setMainWidget(self.pnlMain)
                else:
                    self.setLayout(self.vblMain)
                self.show()
                self.setMinimumWidth(700)
                self.setMinimumHeight(500)
        else:
            Dialogs.showError(translate("AmarokArtistDetails", "Artist Does Not Exist"), 
                    str(translate("AmarokArtistDetails", "\"%s\" does not exist in \"id\" column of \"artist\" table.<br>Table will be refreshed automatically!<br>Please retry.")
                        ) % Organizer.getLink(trForUI(_artistId)))
            if hasattr(Universals.MainWindow, "FileManager"): Universals.MainWindow.FileManager.makeRefresh()
    
    def changeArtist(self, _artistId, _isNew=False):
        self.artistId = _artistId
        self.artistName = Commands.getArtistName(self.artistId)
        self.setWindowTitle(trForUI(self.artistName))  
        if self.pnlClearable != None:
            Universals.clearAllChilds(self.pnlClearable, True)
        self.pnlClearable = MWidget()
        self.vblMain.insertWidget(0, self.pnlClearable, 20)
        vblClearable = MVBoxLayout(self.pnlClearable)    
        self.infoLabels["currentArtist"] = MLabel(self.labels[0]) 
        self.infoLabels["correctedArtist"] = MLabel(self.labels[1]) 
        self.infoValues["currentArtist"] = MLineEdit(trForUI(self.artistName))
        self.infoValues["correctedArtist"] = MLineEdit(trForUI(Organizer.emend(self.artistName)))
        self.songTableContentValues = Commands.getAllMusicFileValuesWithNamesByArtistId(self.artistId)
        self.twSongs = MTableWidget()
        self.twSongs.clear()
        self.twSongs.setColumnCount(len(self.songTableColumns))
        self.twSongs.setHorizontalHeaderLabels(self.songTableColumns)
        self.twSongs.setRowCount(len(self.songTableContentValues))
        for rowNo in range(self.twSongs.rowCount()):
            item = MTableWidgetItem(trForUI(self.songTableContentValues[rowNo]["filePath"]))
            self.twSongs.setItem(rowNo, 0, item)
            item = MTableWidgetItem(trForUI(self.songTableContentValues[rowNo]["artist"]))
            self.twSongs.setItem(rowNo, 1, item)
            item = MTableWidgetItem(trForUI(self.songTableContentValues[rowNo]["title"]))
            self.twSongs.setItem(rowNo, 2, item)
            item = MTableWidgetItem(trForUI(self.songTableContentValues[rowNo]["album"]))
            self.twSongs.setItem(rowNo, 3, item)
            item = MTableWidgetItem(trForUI(self.songTableContentValues[rowNo]["albumartist"]))
            self.twSongs.setItem(rowNo, 4, item)
            item = MTableWidgetItem(trForUI(self.songTableContentValues[rowNo]["tracknumber"]))
            self.twSongs.setItem(rowNo, 5, item)
            item = MTableWidgetItem(trForUI(self.songTableContentValues[rowNo]["year"]))
            self.twSongs.setItem(rowNo, 6, item)
            item = MTableWidgetItem(trForUI(self.songTableContentValues[rowNo]["genre"]))
            self.twSongs.setItem(rowNo, 7, item)
            item = MTableWidgetItem(trForUI(self.songTableContentValues[rowNo]["comment"]))
            self.twSongs.setItem(rowNo, 8, item)
            for x in range(self.twSongs.columnCount()):
                self.twSongs.item(rowNo, x).setFlags(Mt.ItemIsSelectable | Mt.ItemIsEnabled)
        HBOXs = []
        HBOXs.append(MHBoxLayout())
        HBOXs[-1].addWidget(self.infoLabels["currentArtist"])
        HBOXs[-1].addWidget(self.infoValues["currentArtist"])
        HBOXs.append(MHBoxLayout())
        HBOXs[-1].addWidget(self.infoLabels["correctedArtist"])
        HBOXs[-1].addWidget(self.infoValues["correctedArtist"])
        vblInfos = MVBoxLayout()
        for hbox in HBOXs:
            vblInfos.addLayout(hbox)
        vblInfos.addWidget(self.twSongs)
        vblClearable.addLayout(vblInfos)
                                       
    def closeAllAmarokArtistDialogs():
        for dialog in amarokArtistDialogs:
            try:
                if dialog.isVisible()==True:
                    dialog.close()
            except:
                continue
        
    def save(self):
        try:
            import Records
            Records.setTitle(translate("AmarokArtistDetails", "Amarok - Artist"))
            Operations.changeArtistValues([{"id" : self.artistId, "name" : str(self.infoValues["correctedArtist"].text())}])
            if self.artistName!=str(self.infoValues["correctedArtist"].text()):
                self.changeArtist(Commands.getArtistId(str(self.infoValues["correctedArtist"].text())))
            if hasattr(Universals.MainWindow, "FileManager"): Universals.MainWindow.FileManager.makeRefresh()
            Records.saveAllRecords()
        except:
            error = ReportBug.ReportBug()
            error.show()  
    
                        
            
