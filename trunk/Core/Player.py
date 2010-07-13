# -*- coding: utf-8 -*-

from InputOutputs import Musics
import InputOutputs
import os
from MyObjects import *
import Dialogs
import Organizer
import time
import Universals
import ReportBug

class Player(MWidget):
    def __init__(self, _parent, _type="bar", _file=""):
        MWidget.__init__(self, _parent)
        self.Player = None
        self.PlayerName = None
        self.file = _file
        self.type = _type
        self.infoScroller = InfoScroller(self)
        self.tbPause = MToolButton(self)
        self.tbPause.setToolTip(translate("Player", "Pause / Continue"))
        self.tbPause.setIcon(MIcon("Images:mediaPause.png"))
        self.tbPause.setAutoRaise(True)
        #self.tbPause.setCheckable(True)
        self.tbMute = MToolButton(self)
        self.tbMute.setToolTip(translate("Player", "Mute"))
        self.tbMute.setIcon(MIcon("Images:playerMute.png"))
        self.tbMute.setAutoRaise(True)
        self.tbMute.setCheckable(True)
        self.tbPlay = MToolButton(self)
        self.tbPlay.setToolTip(translate("Player", "Play"))
        self.tbPlay.setIcon(MIcon("Images:mediaPlay.png"))
        self.tbPlay.setAutoRaise(True)
        self.tbStop = MToolButton(self)
        self.tbStop.setToolTip(translate("Player", "Stop"))
        self.tbStop.setIcon(MIcon("Images:mediaStop.png"))
        self.tbStop.setAutoRaise(True)
        self.tbPause.setEnabled(False)
        self.tbMute.setEnabled(False)
        self.tbStop.setEnabled(False)
        MObject.connect(self.tbPause, SIGNAL("clicked()"), self.pause)
        MObject.connect(self.tbMute, SIGNAL("clicked()"), self.mute)
        MObject.connect(self.tbPlay, SIGNAL("clicked()"), self.play)
        MObject.connect(self.tbStop, SIGNAL("clicked()"), self.stop)
#        self.sldState = MSlider(Mt.Horizontal)
#        self.sldState.setMaximum(100)
#        self.sldState.setTickInterval(1)
#        MObject.connect(self.sldState, SIGNAL("valueChanged(int)"), self.seek)
#        runButtons =[]
#        for value in ["-60","-30","-10","10","30","60"]:
#            runButtons.append(MPushButton(str(value).decode("utf-8")))
#            runButtons[-1].setObjectName(str(value))
#            MObject.connect(runButtons[-1], SIGNAL("clicked()"), self.run)
#        for btn in runButtons:
#            HBOXs[0].addWidget(btn)
#        HBOXs.append(MHBoxLayout())
#        HBOXs[1].addWidget(self.sldState)
#        VBOX.addLayout(HBOXs[1])
        if _type == "bar" and Universals.windowMode==Universals.windowModeKeys[1]:
            pass
        else:
            self.info = MLabel(translate("Player", "Please Select The File You Want To Play And Click The Play Button."))
        if _type=="bar":
            #little style for bar
            self.playInBar = MToolButton(self)
            self.playInBar.setToolTip(translate("Player", "The Selected Files Are Played Here Instead Of The Details Window."))
            self.playInBar.setIcon(MIcon("Images:playInBar.png"))
            self.playInBar.setAutoRaise(True)
            self.playInBar.setCheckable(True)
            self.playInBar.setChecked(True)
            HBOXs=[]
            HBOXs.append(MHBoxLayout())
            HBOXs[0].addWidget(self.tbPause)
            HBOXs[0].addWidget(self.tbPlay)
            HBOXs[0].addWidget(self.tbStop)
            HBOXs[0].addWidget(self.tbMute)
            HBOXs[0].addWidget(self.playInBar)
            HBOXs.append(MHBoxLayout())
            if Universals.windowMode==Universals.windowModeKeys[1]:
                self.playInBar.setMaximumHeight(16)
                self.tbPause.setMaximumHeight(16)
                self.tbMute.setMaximumHeight(16)
                self.tbPlay.setMaximumHeight(16)
                self.tbStop.setMaximumHeight(16)
            else:
                HBOXs[1].addWidget(self.info)
                self.playInBar.setMinimumHeight(22)
                self.tbPause.setMinimumHeight(22)
                self.tbMute.setMinimumHeight(22)
                self.tbPlay.setMinimumHeight(22)
                self.tbStop.setMinimumHeight(22)
            VBOX = MVBoxLayout()
            VBOX.setSpacing(0)
            VBOX.addLayout(HBOXs[1])
            VBOX.addLayout(HBOXs[0])
            self.setLayout(VBOX)
            self.setMaximumSize(150, 40)
        elif _type=="dialog":
            #full style for dialog
            HBOXs=[]
            HBOXs.append(MHBoxLayout())
            HBOXs[0].addWidget(self.tbPause)
            HBOXs[0].addWidget(self.tbPlay)
            HBOXs[0].addWidget(self.tbStop)
            HBOXs[0].addWidget(self.tbMute)
            HBOXs.append(MHBoxLayout())
            HBOXs[1].addWidget(self.info)
            VBOX = MVBoxLayout()
            VBOX.setSpacing(0)
            VBOX.addLayout(HBOXs[1])
            VBOX.addLayout(HBOXs[0])
            self.setLayout(VBOX)
            self.info.setMinimumWidth(len(self.info.text())*7)
            self.tbPause.setMinimumHeight(22)
            self.tbMute.setMinimumHeight(22)
            self.tbPlay.setMinimumHeight(22)
            self.tbStop.setMinimumHeight(22)
            self.setMaximumSize(390, 44)
        if self.type != "bar" or Universals.windowMode!=Universals.windowModeKeys[1]:
            self.infoScroller.start()
            
    def setInfoText(self, _info):
        if self.type == "bar" and Universals.windowMode==Universals.windowModeKeys[1]:
            Universals.MainWindow.StatusBar.showMessage(_info)
        else:
            self.info.setText(_info)
            self.info.setMinimumWidth(len(self.info.text())*7)
            
    def play(self, _filePath="", _isPlayNow=True):
        try:
            MApplication.processEvents()
            playerName = Universals.MySettings["playerName"]
            if self.Player==None or self.PlayerName != playerName:
                self.stop()
                self.PlayerName = playerName
                if playerName=="Phonon":
                    self.Player = M_Phonon()
                elif playerName=="Phonon (PySide)":
                    self.Player = M_Phonon_PySide()
                elif playerName=="tkSnack":
                    self.Player = M_tkSnack()
                else:
                    self.Player = M_MPlayer()
            self.stop()
            if _filePath=="" and self.file=="":
                _filePath = InputOutputs.currentDirectoryPath + "/" + InputOutputs.musicFileNames[self.parent().parent().Table.currentRow()]
            elif self.file!="":
                _filePath = self.file
            if InputOutputs.isFile(_filePath):
                self.musicTags = Musics.readMusics(None,_filePath)
                self.setInfoText((("%s - %s (%s)") % (self.musicTags[2] , self.musicTags[3], self.musicTags[4])).decode("utf-8"))
                if _isPlayNow==True:
                    if self.Player.play(_filePath):
                #        self.checkState = CheckState(self, self.Player)
                #        self.checkState.start()
                        self.tbPause.setEnabled(True)
                        self.tbMute.setEnabled(True)
                        self.tbStop.setEnabled(True)
        except:
            error = ReportBug.ReportBug()
            error.show()
        
    def stop(self):
        try:
            try:self.Player.stop()
            except:pass
            self.tbPause.setEnabled(False)
            self.tbMute.setEnabled(False)
            self.tbPause.setChecked(False)
            self.tbMute.setChecked(False)
            self.tbStop.setEnabled(False)
            if self.type=="bar":
                self.setInfoText(translate("Player", "Please Select The File You Want To Play And Click The Play Button."))
        except:
            error = ReportBug.ReportBug()
            error.show()
        
    def mute(self):
        try:
            if self.tbPause.isChecked():
                self.tbPause.setChecked(False)
            self.Player.mute()
        except:
            error = ReportBug.ReportBug()
            error.show()
        
    def pause(self):
        try:
            self.Player.pause()
        except:
            error = ReportBug.ReportBug()
            error.show()
        
    def runTo(self):
        try:
            temp=nesne_adi().split(";")
            self.Player.runTo(temp[1])
        except:
            error = ReportBug.ReportBug()
            error.show()
        
    def seek(self, _state):      
        try:  
            self.Player.seek(_state)
        except:
            error = ReportBug.ReportBug()
            error.show()


class M_Phonon():
    def __init__(self):
        self.m_media = None
        self.paused = False
        self.muted = False
    
    def play(self, _filePath):
        if self.m_media!=None:
           self.stop() 
        try:
            from PyQt4.phonon import Phonon
        except:
            Dialogs.showError(translate("Player", "Phonon Is Not Installed On Your System."),
                        translate("Player", "We could not find the Phonon(PyQt4) module installed on your system.<br>Please choose another player from the options or <br>check your Phonon installation."))
            return False
        import Universals
        if not self.m_media:
            self.m_media = Phonon.MediaObject(Universals.MainWindow)
            self.audioOutput = Phonon.AudioOutput(Phonon.MusicCategory, Universals.MainWindow)
            Phonon.createPath(self.m_media, self.audioOutput)
        self.m_media.setCurrentSource(
            Phonon.MediaSource(_filePath.decode("utf-8")))
        self.m_media.play()
        self.paused = False
        return True
    
    def pause(self):
        if self.paused:
            self.m_media.play()
            self.paused=False
        else:
            self.m_media.pause()
            self.paused=True
    
    def stop(self):
        if self.m_media!=None:
            self.m_media.stop()
        self.paused = False
    
    def runTo(self, _saniye):
        self.m_media.seek(_saniye)
    
    def seek(self, _state):
        pass
    
    def mute(self):
        if self.muted:
            self.audioOutput.setMuted(False)
            self.muted=False
        else:
            self.audioOutput.setMuted(True)
            self.muted=True

class M_Phonon_PySide():
    def __init__(self):
        self.m_media = None
        self.paused = False
        self.muted = False
    
    def play(self, _filePath):
        if self.m_media!=None:
           self.stop() 
        try:
            from PySide.phonon import Phonon
        except:
            Dialogs.showError(translate("Player", "Phonon Is Not Installed On Your System."),
                        translate("Player", "We could not find the Phonon(PySide) module installed on your system.<br>Please choose another player from the options or <br>check your Phonon installation."))
        import Universals
        if not self.m_media:
            self.m_media = Phonon.MediaObject()
            self.audioOutput = Phonon.AudioOutput(Phonon.MusicCategory)
            Phonon.createPath(self.m_media, self.audioOutput)
        self.m_media.setCurrentSource(Phonon.MediaSource(_filePath.decode("utf-8")))
        self.m_media.play()
        self.paused = False
        return True
    
    def pause(self):
        if self.paused:
            self.m_media.play()
            self.paused=False
        else:
            self.m_media.pause()
            self.paused=True
    
    def stop(self):
        if self.m_media!=None:
            self.m_media.stop()
        self.paused = False
    
    def runTo(self, _saniye):
        self.m_media.seek(_saniye)
    
    def seek(self, _state):
        pass
    
    def mute(self):
        if self.muted:
            self.audioOutput.setMuted(False)
            self.muted=False
        else:
            self.audioOutput.setMuted(True)
            self.muted=True

class M_tkSnack():
    def __init__(self):
        self.tada = None

    def play(self, _filePath):
        if self.tada!=None:
           self.stop() 
        from Tkinter import Tk
        import tkSnack
        self.root = Tk()
        tkSnack.initializeSnack(self.root)
        self.tada = tkSnack.Sound(file=_filePath)
        self.tada.play()
        return True

    def pause(self):
        self.tada.pause()

    def stop(self):
        if self.tada!=None:
            self.tada.stop()

    def runTo(self, _saniye):
        pass

    def seek(self, _state):
        pass

    def mute(self):
        pass

class M_MPlayer():
    
    def __init__(self):
        self.popen = False
    
    def runCommand(self, _command):
        if self.popen!=False:
            from Execute import writeToPopen
            writeToPopen(self.popen, _command)
        
    def play(self, _filePath):
        from Execute import execute
        if self.popen!=False:
            self.runCommand("quit")
        command = str("\"" + Universals.MySettings["mplayerPath"]+"\" "+
                    Universals.MySettings["mplayerArgs"]+" "+
                    Universals.MySettings["mplayerAudioDevicePointer"]+" "+
                    Universals.MySettings["mplayerAudioDevice"])
        command += " '" + _filePath + "'"
        self.popen = execute(command)
        return True
        
    def pause(self):
        self.runCommand("pause")  
        
    def stop(self):
        self.runCommand("quit")
        try:self.popen.close()
        except:pass
        self.popen = False
        
    def runTo(self, _saniye):
        self.runCommand("seek " + str(_saniye))
    
    def seek(self, _state):
        self.runCommand("seek " + str(_state) + " 100")
    
    def mute(self):
        self.runCommand("mute")        
        
class CheckState(MThread):
    
    def __init__(self, _parent, _Player):
        MApplication.processEvents()
        MThread.__init__(self)
        self.Player = _Player
        self.parent = _parent
    
    def run(self):
        MApplication.processEvents()
        i=0
        while 1==1:
            MApplication.processEvents()
            self.parent.setInfoText(str(i))
            time.sleep(1)
            self.parent.setInfoText(str(self.Player.konumuNe()))
            #self.sldState.setValue(int(1))
            time.sleep(1)
            i+=1
        
        
try:
    class InfoScroller(MThread):
        def __init__(self, _parent):
            MApplication.processEvents()
            MThread.__init__(self)
            self.parent = _parent
        
        def run(self):
            try:
                MApplication.processEvents()
                x = 150
                while 1==1:
                    MApplication.processEvents()
                    self.parent.info.move(x, 0)
                    time.sleep(0.05)
                    x-=1
                    if x<=-(len(self.parent.info.text())*7):
                        x=150
            except:pass
except:pass
