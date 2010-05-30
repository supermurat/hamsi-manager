# -*- coding: utf-8 -*-

import InputOutputs
from MyObjects import *
from time import gmtime
from os import *
import Dialogs
import eyeD3
import Organizer
import Records
import Universals

class Musics:
    """All information about the music files will be arranged in this class
        currentFilesAndFoldersValues[file no][value no]
    """
    global readMusics,writeMusics,correctForMusicTagType,writeMusicFile,currentFilesAndFoldersValues, types,types_nos,getSelectedMusicTagType, correctValuesForMusicTagType, musicTagType, getValuesForMusicTagType, changedValueNumber
    types = [u"Other (Default)",u"Icon",u"Other Icon",u"Front Cover",u"Back Cover",u"Leaflet",u"Media",
            u"Lead Artist",u"Artist",u"Leader",u"Band",u"Composer",u"Lyrics By",u"Recorded At",
            u"Recording",u"Performing",u"Video",u"Made Famous",u"Example",u"Band Logo",u"Publisher Logo"]
    types_nos = ["0","1","2","3","4","5","6","7","8","9","A","B","C","D","E","F","10","11","12","13","14"] 
    currentFilesAndFoldersValues = []
    changedValueNumber = 0
    
    def readMusics(_directoryPath=None,_filePath=None):
        global currentFilesAndFoldersValues,types,types_nos, musicTagType, changedValueNumber
        changedValueNumber = 0
        musicTagType = getSelectedMusicTagType()
        if _filePath!=None:
            _directoryPath = InputOutputs.getDirName(_filePath)
            musicFileNames = [InputOutputs.getBaseName(_filePath)]
        else:
            currentFilesAndFoldersValues = []
            InputOutputs.readDirectory(_directoryPath)
            musicFileNames = InputOutputs.musicFileNames
        isCanNoncompatible = False
        for musicNo,musicName in enumerate(musicFileNames):
            MApplication.processEvents()
            if eyeD3.isMp3File(_directoryPath+"/"+musicName) == False:
                isCanNoncompatible=True
            musicTagsValues=[]
            if _filePath!=None:
                musicTagsValues.append(_directoryPath)
            else:
                musicTagsValues.append(InputOutputs.getBaseName(_directoryPath))
            musicTagsValues.append(musicName)
            try:
                tag = eyeD3.Tag()
                try:
                    tag.link((_directoryPath+"/"+musicName).encode(InputOutputs.systemsCharSet), musicTagType)
                except:
                    tag = eyeD3.Tag()
                    tag.link(_directoryPath+"/"+musicName, musicTagType)
                try:    musicTagsValues.append(getValuesForMusicTagType(str(tag.getArtist())))
                except: musicTagsValues.append("None")
                try:    musicTagsValues.append(getValuesForMusicTagType(str(tag.getTitle())))
                except: musicTagsValues.append("None")
                try:    musicTagsValues.append(getValuesForMusicTagType(str(tag.getAlbum())))
                except: musicTagsValues.append("None")
                try:
                    if musicTagType==eyeD3.ID3_V2:
                        musicTagsValues.append(str(str(tag.getTrackNum()[0])+"/"+str(tag.getTrackNum()[1])))
                    else:
                        musicTagsValues.append(str(tag.getTrackNum()[0]))
                except: musicTagsValues.append("None")
                try:    musicTagsValues.append(str(tag.getYear()))
                except: musicTagsValues.append("None")
                try:    musicTagsValues.append(getValuesForMusicTagType(str(tag.getGenre())))
                except: musicTagsValues.append("None")
                try:    musicTagsValues.append(getValuesForMusicTagType(str(tag.getComment())))
                except: musicTagsValues.append("None")
                try:
                    if len(tag.getLyrics())!=0:
                        musicTagsValues.append(getValuesForMusicTagType(str(tag.getLyrics()[0].lyrics)))
                    else:
                        musicTagsValues.append("None")
                except:
                    musicTagsValues.append("None")
                if _filePath!=None:
                    try:
                        try:
                            musicFileDetail = eyeD3.Mp3AudioFile((_directoryPath+"/"+musicName).encode(InputOutputs.systemsCharSet))
                        except:
                            musicFileDetail = eyeD3.Mp3AudioFile(_directoryPath+"/"+musicName)
                        musicTagsValues.append(str(musicFileDetail.getSize()))
                        musicTagsValues.append(str(musicFileDetail.getPlayTimeString()))
                        musicTagsValues.append(str(musicFileDetail.getSampleFreq()))
                        musicTagsValues.append(str(musicFileDetail.getBitRateString()))
                    except:
                        musicTagsValues.append("")
                        musicTagsValues.append("")
                        musicTagsValues.append("")
                        musicTagsValues.append("")
                    musicTagsValues.append([])
                    try:
                        for image_no,image in enumerate(tag.getImages()):
                            musicTagsValues[-1].append([])
                            for no,type in enumerate(types):
                                if str(image.pictureType)==types_nos[no]:
                                    musicTagsValues[-1][image_no].append(no)
                                    musicTagsValues[-1][image_no].append(type)
                                    break
                            musicTagsValues[-1][image_no].append(image.mimeType)
                            musicTagsValues[-1][image_no].append(image.imageData)
                    except:
                        pass
                    return musicTagsValues
            except:
                musicTagsValues.append("")
                musicTagsValues.append("")
                musicTagsValues.append("")
                musicTagsValues.append("")
                musicTagsValues.append("")
                musicTagsValues.append("")
                musicTagsValues.append("")
                musicTagsValues.append("")
                if _filePath!=None:
                    musicTagsValues.append("")
                    musicTagsValues.append("")
                    musicTagsValues.append("")
                    musicTagsValues.append("")
                    musicTagsValues.append([])
                    return musicTagsValues
            currentFilesAndFoldersValues.append(musicTagsValues)
            Dialogs.showState(translate("InputOutputs/Musics", "Reading Music Tags"),musicNo+1,len(musicFileNames))
        if isCanNoncompatible == True:
            Dialogs.show(translate("InputOutputs/Musics", "Possible ID3 Mismatch"),
                translate("InputOutputs/Musics", "Some of the files presented in the table may not support ID3 technology.<br>Please check the files and make sure they support ID3 information before proceeding."))
    
    def writeMusics(_table):
        global musicTagType, changedValueNumber
        changedValueNumber = 0
        musicTagType = getSelectedMusicTagType()
        changingFileDirectories=[]
        if _table.isShowOldValues.isChecked()==True:
            startRowNo,rowStep=1,2
        else:
            startRowNo,rowStep=0,1
        Dialogs.showState(translate("InputOutputs/Musics", "Writing Music Tags"),0,len(currentFilesAndFoldersValues))
        for rowNo in range(startRowNo,_table.rowCount(),rowStep):
            MApplication.processEvents()
            if _table.isShowOldValues.isChecked()==True:
                realRowNo=rowNo/2
            else:
                realRowNo=rowNo
            if InputOutputs.isWritableFileOrDir(InputOutputs.currentDirectoryPath+"/"+str(currentFilesAndFoldersValues[realRowNo][1])):
                if _table.isRowHidden(rowNo):
                    InputOutputs.removeFileOrDir(InputOutputs.currentDirectoryPath+"/"+str(currentFilesAndFoldersValues[realRowNo][1]))
                    continue
                tag = eyeD3.Tag()
                try:
                    tag.link((InputOutputs.currentDirectoryPath+"/"+currentFilesAndFoldersValues[realRowNo][1]).encode(InputOutputs.systemsCharSet), musicTagType)
                except:
                    tag = eyeD3.Tag()
                    tag.link(InputOutputs.currentDirectoryPath+"/"+currentFilesAndFoldersValues[realRowNo][1], musicTagType)
                correctForMusicTagType(tag)
                if _table.isColumnHidden(2)!=True and (_table.item(rowNo,2).isSelected()==_table.isChangeSelected.isChecked() or _table.isChangeAll.isChecked())==True:
                    value = unicode(_table.item(rowNo,2).text(), "utf-8")
                    if value!=str(currentFilesAndFoldersValues[realRowNo][2]) and (str(currentFilesAndFoldersValues[realRowNo][2])!="None" or value!=""):
                        tag.setArtist(correctValuesForMusicTagType(value))
                        Records.add(str(translate("MusicTable", "Artist")), str(currentFilesAndFoldersValues[realRowNo][2]), value)
                        changedValueNumber += 1
                if _table.isColumnHidden(3)!=True and (_table.item(rowNo,3).isSelected()==_table.isChangeSelected.isChecked() or _table.isChangeAll.isChecked())==True:
                    value = unicode(_table.item(rowNo,3).text(), "utf-8")
                    if value!=str(currentFilesAndFoldersValues[realRowNo][3]) and (str(currentFilesAndFoldersValues[realRowNo][3])!="None" or value!=""):
                        tag.setTitle(correctValuesForMusicTagType(value))
                        Records.add(str(translate("MusicTable", "Title")), str(currentFilesAndFoldersValues[realRowNo][3]), value)
                        changedValueNumber += 1
                if _table.isColumnHidden(4)!=True and (_table.item(rowNo,4).isSelected()==_table.isChangeSelected.isChecked() or _table.isChangeAll.isChecked())==True:
                    value = unicode(_table.item(rowNo,4).text(), "utf-8")
                    if value!=str(currentFilesAndFoldersValues[realRowNo][4]) and (str(currentFilesAndFoldersValues[realRowNo][4])!="None" or value!=""):
                        tag.setAlbum(correctValuesForMusicTagType(value))
                        Records.add(str(translate("MusicTable", "Album")), str(currentFilesAndFoldersValues[realRowNo][4]), value)
                        changedValueNumber += 1
                if _table.isColumnHidden(5)!=True and (_table.item(rowNo,5).isSelected()==_table.isChangeSelected.isChecked() or _table.isChangeAll.isChecked())==True:
                    value = unicode(_table.item(rowNo,5).text(), "utf-8")
                    if value!=str(currentFilesAndFoldersValues[realRowNo][5]) and (str(currentFilesAndFoldersValues[realRowNo][5])!="None" or value!=""):
                        track = []
                        if musicTagType==eyeD3.ID3_V2:
                            if value.find("/")!=-1:
                                track_temp = value.split("/")
                                try:    track.append(int(track_temp[0]))
                                except: track.append(None)
                                try:    track.append(int(track_temp[1]))
                                except: track.append(len(currentFilesAndFoldersValues))
                            elif value=="":
                                track.append(None)
                                track.append(None)
                            else:
                                try:    track.append(int(value))
                                except: track.append(None)    
                                track.append(len(currentFilesAndFoldersValues))
                        else:
                            try:    track = int(value)
                            except: track = None 
                        tag.setTrackNum(track)
                        Records.add(str(translate("MusicTable", "Track No")), str(currentFilesAndFoldersValues[realRowNo][5]), track)
                        changedValueNumber += 1
                if _table.isColumnHidden(6)!=True and (_table.item(rowNo,6).isSelected()==_table.isChangeSelected.isChecked() or _table.isChangeAll.isChecked())==True:
                    value = unicode(_table.item(rowNo,6).text(), "utf-8")
                    if value!=str(currentFilesAndFoldersValues[realRowNo][6]) and (str(currentFilesAndFoldersValues[realRowNo][6])!="None" or value!=""):
                        if len(value)==4:
                            tag.setDate(value)
                            Records.add(str(translate("MusicTable", "Year")), str(currentFilesAndFoldersValues[realRowNo][6]), value)
                            changedValueNumber += 1
                        elif value=="":
                            tag.setDate(None)
                            Records.add(str(translate("MusicTable", "Year")), str(currentFilesAndFoldersValues[realRowNo][6]), None)
                            changedValueNumber += 1
                        else:
                            tag.setDate(gmtime()[0])
                            Records.add(str(translate("MusicTable", "Year")), str(currentFilesAndFoldersValues[realRowNo][6]), gmtime()[0])
                            changedValueNumber += 1
                if _table.isColumnHidden(7)!=True and (_table.item(rowNo,7).isSelected()==_table.isChangeSelected.isChecked() or _table.isChangeAll.isChecked())==True:
                    value = unicode(_table.item(rowNo,7).text(), "utf-8")
                    if value!=str(currentFilesAndFoldersValues[realRowNo][7]) and (str(currentFilesAndFoldersValues[realRowNo][7])!="None" or value!=""):
                        tag.setGenre(correctValuesForMusicTagType(value))
                        Records.add(str(translate("MusicTable", "Genre")), str(currentFilesAndFoldersValues[realRowNo][7]), value)
                        changedValueNumber += 1
                if _table.isColumnHidden(8)!=True and (_table.item(rowNo,8).isSelected()==_table.isChangeSelected.isChecked() or _table.isChangeAll.isChecked())==True:
                    value = unicode(_table.item(rowNo,8).text(), "utf-8")
                    if value!=str(currentFilesAndFoldersValues[realRowNo][8]) and (str(currentFilesAndFoldersValues[realRowNo][8])!="None" or value!=""):
                        tag.removeComments()
                        tag.addComment(correctValuesForMusicTagType(value))
                        Records.add(str(translate("MusicTable", "Comment")), str(currentFilesAndFoldersValues[realRowNo][8]), value)
                        changedValueNumber += 1
                if musicTagType==eyeD3.ID3_V2 and _table.isColumnHidden(9)!=True and (_table.item(rowNo,9).isSelected()==_table.isChangeSelected.isChecked() or _table.isChangeAll.isChecked())==True:
                    value = unicode(_table.item(rowNo,9).text(), "utf-8")
                    if value!=str(currentFilesAndFoldersValues[realRowNo][9]) and (str(currentFilesAndFoldersValues[realRowNo][9])!="None" or value!=""):
                        tag.removeLyrics()
                        tag.addLyrics(correctValuesForMusicTagType(value))
                        Records.add(str(translate("MusicTable", "Lyrics")), str(currentFilesAndFoldersValues[realRowNo][9]), value)
                        changedValueNumber += 1
                tag.update()
                newFileName=str(currentFilesAndFoldersValues[realRowNo][1])
                if _table.isColumnHidden(1)!=True and (_table.item(rowNo,1).isSelected()==_table.isChangeSelected.isChecked() or _table.isChangeAll.isChecked())==True:
                    if str(currentFilesAndFoldersValues[realRowNo][1])!=unicode(_table.item(rowNo,1).text()).encode("utf-8"):
                        if unicode(_table.item(rowNo,1).text()).encode("utf-8").strip()!="":
                            orgExt = str(currentFilesAndFoldersValues[realRowNo][1]).split(".")[-1].decode("utf-8").lower()
                            if unicode(_table.item(rowNo,1).text()).encode("utf-8").split(".")[-1].decode("utf-8").lower() != orgExt:
                                _table.setItem(rowNo,1,MTableWidgetItem(str(unicode(_table.item(rowNo,1).text()).encode("utf-8") + "." + orgExt).decode("utf-8")))
                            if unicode(_table.item(rowNo,1).text()).encode("utf-8").split(".")[-1] != orgExt:
                                extState = unicode(_table.item(rowNo,1).text()).encode("utf-8").decode("utf-8").lower().find(orgExt)
                                if extState!=-1:
                                    _table.setItem(rowNo,1,MTableWidgetItem(str(unicode(_table.item(rowNo,1).text()).encode("utf-8")[:extState] + "." + orgExt).decode("utf-8")))
                            newFileName = InputOutputs.moveOrChange(InputOutputs.currentDirectoryPath+"/"+str(currentFilesAndFoldersValues[realRowNo][1]), InputOutputs.currentDirectoryPath+"/"+unicode(_table.item(rowNo,1).text()).encode("utf-8"))
                            changedValueNumber += 1
                if newFileName==False:
                    continue
                if _table.isColumnHidden(0)!=True and (_table.item(rowNo,0).isSelected()==_table.isChangeSelected.isChecked() or _table.isChangeAll.isChecked())==True:
                    newDirectoryName=unicode(_table.item(rowNo,0).text()).encode("utf-8")
                    try:
                        newDirectoryName=int(newDirectoryName)
                        newDirectoryName=str(newDirectoryName)
                    except:
                        if newDirectoryName.decode("utf-8").lower()==newDirectoryName.upper():
                            newDirectoryName=str(currentFilesAndFoldersValues[realRowNo][0])
                    if str(currentFilesAndFoldersValues[realRowNo][0])!=newDirectoryName:
                        newPath=InputOutputs.getDirName(InputOutputs.currentDirectoryPath)
                        changingFileDirectories.append([])
                        changingFileDirectories[-1].append(newPath+"/"+str(currentFilesAndFoldersValues[realRowNo][0])+"/"+newFileName)
                        changingFileDirectories[-1].append(newPath+"/"+newDirectoryName+"/"+newFileName)
                        changedValueNumber += 1
            if _table.isShowOldValues.isChecked()==True:
                actionNumber=rowNo/2
            else:
                actionNumber=rowNo
            Dialogs.showState(translate("InputOutputs/Musics", "Writing Music Tags"),actionNumber+1,len(currentFilesAndFoldersValues))
        return InputOutputs.changeDirectories(changingFileDirectories)
        
    def writeMusicFile(_oldMusicTagsValues,_newMusicTagsValues,_isImageAction=False,_ImageType=False,_ImagePath=False):
        global musicTagType
        if InputOutputs.isWritableFileOrDir(_oldMusicTagsValues[0]+"/"+_oldMusicTagsValues[1]):
            musicTagType = getSelectedMusicTagType()
            tag = eyeD3.Tag()
            try:
                tag.link((_oldMusicTagsValues[0]+"/"+_oldMusicTagsValues[1]).encode(InputOutputs.systemsCharSet), musicTagType)
            except:
                tag = eyeD3.Tag()
                tag.link(_oldMusicTagsValues[0]+"/"+_oldMusicTagsValues[1], musicTagType)
            correctForMusicTagType(tag)
            if _isImageAction==False:
                if _newMusicTagsValues[2]!=_oldMusicTagsValues[2]:
                    tag.setArtist(correctValuesForMusicTagType(unicode(_newMusicTagsValues[2])))
                if _newMusicTagsValues[3]!=_oldMusicTagsValues[3]:
                    tag.setTitle(correctValuesForMusicTagType(unicode(_newMusicTagsValues[3])))
                if _newMusicTagsValues[4]!=_oldMusicTagsValues[4]:
                    tag.setAlbum(correctValuesForMusicTagType(unicode(_newMusicTagsValues[4])))
                if _newMusicTagsValues[5]!=_oldMusicTagsValues[5]:
                    track = []
                    track_temp=_newMusicTagsValues[5]
                    if track_temp.find("/")!=-1:
                        track_temp2 = track_temp.split("/")
                        try:    track.append(int(track_temp2[0]))
                        except: track.append(None)
                        try:    track.append(int(track_temp2[1]))
                        except: track.append(len(currentFilesAndFoldersValues))
                    elif track_temp=="":
                        track.append(None)
                        track.append(None)
                    else:
                        try:    track.append(int(track_temp))
                        except: track.append(None)    
                        track.append(len(currentFilesAndFoldersValues))
                    tag.setTrackNum(track)
                if _newMusicTagsValues[6]!=_oldMusicTagsValues[6]:
                    if len(_newMusicTagsValues[6])==4:
                        tag.setDate(unicode(_newMusicTagsValues[6]))
                    elif _newMusicTagsValues[6]=="":
                        tag.setDate(None)
                    else:
                        tag.setDate(gmtime()[0])
                if _newMusicTagsValues[7]!=_oldMusicTagsValues[7]:
                    tag.setGenre(correctValuesForMusicTagType(str(unicode(_newMusicTagsValues[7]))))
                if _newMusicTagsValues[8]!=_oldMusicTagsValues[8]:
                    tag.removeComments()
                    tag.addComment(correctValuesForMusicTagType(unicode(_newMusicTagsValues[8])))
                if musicTagType==eyeD3.ID3_V2 and _newMusicTagsValues[9]!=_oldMusicTagsValues[9]:
                    tag.removeLyrics()
                    tag.addLyrics(correctValuesForMusicTagType(unicode(_newMusicTagsValues[9])))
                        
                tag.update()
                newFileName=_oldMusicTagsValues[1]
                if _oldMusicTagsValues[1]!=_newMusicTagsValues[1]:
                    if _newMusicTagsValues[1].strip()!="":
                        orgExt = _oldMusicTagsValues[1].split(".")[-1].decode("utf-8").lower()
                        if _newMusicTagsValues[1].split(".")[-1].decode("utf-8").lower() != orgExt:
                            _newMusicTagsValues[1] = _newMusicTagsValues[1].split(".")[-1] + "." + orgExt
                        if _newMusicTagsValues[1].split(".")[-1] != orgExt:
                            extState = _newMusicTagsValues[1].lower().find(orgExt)
                            if extState!=-1:
                                _newMusicTagsValues[1] = _newMusicTagsValues[1].split(".")[-1][:extState] + "." + orgExt
                        newFileName = InputOutputs.moveOrChange(_oldMusicTagsValues[0]+"/"+_oldMusicTagsValues[1],_oldMusicTagsValues[0]+"/"+_newMusicTagsValues[1])
                            
                newDirectoryName=_newMusicTagsValues[0].replace(InputOutputs.getDirName(_oldMusicTagsValues[0])+"/","")
                try:
                    newDirectoryName=str(newDirectoryName)
                    newDirectoryName=int(newDirectoryName)
                except:
                    if newDirectoryName.decode("utf-8").lower()==newDirectoryName.upper():
                        newDirectoryName=_oldMusicTagsValues[0]
                if InputOutputs.getBaseName(_oldMusicTagsValues[0])!=newDirectoryName:
                    if InputOutputs.moveOrChange(_oldMusicTagsValues[0]+"/"+newFileName,InputOutputs.getDirName(_oldMusicTagsValues[0])+"/"+newDirectoryName+"/"+newFileName)==True:
                        return InputOutputs.getDirName(_oldMusicTagsValues[0])+"/"+newDirectoryName+"/"+newFileName
            
            #Making changes on image files
            else:
                if musicTagType==eyeD3.ID3_V2:
                    tag.addImage(_ImageType,_ImagePath)
                    tag.update()
                return None
        return _oldMusicTagsValues[0]+"/"+_oldMusicTagsValues[1]

    def correctForMusicTagType(_tag):
        _tag.setVersion(musicTagType)
        if musicTagType==eyeD3.ID3_V2:
            _tag.setTextEncoding(eyeD3.frames.UTF_8_ENCODING)
            
    def correctValuesForMusicTagType(_value):
        if musicTagType==eyeD3.ID3_V1:
            return unicode(str(_value), "latin1")
        else:
            return unicode(str(_value))
        
    def getValuesForMusicTagType(_value):
        if musicTagType==eyeD3.ID3_V1:
            return unicode(_value).encode("latin1")
        else:
            return _value
        
    def getSelectedMusicTagType():
        t = Universals.MySettings["musicTagType"]
        if t=="ID3 V2":v=eyeD3.ID3_V2
        elif t=="ID3 V1":v=eyeD3.ID3_V1
        else:v = eyeD3.ID3_CURRENT_VERSION
        return v
        
        
        
        
