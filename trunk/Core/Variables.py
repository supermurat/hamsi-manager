# -*- coding: utf-8 -*-

import os, sys

class Variables():
    global checkStartupVariables, checkEncoding, getAvailablePlayers, getCharSets, getStyles, getScreenSize, getMyObjectsNames
    global defaultFileSystemEncoding
    defaultFileSystemEncoding = sys.getfilesystemencoding().lower()

    def checkStartupVariables():
        checkEncoding()

    def checkEncoding(_isSetUTF8=False):
        global defaultFileSystemEncoding
        from encodings import aliases
        if [str(v).lower().replace("_", "-") for k, v in aliases.aliases.iteritems()].count(defaultFileSystemEncoding)==0:
            if _isSetUTF8:
                defaultFileSystemEncoding = "utf-8"
            else:
                defaultFileSystemEncoding = sys.getdefaultencoding().lower()
                checkEncoding(True)

    def getAvailablePlayers():
        playerNames = ["Mplayer"]
        try:
            import tkSnack
            playerNames.append("tkSnack")
        except:pass
        try:
            from PySide.phonon import Phonon
            playerNames.append("Phonon (PySide)")
        except:pass
        try:
            from PyQt4.phonon import Phonon
            playerNames.append("Phonon")
        except:pass
        return playerNames
       
    def getCharSets():
        from encodings import aliases
        charSets = []
        for k, v in aliases.aliases.iteritems():
            if charSets.count(v.replace("_", "-"))==0:
                charSets.append(v.replace("_", "-"))
        charSets.sort()
        return charSets
        
    def getStyles():
        from PyQt4.QtGui import QStyleFactory
        styles = []
        for stil in QStyleFactory.keys(): 
            styles.append(str(stil))
        return styles
        
    def getScreenSize():
        from PyQt4.QtGui import QDesktopWidget
        if Universals.MainWindow!=None:
            return QDesktopWidget().screenGeometry()
        else:
            return None
        
    def getMyObjectsNames():
        myObjectsName = []
        try:
            import PyQt4
            myObjectsName.append("PyQt4")
        except:pass
        try:
            import PySide
            myObjectsName.append("PySide")
        except:pass
        return myObjectsName
        
    def isAvailablePyKDE4():
        try:
            import PyKDE4
            return True
        except:
            return False
        
    def getUserDesktopPath():
        import Universals
        if isAvailablePyKDE4():
            from PyKDE4.kdeui import KGlobalSettings
            desktopPath = str(KGlobalSettings.desktopPath())
        else:
            from MyObjects import translate
            desktopNames = [str(translate("Install","Desktop")), "Desktop"]
            for dirName in desktopNames:
                if InputOutputs.isDir(Universals.userDirectoryPath + "/" + dirName):
                    desktopPath = Universals.userDirectoryPath + "/" + dirName
                    break
                else:
                    desktopPath = Universals.userDirectoryPath
        return desktopPath

