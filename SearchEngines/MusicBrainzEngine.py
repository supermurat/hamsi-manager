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


isAvailable = False
try:
    from musicbrainz2 import webservice, model, utils
    from musicbrainz2.webservice import Query, ArtistFilter, WebServiceError, ReleaseFilter, TrackFilter
    isAvailable = True
except:pass
from MyObjects import *
import Dialogs
import time
import Universals
pluginName = "MusicBrainz"

class Search(MDialog):

    def __init__(self, _parent, _isCheckSingleFile=False, _searchDepth=3):
        MDialog.__init__(self, _parent)
        if Universals.isActivePyKDE4==True:
            self.setButtons(MDialog.NoDefault)
        self.isCheckSingleFile = _isCheckSingleFile
        self.searchDepth = _searchDepth
        self.nullSongs, self.falseSongs, self.trueSongs, self.songsOfArtist, self.songsOfAlbum, self.cbTags, self.leTags, self.incorrectSongs = [], [], [], [], [], [], [], []
        self.searchedArtists, self.searchedTitles, self.searchedAlbums = [[], []], [[], []], [[], []]
        self.searchedAlbumsOfArtist, self.searchedSongsOfAlbum, self.searchedDetailsOfArtist, self.searchedDetailsOfAlbum = [[], []], [[], []], [[], []], [[], []]
        self.showSuggest(True)
        self.isAlterAlbum = False
        self.isArtistImportant = True
        self.isArtistChanged = False
        self.isAlterArtist = True
        self.setModal(True)
        self.prgbState = MProgressBar()
        self.prgbAllState = MProgressBar()
        self.prgbStateLabel = MLabel(translate("SearchEngines", "Current Proccess"))
        self.prgbAllStateLabel = MLabel(translate("SearchEngines", "General"))
        self.pbtnApply = MPushButton(translate("SearchEngines", "Apply"))
        self.pbtnApply.setMaximumWidth(120)
        self.pbtnApply.setVisible(False)
        self.pbtnCancel = MPushButton(translate("SearchEngines", "Cancel"))
        self.pbtnCancel.setMaximumWidth(120)
        self.pbtnClose = MPushButton(translate("SearchEngines", "Close"))
        self.pbtnClose.setMaximumWidth(120)
        self.pbtnClose.setVisible(False)
        MObject.connect(self.pbtnApply,SIGNAL("clicked()"),self.apply)
        MObject.connect(self.pbtnClose,SIGNAL("clicked()"),self.close)
        MObject.connect(self.pbtnCancel, SIGNAL("clicked()"), Universals.cancelThreadAction)
        pnlMain = MWidget(self)
        self.saPanel = MScrollArea(pnlMain)
        self.vblPanel = MVBoxLayout()
        self.vblPanel.setAlignment(Mt.AlignHCenter)
        self.vblPanel.setAlignment(Mt.AlignTop)
        self.vblPanel.addWidget(self.prgbStateLabel)
        self.vblPanel.addWidget(self.prgbState)
        self.vblPanel.addWidget(self.prgbAllStateLabel)
        self.vblPanel.addWidget(self.prgbAllState)
        self.pnlPanel = MWidget(pnlMain)
        self.pnlPanel.setLayout(self.vblPanel)
        self.pnlPanel.setFixedSize(595,100)
        self.saPanel.setWidget(self.pnlPanel)
        self.saPanel.setFrameShape(MFrame.StyledPanel)
        self.saPanel.setAlignment(Mt.AlignHCenter)
        self.saPanel.setFixedSize(645,110)
        vblBox = MVBoxLayout(pnlMain)
        vblBox.addWidget(self.saPanel)
        hblBox = MHBoxLayout()
        hblBox.addStretch(2)
        hblBox.addWidget(self.pbtnCancel)
        hblBox.addWidget(self.pbtnClose)
        hblBox.addWidget(self.pbtnApply)
        vblBox.addLayout(hblBox)
        if Universals.isActivePyKDE4==True:
            self.setMainWidget(pnlMain)
        else:
            self.setLayout(vblBox)
        self.setWindowTitle(translate("SearchEngines", "Searching Information On The Internet!.."))
        self.setFixedSize(670,160)
        self.setAttribute(Mt.WA_DeleteOnClose)
        self.show()
        self.connect(self, SIGNAL("changedProgressBarValue"), self.changeProgressBarValue)
        import MyThread
        myProcs = MyThread.MyThread(self.startSearch, self.finishSearch)
        myProcs.start()
        
    def closeEvent(self, _event):
        if Universals.isContinueThreadAction():
            Universals.cancelThreadAction()
            _event.ignore()
        
    def changeProgressBarValue(self, _progressBarName, _value):
        if _progressBarName=="AllState":
            self.prgbAllState.setValue(_value)
            self.prgbAllState.repaint()
        elif _progressBarName=="State":
            self.prgbState.setValue(_value)
            self.prgbState.repaint()
        
    def startSearch(self):
        if self.isCheckSingleFile:
            self.prgbAllState.setRange(0,1)
            self.rows = range(Universals.MainWindow.Table.currentRow(), Universals.MainWindow.Table.currentRow()+1)
            self.heightValue = 150
        else:
            self.prgbAllState.setRange(0,Universals.MainWindow.Table.rowCount())
            self.rows = range(Universals.MainWindow.Table.rowCount())
            if Universals.MainWindow.Table.rowCount()<7:
                self.heightValue = 300
            else:
                self.heightValue = 500
        tagsOfSongs = []
        for rowNo in self.rows:
            tagsOfSongs.append([str(Universals.MainWindow.Table.item(rowNo,2).text()),
                               str(Universals.MainWindow.Table.item(rowNo,3).text()),
                               str(Universals.MainWindow.Table.item(rowNo,4).text()), rowNo])
        Universals.startThreadAction()
        for tagsOfSong in tagsOfSongs:
            isContinueThreadAction = Universals.isContinueThreadAction()
            if isContinueThreadAction:
                try:
                    self.checkIt(tagsOfSong, self.searchDepth)
                except webservice.WebServiceError as errorDetails:
                    Dialogs.showError(translate("SearchEngines", "An Error Occured"),
                                str(translate("SearchEngines", "Please retry the process.<br>If you receive the same error, please try the other search engines.<br><b>Error details:</b><br>%s")) % (str(errorDetails)))
                except ValueError as errorDetails:
                    Dialogs.showError(translate("SearchEngines", "An Error Occured"),
                                str(translate("SearchEngines", "Fetching information for the music file that caused the error is canceled.<br>If you receive the same error, please try the other search engines.<br><b>Error details:</b><br>%s")) % (str(errorDetails)))
                    self.incorrectSongs.append([[Universals.MainWindow.Table.item(tagsOfSong[3],1).text()], [tagsOfSong[0]], [tagsOfSong[1]], [tagsOfSong[2]], tagsOfSong[3]])
                self.emit(SIGNAL("changedProgressBarValue"), "AllState", tagsOfSong[3]+1)
        Universals.finishThreadAction()
        return True
            
    def finishSearch(self, _isContinue):
        if _isContinue:
            self.prgbState.setVisible(False)
            self.prgbAllState.setVisible(False)
            self.prgbStateLabel.setVisible(False)
            self.prgbAllStateLabel.setVisible(False)
            self.showInList()
            self.pbtnCancel.setVisible(False)
            self.pbtnClose.setVisible(True)
            self.pbtnApply.setVisible(True)
            self.setMinimumSize(670,self.heightValue+50)
            self.saPanel.setFixedSize(645,self.heightValue)
        
    def checkIt(self, _tagsOfSong, _searchDepth):
        self.prgbState.setRange(0,100)
        if _tagsOfSong[1].strip()!="":
            searchType = "Title"
            self.emit(SIGNAL("changedProgressBarValue"), "State", 2)
        elif _tagsOfSong[2].strip()!="":
            searchType = "Album"
            self.emit(SIGNAL("changedProgressBarValue"), "State", 10)
        elif _tagsOfSong[0].strip()!="":
            searchType = "Artist"
            self.emit(SIGNAL("changedProgressBarValue"), "State", 20)
        else:
            self.emit(SIGNAL("changedProgressBarValue"), "State", 100)
            self.nullSongs.append([[self.parent().item(_tagsOfSong[3],1).text()], [_tagsOfSong[0]], [_tagsOfSong[1]], [_tagsOfSong[2]], _tagsOfSong[3]])
            return
        if searchType=="Title":
            titles = self.getSongsFromTitle(_tagsOfSong[1].strip())
            if len(titles)!=0:
                self.emit(SIGNAL("changedProgressBarValue"), "State", 90)
                for title in titles:
                    if str(title[2]).lower()==str(_tagsOfSong[1]).lower():
                        if str(title[5]).lower()==str(_tagsOfSong[2]).lower():
                            if str(title[7]).lower()==str(_tagsOfSong[0]).lower():
                                self.trueSongs.append([_tagsOfSong[0], _tagsOfSong[1], _tagsOfSong[2], _tagsOfSong[3], _tagsOfSong[0], _tagsOfSong[1], _tagsOfSong[2]])
                                return
                artistNames, albumNames, titleNames=[], [], []
                for title in titles:
                    if artistNames.count(title[7])==0:
                        artistNames.append(title[7])
                    if titleNames.count(title[2])==0:
                        titleNames.append(title[2])
                    if albumNames.count(title[5])==0:
                        albumNames.append(title[5])
                self.falseSongs.append([artistNames, titleNames, albumNames, _tagsOfSong[3], _tagsOfSong[0], _tagsOfSong[1], _tagsOfSong[2]])
            else:
                searchType = "Album"
        if searchType=="Album":
            albums = self.getAlbumsFromAlbum(_tagsOfSong[2].strip())
            if len(albums)!=0:
                self.emit(SIGNAL("changedProgressBarValue"), "State", 60)
                artistNames, albumNames, titleNames=[], [], []
                for album in albums:
                    if artistNames.count(album[7])==0:
                        artistNames.append(album[7])
                        albumNames.append([])
                        titleNames.append([])
                        artistNo = -1
                    else:
                        artistNo = artistNames.index(album[7])
                    albumNames[artistNo].append(album[2])
                    titleNames[artistNo].append([])
                    titles = self.getSongsOfAlbum(album[1])
                    self.emit(SIGNAL("changedProgressBarValue"), "State", 90)
                    if len(titles)!=0:
                        for title in titles:
                            titleNames[artistNo][-1].append(title[1])
                self.songsOfAlbum.append([artistNames,titleNames,albumNames, _tagsOfSong[3],_tagsOfSong[0], _tagsOfSong[1],_tagsOfSong[2]])   
            else:
                searchType = "Artist"
        if searchType=="Artist":
            artists = self.getArtistsFromArtist(_tagsOfSong[0].strip())
            if len(artists)!=0:
                self.emit(SIGNAL("changedProgressBarValue"), "State", 40)
                artistNames, albumNames, titleNames=[], [], []
                for artist in artists:
                    artistNames.append(artist[2])
                    albumNames.append([])
                    titleNames.append([])
                    albums = self.getAlbumsOfArtist(artist[1], _searchDepth)
                    if len(albums)!=0:
                        self.emit(SIGNAL("changedProgressBarValue"), "State", 65)
                        for album in albums:
                            albumNames[-1].append(album[1])
                            titleNames[-1].append([])
                            titles = self.getSongsOfAlbum(album[0])
                            if len(titles)!=0:
                                self.emit(SIGNAL("changedProgressBarValue"), "State", 90)
                                for title in titles:
                                    titleNames[-1][-1].append(title[1])
                self.songsOfArtist.append([artistNames,titleNames,albumNames, _tagsOfSong[3],_tagsOfSong[0], _tagsOfSong[1],_tagsOfSong[2]])
            else:
                self.nullSongs.append([[self.parent().item(_tagsOfSong[3],1).text()], [_tagsOfSong[0]], [_tagsOfSong[1]], [_tagsOfSong[2]], _tagsOfSong[3]])

    def getArtistsFromArtist(self, _artistName):
        """Returns artists that are similar to the one selected.
        Returned[x][0]:Match             Returned[x][1]:Artist ID
        Returned[x][2]:Name              Returned[x][3]:Nickname"""
        try:
            return self.searchedArtists[1][self.searchedArtists[0].index(_artistName)]
        except:pass
        self.searchedArtists[0].append(_artistName)
        values, controlValue=[], 1
        while controlValue>0 and controlValue<4:
            try:
                returnedValues = Query().getArtists(ArtistFilter(_artistName, limit=5))
                controlValue=0
            except webservice.WebServiceError as errorDetails:
                if str(errorDetails)[:15]=="HTTP Error 503:":
                    time.sleep(controlValue)
                    controlValue+=1
                else:
                    raise ValueError(errorDetails)
        for result in returnedValues:
            values.append([result.score, result.artist.id, result.artist.name, result.artist.sortName])
        self.searchedArtists[1].append(values)
        return values

    def getAlbumsFromAlbum(self, _albumName):
        """Returns albums that are similar to the one selected.
        Returned[x][0]:Match            Returned[x][1]:Id
        Returned[x][2]:Name             Returned[x][3]:Asin
        Returned[x][4]:Text             Returned[x][5]:Genre
        Returned[x][6]:Artist Id	      Returned[x][7]:Artist Name"""
        try:
            return self.searchedAlbums[1][self.searchedAlbums[0].index(_albumName)]
        except:pass
        self.searchedAlbums[0].append(_albumName)
        values, controlValue=[], 1
        while controlValue>0 and controlValue<4:
            try:
                returnedValues = Query().getReleases(ReleaseFilter(query=_albumName))
                controlValue=0
            except webservice.WebServiceError as errorDetails:
                if str(errorDetails)[:15]=="HTTP Error 503:":
                    time.sleep(controlValue)
                    controlValue+=1
                else:
                    raise ValueError(errorDetails)
        for result in returnedValues:
            values.append([result.score, result.release.id, result.release.title, result.release.asin,(result.release.textLanguage, "/", result.release.textScript), result.release.types, result.release.artist.id, result.release.artist.name])
        self.searchedAlbums[1].append(values)
        return values    

    def getSongsFromTitle(self, _titleName):
        """Returns titles that are similar to the one selected.
        Returned[x][0]:Match		    Returned[x][1]:Id              
        Returned[x][2]:Title		    Returned[x][3]:Length
        Returned[x][4]:Album Id		  Returned[x][5]:Album Name
        Returned[x][6]:Artist Id	  Returned[x][7]:Artist Name"""
        try:
            return self.searchedTitles[1][self.searchedTitles[0].index(_titleName)]
        except:pass
        self.searchedTitles[0].append(_titleName)
        values, controlValue=[], 1
        while controlValue>0 and controlValue<4:
            try:
                returnedValues = Query().getTracks(TrackFilter(query=_titleName))
                controlValue=0
            except webservice.WebServiceError as errorDetails:
                if str(errorDetails)[:15]=="HTTP Error 503:":
                    time.sleep(controlValue)
                    controlValue+=1
                else:
                    raise ValueError(errorDetails)
        for result in returnedValues:
            values.append([result.score, result.track.id, result.track.title, result.track.duration,result.track.releases[0].id ,result.track.releases[0].title ,result.track.artist.id ,result.track.artist.name ])
        self.searchedTitles[1].append(values)
        return values

    def getDetailsOfArtist(self, _artistId):
        """Returns all details for the selected artist ID.
        Returned[0]:Id			    Returned[1]:Name
        Returned[2]:Nickname		Returned[3]:Unique Name
        Returned[4]:Genre		    Returned[5]:Beginning Date
        Returned[6]:End Date		Returned[7]:Tags"""
        try:
            return self.searchedDetailsOfArtist[1][self.searchedDetailsOfArtist[0].index(_artistId)]
        except:pass
        self.searchedDetailsOfArtist[0].append(_artistId)
        controlValue=1
        while controlValue>0 and controlValue<4:
            try:
                q = Query()
                inc = webservice.ArtistIncludes(tags=True)
                artist = q.getArtistById(_artistId, inc)
                controlValue=0
            except webservice.WebServiceError as errorDetails:
                if str(errorDetails)[:15]=="HTTP Error 503:":
                    time.sleep(controlValue)
                    controlValue+=1
                else:
                    raise ValueError(errorDetails)
        values = [artist.id, artist.name, artist.sortName, artist.getUniqueName(), artist.type, artist.beginDate, artist.endDate, ", ".join(t.value for t in artist.tags)]
        self.searchedDetailsOfArtist[1].append(values)
        return values

    def getAlbumsOfArtist(self, _artistId, _searchDepth):
        """Returns all albums for the selected artist ID.
        Returned[x][0]:Id               Returned[x][1]:Title
        Returned[x][2]:Asin             Returned[x][3]:Text
        Returned[x][4]:Genre"""
        try:
            return self.searchedAlbumsOfArtist[1][self.searchedAlbumsOfArtist[0].index(_artistId)]
        except:pass
        self.searchedAlbumsOfArtist[0].append(_artistId)
        values=[]
        albumTypes = [model.Release.TYPE_ALBUM, model.Release.TYPE_SINGLE, model.Release.TYPE_COMPILATION, 
                        model.Release.TYPE_SOUNDTRACK, model.Release.TYPE_REMIX, model.Release.TYPE_SPOKENWORD, 
                        model.Release.TYPE_INTERVIEW, model.Release.TYPE_AUDIOBOOK, model.Release.TYPE_LIVE, 
                        model.Release.TYPE_EP, model.Release.TYPE_OTHER]
        albumStates = [model.Release.TYPE_OFFICIAL, model.Release.TYPE_PROMOTION, 
                          model.Release.TYPE_BOOTLEG, model.Release.TYPE_PSEUDO_RELEASE]
        for albumStateNo, albumState in enumerate(albumStates):
            if albumStateNo==0 or (albumStateNo==1 and _searchDepth>4) or (albumStateNo==2 and _searchDepth>7) or (albumStateNo==3 and _searchDepth>10):
                for albumTypeNo, albumType in enumerate(albumTypes):
                    if albumTypeNo<=_searchDepth:
                        controlValue = 1
                        while controlValue>0 and controlValue<4:
                            try:
                                q = Query()
                                inc = webservice.ArtistIncludes(releases=(albumState, albumType),tags=True)
                                artist = q.getArtistById(_artistId, inc)
                                controlValue=0
                            except webservice.WebServiceError as errorDetails:
                                if str(errorDetails)[:15]=="HTTP Error 503:":
                                    time.sleep(controlValue)
                                    controlValue+=1
                                else:
                                    raise ValueError(errorDetails)
                        for release in artist.getReleases():
                            values.append([release.id, release.title, release.asin, (release.textLanguage, "/", release.textScript), release.types])
        self.searchedAlbumsOfArtist[1].append(values)
        return values

    def getDetailsOfAlbum(self, _albumId):
        """Returns all details for the selected album ID.
        Returned[0]:Id              			  Returned[1]:Title
        Returned[2]:Asin	                	Returned[3]:Language
        Returned[4]:Artist ID	  	        	Returned[5]:Artist Name
        Returned[6]:Artist Nickname			    Returned[7]:First Release Date
        Returned[8]:Release Dates(By the countries)
        Returned[8][0]:Country				      Returned[8][1]:Release Date
        Returned[8][2]:Catalogue no			    Returned[8][3]:BarCode
        Returned[8][4]:Label name
        Returned[9]:CDs
        Returned[9][0]:CD ID				        Returned[9][1]:Disc Sector"""
        try:
            return self.searchedDetailsOfAlbum[1][self.searchedDetailsOfAlbum[0].index(_albumId)]
        except:pass
        self.searchedDetailsOfAlbum[0].append(_albumId)
        controlValue=1
        while controlValue>0 and controlValue<4:
            try:
                q = webservice.Query()
                inc = webservice.ReleaseIncludes(artist=True, releaseEvents=True, labels=True, discs=True, tracks=True)
                release = q.getReleaseById(_albumId, inc)
                controlValue=0
            except webservice.WebServiceError as errorDetails:
                if str(errorDetails)[:15]=="HTTP Error 503:":
                    time.sleep(controlValue)
                    controlValue+=1
                else:
                    raise ValueError(errorDetails)
        releaseDates=[]
        for event in release.releaseEvents:
            releaseDates.append([utils.getCountryName(event.country), event.date, 
                                ("#" + event.catalogNumber), 
                                ("EAN=" + event.barcode), 
                                ("(" + event.label.name + ")")])
        diskler=[]
        for disc in release.discs:
            diskler.append([disc.id, disc.sectors])
        values = [release.id, release.title, release.asin, (release.textLanguage, "/", release.textScript), 
                release.artist.id, release.artist.name, release.artist.sortName, 
                release.getEarliestReleaseDate(), releaseDates, diskler]
        self.searchedDetailsOfAlbum[1].append(values)
        return values

    def getSongsOfAlbum(self, _albumId):
        """Returns all titles for the selected album ID..
        Returned[x][0]:Id               Returned[x][1]:Title
        Returned[x][2]:Length"""
        try:
            return self.searchedSongsOfAlbum[1][self.searchedSongsOfAlbum[0].index(_albumId)]
        except:pass
        self.searchedSongsOfAlbum[0].append(_albumId)
        values, controlValue=[], 1
        while controlValue>0 and controlValue<4:
            try:
                q = webservice.Query()
                inc = webservice.ReleaseIncludes(artist=True, releaseEvents=True, labels=True, discs=True, tracks=True)
                release = q.getReleaseById(_albumId, inc)
                controlValue=0
            except webservice.WebServiceError as errorDetails:
                if str(errorDetails)[:15]=="HTTP Error 503:":
                    time.sleep(controlValue)
                    controlValue+=1
                else:
                    raise ValueError(errorDetails)
        for track in release.tracks:
            values.append([track.id, track.title, track.duration])
        self.searchedSongsOfAlbum[1].append(values)
        return values

    def getArtistIdFromArtist(self, _artistName):
        for artists in self.searchedArtists[1]:
            for artist in artists:
                if artist[2]==_artistName:
                    return artist[1]
        for albums in self.searchedAlbums[1]:
            for album in albums:
                if album[7]==_artistName:
                    return album[6]
        for titles in self.searchedTitles[1]:
            for title in titles:
                if title[7]==_artistName:
                    return title[6]
        return -1
        
    def getAlbumIdFromAlbum(self, _albumName):
        for albums in self.searchedAlbums[1]:
            for album in albums:
                if album[2]==_albumName:
                    return album[1]
        for titles in self.searchedTitles[1]:
            for title in titles:
                if title[5]==_albumName:
                    return title[4]
        for albums in self.searchedAlbumsOfArtist[1]:
            for album in albums:
                if album[1]==_albumName:
                    return album[0]
        return -1
        
    def getTitleIdFromTitle(self, _titleName):
        for titles in self.searchedTitles[1]:
            for title in titles:
                if title[2]==_titleName:
                    return title[1]
        for titles in self.searchedSongsOfAlbum[1]:
            for title in titles:
                if title[1]==_titleName:
                    return title[0]
        return -1
        
    def showInList(self):
        HBoxs=[]
        if len(self.trueSongs)>0 or len(self.falseSongs)>0 or len(self.songsOfAlbum)>0 or len(self.songsOfArtist)>0:
            tagNames = [translate("MusicTable", "Artist"), 
                        translate("MusicTable", "Title"), 
                        translate("MusicTable", "Album")]
            tagNamesKeys = ["Artist", "Title","Album", "File Name"]
            HBoxs.append(MHBoxLayout())
            HBoxs[-1].addWidget(MLabel(tagNames[0]))
            HBoxs[-1].addWidget(MLabel(tagNames[1]))
            HBoxs[-1].addWidget(MLabel(tagNames[2]))
            if len(self.trueSongs)>0:
                HBoxs.append(MHBoxLayout())
                HBoxs[-1].addWidget(MLabel(translate("SearchEngines", "Songs identified correctly:")))
                for song in self.trueSongs:
                    HBoxs.append(MHBoxLayout())
                    for no in range(len(tagNames)):
                        self.cbTags.append(MComboBox())
                        self.cbTags[-1].setObjectName(tagNamesKeys[no]+str(song[3]))
                        self.cbTags[-1].setEditable(True)
                        self.cbTags[-1].setMaximumWidth(200)
                        self.cbTags[-1].setMinimumWidth(200)
                        self.cbTags[-1].setToolTip(trForUI(song[no+4]))
                        for tag in song[no]:
                            self.cbTags[-1].addItem(trForUI(tag))
                        HBoxs[-1].addWidget(self.cbTags[-1])
            if len(self.falseSongs)>0:
                HBoxs.append(MHBoxLayout())
                HBoxs[-1].addWidget(MLabel(translate("SearchEngines", "Songs identified correctly but with errors:")))
                for song in self.falseSongs:
                    HBoxs.append(MHBoxLayout())
                    for no in range(len(tagNames)):
                        self.cbTags.append(MComboBox())
                        self.cbTags[-1].setObjectName(tagNamesKeys[no]+str(song[3]))
                        self.cbTags[-1].setEditable(True)
                        self.cbTags[-1].setMaximumWidth(200)
                        self.cbTags[-1].setMinimumWidth(200)
                        self.cbTags[-1].setToolTip(trForUI(song[no+4]))
                        for tag in song[no]:
                            self.cbTags[-1].addItem(trForUI(tag))
                        HBoxs[-1].addWidget(self.cbTags[-1])
            if len(self.songsOfAlbum)>0:
                HBoxs.append(MHBoxLayout())
                HBoxs[-1].addWidget(MLabel(translate("SearchEngines", "Songs searched with album name:")))
                for song in self.songsOfAlbum:
                    HBoxs.append(MHBoxLayout())
                    for no in range(len(tagNames)):
                        self.cbTags.append(MComboBox())
                        self.cbTags[-1].setObjectName(tagNamesKeys[no]+str(song[3]))
                        self.cbTags[-1].setEditable(True)
                        self.cbTags[-1].setMaximumWidth(200)
                        self.cbTags[-1].setMinimumWidth(200)
                        self.cbTags[-1].setToolTip(trForUI(song[no+4]))
                        HBoxs[-1].addWidget(self.cbTags[-1])
                        if no==0:
                            for tag in song[no]:
                                if self.cbTags[-1].findText(trForUI(tag))==-1:
                                    self.cbTags[-1].addItem(trForUI(tag))
                            self.cbTags[-1].addItem(translate("SearchEngines", "All Artists"))
                            MObject.connect(self.cbTags[-1],SIGNAL("currentIndexChanged(int)"),self.artistChanged)
                        elif no==1:
                            for tag in song[no]:
                                for t in tag:
                                    for bil in t:
                                        if self.cbTags[-1].findText(trForUI(bil))==-1:
                                            self.cbTags[-1].addItem(trForUI(bil))
                        elif no==2:
                            for tag in song[no]:
                                for t in tag:
                                    if self.cbTags[-1].findText(trForUI(t))==-1:
                                        self.cbTags[-1].addItem(trForUI(t))
                            self.cbTags[-1].addItem(translate("SearchEngines", "All Albums"))   
                            MObject.connect(self.cbTags[-1],SIGNAL("currentIndexChanged(int)"),self.albumChanged)
            if len(self.songsOfArtist)>0:
                HBoxs.append(MHBoxLayout())
                HBoxs[-1].addWidget(MLabel(translate("SearchEngines", "Songs searched with artist name:")))
                for song in self.songsOfArtist:
                    HBoxs.append(MHBoxLayout())
                    for no in range(len(tagNames)):
                        self.cbTags.append(MComboBox())
                        self.cbTags[-1].setObjectName(tagNamesKeys[no]+str(song[3]))
                        self.cbTags[-1].setEditable(True)
                        self.cbTags[-1].setMaximumWidth(200)
                        self.cbTags[-1].setMinimumWidth(200)
                        self.cbTags[-1].setToolTip(trForUI(song[no+4]))
                        HBoxs[-1].addWidget(self.cbTags[-1])
                        if no==0:
                            for tag in song[no]:
                                if self.cbTags[-1].findText(trForUI(tag))==-1:
                                    self.cbTags[-1].addItem(trForUI(tag))
                            self.cbTags[-1].addItem(translate("SearchEngines", "All Artists"))
                            MObject.connect(self.cbTags[-1],SIGNAL("currentIndexChanged(int)"),self.artistChanged)
                        elif no==1:
                            for tag in song[no]:
                                for t in tag:
                                    for s in t:
                                        if self.cbTags[-1].findText(trForUI(s))==-1:
                                            self.cbTags[-1].addItem(trForUI(s))
                        elif no==2:
                            for tag in song[no]:
                                for t in tag:
                                    if self.cbTags[-1].findText(trForUI(t))==-1:
                                        self.cbTags[-1].addItem(trForUI(t))
                            self.cbTags[-1].addItem(translate("SearchEngines", "All Albums"))    
                            MObject.connect(self.cbTags[-1],SIGNAL("currentIndexChanged(int)"),self.albumChanged)
        if len(self.nullSongs)>0:
            tagNames = [translate("MusicTable", "File Name"), 
                        translate("MusicTable", "Artist"), 
                        translate("MusicTable", "Title"), 
                        translate("MusicTable", "Album")]
            tagNamesKeys = ["File Name", "Artist", "Title", "Album"]
            HBoxs.append(MHBoxLayout())
            HBoxs[-1].addWidget(MLabel(tagNames[0]))
            HBoxs[-1].addWidget(MLabel(tagNames[1]))
            HBoxs[-1].addWidget(MLabel(tagNames[2]))
            HBoxs[-1].addWidget(MLabel(tagNames[3]))
            HBoxs.append(MHBoxLayout())
            HBoxs[-1].addWidget(MLabel(translate("SearchEngines", "Songs identified incorrectly:")))
            for song in self.nullSongs:
                HBoxs.append(MHBoxLayout())
                for no in range(len(tagNames)):
                    self.cbTags.append(MComboBox())
                    self.cbTags[-1].setObjectName(tagNamesKeys[no]+str(song[4]))
                    self.cbTags[-1].setEditable(True)
                    self.cbTags[-1].setMaximumWidth(150)
                    self.cbTags[-1].setMinimumWidth(150)
                    for tag in song[no]:
                        self.cbTags[-1].addItem(trForUI(tag))
                    HBoxs[-1].addWidget(self.cbTags[-1])
        if len(self.incorrectSongs)>0:
            tagNames= [tagNames[0], tagNames[1], tagNames[2], translate("MusicTable", "File Name")]
            HBoxs.append(MHBoxLayout())
            HBoxs[-1].addWidget(MLabel(tagNames[0]))
            HBoxs[-1].addWidget(MLabel(tagNames[1]))
            HBoxs[-1].addWidget(MLabel(tagNames[2]))
            HBoxs[-1].addWidget(MLabel(tagNames[3]))
            HBoxs.append(MHBoxLayout())
            HBoxs[-1].addWidget(MLabel(translate("SearchEngines", "Songs that caused errors:")))
            for song in self.incorrectSongs:
                HBoxs.append(MHBoxLayout())
                for no in range(len(tagNames)):
                    self.cbTags.append(MComboBox())
                    self.cbTags[-1].setObjectName(tagNamesKeys[no]+str(song[4]))
                    self.cbTags[-1].setEditable(True)
                    self.cbTags[-1].setMaximumWidth(150)
                    self.cbTags[-1].setMinimumWidth(150)
                    self.cbTags[-1].setToolTip(trForUI(song[no+4]))
                    for tag in song[no]:
                        self.cbTags[-1].addItem(trForUI(tag))
                    HBoxs[-1].addWidget(self.cbTags[-1])
        for box in HBoxs:
            self.vblPanel.addLayout(box)
        self.pnlPanel.setFixedSize(620,len(HBoxs)*30)
        self.checkSuggest()

    
    def checkSuggest(self):
        if len(self.searchedAlbums[0])==1 and len(self.rows)>1:
            self.sortBySelectedAlbum()
        if len(self.searchedArtists[0])==1 and len(self.rows)>1:
            self.showSuggest()
    
    def selectAlbum(self):
        for rowNo in self.rows:
            if len(self.rows)-1!=self.rows[-1]:
                rowNo=rowNo/2
            self.findChild(MComboBox, "Album"+str(rowNo)).setCurrentIndex(self.findChild(MComboBox, "Album0").currentIndex())
    
    def sortBySelectedAlbum(self):
        for rowNo in self.rows:
            if len(self.rows)-1!=self.rows[-1]:
                rowNo=rowNo/2
            self.findChild(MComboBox, "Title"+str(rowNo)).setCurrentIndex(rowNo)

    def showSuggest(self, _isHidden=False):
        self.lblSuggest = MLabel(self)
        self.pbtnSuggest = MPushButton("", self)
        self.pbtnSuggest.setFlat(True)
        self.movie = MMovie("Images:suggest.gif")
        self.lblSuggest.setMovie(self.movie)
        self.movie.start()
        if _isHidden:
            self.pbtnSuggest.setVisible(False)
            self.lblSuggest.setVisible(False)
        else:
            self.lblSuggest.setGeometry(600, 25, 30, 30)
            self.pbtnSuggest.setGeometry(600, 30, 20, 20)
            self.mSuggest = MMenu(self)
            self.mSuggest.clear()
            self.labelsOfSuggests = [translate("SearchEngines", "Sort Titles By Album")]
            for label in self.labelsOfSuggests:
                action = MAction(label, self.mSuggest)
                action.setObjectName(label)
                self.mSuggest.addAction(action)
            MObject.connect(self.mSuggest,SIGNAL("triggered(QAction *)"),self.applySuggest)
            self.mSuggest.setGeometry(self.pbtnSuggest.x()+10,self.pbtnSuggest.y()+10,
                                       self.mSuggest.width(),self.mSuggest.height())
            self.pbtnSuggest.setMenu(self.mSuggest)
            self.lblSuggest.setVisible(True)
            self.pbtnSuggest.setVisible(True)
            
    def applySuggest(self, _action):
        if str(_action.objectName()) == str(self.labelsOfSuggests[0]):
            isPracticable = True
            id= self.getAlbumIdFromAlbum(self.findChild(MComboBox, "Album0").currentText())
            if len(self.rows)!=len(self.getSongsOfAlbum(id)):
                isPracticable = False
                answer = Dialogs.ask(translate("SearchEngines", "Number Of Songs Are Different"), 
                                translate("SearchEngines", "The number of songs for the album you selected is not the same with the album you have verified.<br>Do you want to sort by the album anyway?"))
                if answer==Dialogs.Yes:
                    isPracticable = True
            if isPracticable:
                self.selectAlbum()
                self.sortBySelectedAlbum()
            
    def apply(self):
        self.parent().createHistoryPoint()
        songs=[]
        for tag in self.trueSongs:
            artist = str(self.findChild(MComboBox, trForUI("Artist"+str(tag[3]))).currentText())
            title = str(self.findChild(MComboBox, trForUI("Title"+str(tag[3]))).currentText())
            album = str(self.findChild(MComboBox, trForUI("Album"+str(tag[3]))).currentText())
            songs.append([artist,title,album,tag[3]])   
        for tag in self.falseSongs:
            artist = str(self.findChild(MComboBox, trForUI("Artist"+str(tag[3]))).currentText())
            title = str(self.findChild(MComboBox, trForUI("Title"+str(tag[3]))).currentText())
            album = str(self.findChild(MComboBox, trForUI("Album"+str(tag[3]))).currentText())
            songs.append([artist,title,album,tag[3]])
        for tag in self.songsOfAlbum:
            artist = str(self.findChild(MComboBox, trForUI("Artist"+str(tag[3]))).currentText())
            title = str(self.findChild(MComboBox, trForUI("Title"+str(tag[3]))).currentText())
            album = str(self.findChild(MComboBox, trForUI("Album"+str(tag[3]))).currentText())
            songs.append([artist,title,album,tag[3]])
        for tag in self.songsOfArtist:
            artist = str(self.findChild(MComboBox, trForUI("Artist"+str(tag[3]))).currentText())
            title = str(self.findChild(MComboBox, trForUI("Title"+str(tag[3]))).currentText())
            album = str(self.findChild(MComboBox, trForUI("Album"+str(tag[3]))).currentText())
            songs.append([artist,title,album,tag[3]])
        for tag in self.nullSongs:
            dosya = str(self.findChild(MComboBox, trForUI("File Name"+str(tag[4]))).currentText())
            artist = str(self.findChild(MComboBox, trForUI("Artist"+str(tag[4]))).currentText())
            title = str(self.findChild(MComboBox, trForUI("Title"+str(tag[4]))).currentText())
            album = str(self.findChild(MComboBox, trForUI("Album"+str(tag[4]))).currentText())
            songs.append([dosya,artist,title,album,tag[4]])
        for tag in self.incorrectSongs:
            dosya = str(self.findChild(MComboBox, trForUI("File Name"+str(tag[4]))).currentText())
            artist = str(self.findChild(MComboBox, trForUI("Artist"+str(tag[4]))).currentText())
            title = str(self.findChild(MComboBox, trForUI("Title"+str(tag[4]))).currentText())
            album = str(self.findChild(MComboBox, trForUI("Album"+str(tag[4]))).currentText())
            songs.append([dosya,artist,title,album,tag[4]])
        for song in songs:
            if len(song)==4:
                if str(self.parent().item(song[3],2).text())!=song[0]:
                    self.parent().setItem(song[3],2,MTableWidgetItem(trForUI(song[0])))
                if str(self.parent().item(song[3],3).text())!=song[1]:
                    self.parent().setItem(song[3],3,MTableWidgetItem(trForUI(song[1])))
                if str(self.parent().item(song[3],4).text())!=song[2]:
                    self.parent().setItem(song[3],4,MTableWidgetItem(trForUI(song[2])))
            else:
                if str(self.parent().item(song[4],1).text())!=song[0]:
                    self.parent().setItem(song[4],2,MTableWidgetItem(trForUI(song[0])))
                if str(self.parent().item(song[4],2).text())!=song[1]:
                    self.parent().setItem(song[4],2,MTableWidgetItem(trForUI(song[1])))
                if str(self.parent().item(song[4],3).text())!=song[2]:
                    self.parent().setItem(song[4],3,MTableWidgetItem(trForUI(song[2])))
                if str(self.parent().item(song[4],4).text())!=song[3]:
                    self.parent().setItem(song[4],4,MTableWidgetItem(trForUI(song[3])))
        self.close()

    def artistChanged(self, _index):
        if self.isAlterArtist:
            if _index == self.sender().currentIndex():
                self.isArtistImportant = False
            else:
                self.isArtistImportant = True
            self.isArtistChanged = True
            rowNo=int(str(self.sender().objectName()).replace("Artist",""))
            self.isAlterAlbum=True
            cbTag = self.sender()
            for object in self.cbTags:
                if str(object.objectName())=="Title"+str(rowNo):
                    object.clear()
                    for song in self.songsOfArtist:
                        if song[3]==rowNo:
                            for x,tag in enumerate(song[1]):
                                if _index!=self.sender().count()-1:
                                    if song[0][x]==str(cbTag.currentText()):
                                        for t in tag:
                                            for s in t:
                                                if object.findText(trForUI(s))==-1:
                                                    object.addItem(trForUI(s))
                                else:
                                    for t in tag:
                                        for s in t:
                                            if object.findText(trForUI(s))==-1:
                                                object.addItem(trForUI(s))
                            break
                    for song in self.songsOfAlbum:
                        if song[3]==rowNo:
                            for x,tag in enumerate(song[1]):
                                if _index!=self.sender().count()-1:
                                    if song[0][x]==str(cbTag.currentText()):
                                        for t in tag:
                                            for s in t:
                                                if object.findText(trForUI(s))==-1:
                                                    object.addItem(trForUI(s))
                                else:
                                    for t in tag:
                                        for s in t:
                                            if object.findText(trForUI(s))==-1:
                                                object.addItem(trForUI(s))
                            break
                if str(object.objectName())=="Album"+str(rowNo):
                    object.clear()
                    for song in self.songsOfArtist:
                        if song[3]==rowNo:
                            for x,tag in enumerate(song[2]):
                                if _index!=cbTag.count()-1:
                                    if song[0][x]==str(cbTag.currentText()):
                                        for t in tag:
                                            if object.findText(trForUI(t))==-1:
                                                object.addItem(trForUI(t))
                                else:
                                    for t in tag:
                                        if object.findText(trForUI(t))==-1:
                                            object.addItem(trForUI(t))
                            object.addItem(translate("SearchEngines", "All Albums"))
                            break
                    for song in self.songsOfAlbum:
                        if song[3]==rowNo:
                            for x,tag in enumerate(song[2]):
                                if _index!=cbTag.count()-1:
                                    if song[0][x]==str(cbTag.currentText()):
                                        for t in tag:
                                            if object.findText(trForUI(t))==-1:
                                                object.addItem(trForUI(t))
                                else:
                                    for t in tag:
                                        if object.findText(trForUI(t))==-1:
                                            object.addItem(trForUI(t))
                            object.addItem(translate("SearchEngines", "All Albums"))
                            break
            self.isAlterAlbum=False

    def albumChanged(self, _index):
        if _index == self.sender().count()-1:
            self.isArtistChangedTemp = self.isArtistChanged
            self.isArtistImportantTemp = self.isArtistImportant
            self.isArtistChanged = True
            self.isArtistImportant = True
        if self.isAlterAlbum==False:
            cbTag = self.sender()
            rowNo=int(str(cbTag.objectName()).replace("Album",""))
            for object in self.cbTags:
                if str(object.objectName())=="Artist"+str(rowNo):
                    artistObject=object
                    break
            for object in self.cbTags:
                if str(object.objectName())=="Title"+str(rowNo):
                    object.clear()
                    for song in self.songsOfArtist:
                        if song[3]==rowNo:
                            if self.isArtistImportant==True and self.isArtistChanged==True:
                                if artistObject.currentIndex() != artistObject.count()-1:
                                    if _index!=cbTag.count()-1:
                                        for t in song[1][artistObject.currentIndex()][cbTag.currentIndex()]:
                                            if object.findText(trForUI(t))==-1:
                                                object.addItem(trForUI(t))
                                    else:
                                        for y, tag in enumerate(song[2][artistObject.currentIndex()]):
                                            for t in song[1][artistObject.currentIndex()][y]:
                                                if object.findText(trForUI(t))==-1:
                                                    object.addItem(trForUI(t))
                                else:
                                    if _index!=cbTag.count()-1:
                                        for x, tag in enumerate(song[0]):
                                            for y, tag1 in enumerate(song[2][x]): 
                                                if song[2][x][y]==cbTag.currentText():
                                                    for t in song[1][x][y]:
                                                        if object.findText(trForUI(t))==-1:
                                                            object.addItem(trForUI(t))
                                    else:
                                        for x, tag in enumerate(song[0]):
                                            for y, tag1 in enumerate(song[2][x]):
                                                for t in song[1][x][y]:
                                                    if object.findText(trForUI(t))==-1:
                                                        object.addItem(trForUI(t))
                            else:
                                for x, tag in enumerate(song[1]):
                                    for y, tagm in enumerate(tag):
                                        if song[2][x][y] == cbTag.currentText():
                                            self.isAlterArtist = False
                                            artistObject.setCurrentIndex(x)
                                            self.isAlterArtist = True
                                            for t in song[1][x][y]:
                                                if object.findText(trForUI(t))==-1:
                                                    object.addItem(trForUI(t))
                    for song in self.songsOfAlbum:
                        if song[3]==rowNo:
                            if self.isArtistImportant==True and self.isArtistChanged==True:
                                if artistObject.currentIndex() != artistObject.count()-1:
                                    if _index!=cbTag.count()-1:
                                        for t in song[1][artistObject.currentIndex()][cbTag.currentIndex()]:
                                            if object.findText(trForUI(t))==-1:
                                                object.addItem(trForUI(t))
                                    else:
                                        for y, tag in enumerate(song[2][artistObject.currentIndex()]):
                                            for t in song[1][artistObject.currentIndex()][y]:
                                                if object.findText(trForUI(t))==-1:
                                                    object.addItem(trForUI(t))
                                else:
                                    if _index!=cbTag.count()-1:
                                        for x, tag in enumerate(song[0]):
                                            for y, tag1 in enumerate(song[2][x]): 
                                                if song[2][x][y]==cbTag.currentText():
                                                    for t in song[1][x][y]:
                                                        if object.findText(trForUI(t))==-1:
                                                            object.addItem(trForUI(t))
                                    else:
                                        for x, tag in enumerate(song[0]):
                                            for y, tag1 in enumerate(song[2][x]):
                                                for t in song[1][x][y]:
                                                    if object.findText(trForUI(t))==-1:
                                                        object.addItem(trForUI(t))
                            else:
                                for x, tag in enumerate(song[1]):
                                    for y, tagm in enumerate(tag):
                                        if song[2][x][y] == cbTag.currentText():
                                            self.isAlterArtist = False
                                            artistObject.setCurrentIndex(x)
                                            self.isAlterArtist = True
                                            for t in song[1][x][y]:
                                                if object.findText(trForUI(t))==-1:
                                                    object.addItem(trForUI(t))
                    break
        if _index == self.sender().count()-1:
            self.isArtistChanged = self.isArtistChangedTemp
            self.isArtistImportant = self.isArtistImportantTemp
            
            
            
