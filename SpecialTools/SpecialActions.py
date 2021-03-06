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


from Core import Organizer
from Core import Universals as uni
import FileUtils as fu
from Core.MyObjects import *
from Core import Dialogs
from Core import ReportBug
from Databases import BookmarksOfSpecialTools


class SpecialActions(MWidget):
    def __init__(self, _parent):
        MWidget.__init__(self, _parent)
        self.specialTools = _parent
        self.pbtnAddObjects = []
        self.lblSplit = MLabel(">>>", self)
        self.cbBookmarks = MComboBox()
        self.tbClear = MToolButton(self)
        self.tbAddBookmark = MToolButton(self)
        self.tbDeleteBookmark = MToolButton(self)
        self.tbWhatDoesThisCommandDo = MToolButton(self)
        self.tbClear.setToolTip(translate("SpecialTools", "Clear"))
        self.tbAddBookmark.setToolTip(translate("SpecialTools", "Add To Bookmarks"))
        self.tbDeleteBookmark.setToolTip(translate("SpecialTools", "Remove From Bookmarks"))
        self.tbWhatDoesThisCommandDo.setToolTip(translate("SpecialTools", "What Does This Command Do?"))
        self.tbClear.setIcon(MIcon("Images:actionClear.png"))
        self.tbAddBookmark.setIcon(MIcon("Images:addBookmark.png"))
        self.tbDeleteBookmark.setIcon(MIcon("Images:actionDelete.png"))
        self.tbWhatDoesThisCommandDo.setIcon(MIcon("Images:whatDoesThisCommandDo.png"))
        self.tbClear.setAutoRaise(True)
        self.tbAddBookmark.setAutoRaise(True)
        self.tbDeleteBookmark.setAutoRaise(True)
        self.tbWhatDoesThisCommandDo.setAutoRaise(True)
        self.tbDeleteBookmark.setEnabled(False)

        MObject.connect(self.cbBookmarks, SIGNAL("currentIndexChanged(int)"), self.cbBookmarksChanged)
        MObject.connect(self.tbClear, SIGNAL("clicked()"), self.makeClear)
        MObject.connect(self.tbWhatDoesThisCommandDo, SIGNAL("clicked()"), self.whatDoesThisCommandDo)
        MObject.connect(self.tbAddBookmark, SIGNAL("clicked()"), self.addBookmark)
        MObject.connect(self.tbDeleteBookmark, SIGNAL("clicked()"), self.deleteBookmark)

        self.saccAvailable = SpecialActionsCommandContainer(self, "available", translate("SpecialActions", "Availables - Move Here Not To Use"))
        self.saccLeft = SpecialActionsCommandContainer(self, "left",
                                                       translate("SpecialActions", "Move Here To Use As Source"))
        self.saccRight = SpecialActionsCommandContainer(self, "right", translate("SpecialActions", "Move Here To Set"))

        saConcatenate = SpecialActionsCommandButton(self, "Concatenate")
        self.saccAvailable.addToWidgetList(saConcatenate)

        self.HBoxs = []
        self.HBoxs.append(MHBoxLayout())
        self.HBoxs[0].addWidget(self.cbBookmarks)
        self.HBoxs[0].addWidget(self.tbDeleteBookmark)
        self.HBoxs.append(MHBoxLayout())
        self.HBoxs[1].addWidget(self.saccAvailable)
        self.HBoxs.append(MHBoxLayout())
        self.HBoxs[2].addWidget(self.saccLeft, 10)
        self.HBoxs[2].addWidget(self.lblSplit, 1)
        self.HBoxs[2].addWidget(self.saccRight, 10)
        self.HBoxs[2].addWidget(self.tbClear, 1)
        self.HBoxs[2].addWidget(self.tbAddBookmark, 1)
        self.HBoxs[2].addWidget(self.tbWhatDoesThisCommandDo, 1)
        self.HBoxs.append(MHBoxLayout())
        vblSpecialActions = MVBoxLayout()
        vblSpecialActions.addLayout(self.HBoxs[0])
        vblSpecialActions.addLayout(self.HBoxs[1])
        vblSpecialActions.addLayout(self.HBoxs[2])
        self.setLayout(vblSpecialActions)
        self.cbBookmarks.setSizeAdjustPolicy(MComboBox.AdjustToMinimumContentsLength)
        self.refreshBookmarks()

    def showAdvancedSelections(self):
        for btn in self.pbtnAddObjects:
            btn.show()
        self.tbClear.show()
        self.tbWhatDoesThisCommandDo.show()
        self.tbAddBookmark.show()
        self.tbDeleteBookmark.show()
        self.saccAvailable.show()
        self.saccLeft.show()
        self.saccRight.show()
        self.lblSplit.show()

    def hideAdvancedSelections(self):
        for btn in self.pbtnAddObjects:
            btn.hide()
        self.tbClear.hide()
        self.tbWhatDoesThisCommandDo.hide()
        self.tbAddBookmark.hide()
        self.tbDeleteBookmark.hide()
        self.saccAvailable.hide()
        self.saccLeft.hide()
        self.saccRight.hide()
        self.lblSplit.hide()

    def getActionCommand(self):
        leftKeys = []
        for child in self.saccLeft.widgetList:
            objectName = str(child.objectName())
            point = str(child.getPoint())
            if objectName not in ["", "MoveHere"]:
                leftKeys.append(objectName + "~|~" + point)
        rightKeys = []
        for child in self.saccRight.widgetList:
            objectName = str(child.objectName())
            point = str(child.getPoint())
            if objectName not in ["", "MoveHere"]:
                rightKeys.append(objectName + "~|~" + point)
        return leftKeys + ["~||~"] + rightKeys

    def setActionCommand(self, _actionCommand):
        spliterIndex = _actionCommand.index("~||~")
        leftKeys = _actionCommand[:spliterIndex]
        rightKeys = _actionCommand[spliterIndex + 1:]
        for objectNameAndPoint in leftKeys:
            objectNameAndPointList = objectNameAndPoint.split("~|~")
            objectName = objectNameAndPointList[0]
            point = ""
            if len(objectNameAndPointList) > 1:
                point = objectNameAndPointList[1]
            if objectName.find("Concatenate") == -1:
                child = getChild(self.saccAvailable, objectName)
                if child is None:
                    child = getChild(self.saccLeft, objectName)
                if child is None:
                    child = getChild(self.saccRight, objectName)
            else:
                child = SpecialActionsCommandButton(self, objectName)
            child.setPoint(point)
            self.saccLeft.addToWidgetList(child)
        for objectNameAndPoint in rightKeys:
            objectNameAndPointList = objectNameAndPoint.split("~|~")
            objectName = objectNameAndPointList[0]
            point = ""
            if len(objectNameAndPointList) > 1:
                point = objectNameAndPointList[1]
            if objectName.find("Concatenate") == -1:
                child = getChild(self.saccAvailable, objectName)
                if child is None:
                    child = getChild(self.saccLeft, objectName)
                if child is None:
                    child = getChild(self.saccRight, objectName)
            else:
                child = SpecialActionsCommandButton(self, objectName)
            child.setPoint(point)
            self.saccRight.addToWidgetList(child)

    def makeClear(self):
        try:
            for child in getAllChildren(self.saccLeft):
                objectName = str(child.objectName())
                if objectName not in ["", "MoveHere"]:
                    self.saccAvailable.addToWidgetList(child)
            for child in getAllChildren(self.saccRight):
                objectName = str(child.objectName())
                if objectName not in ["", "MoveHere"]:
                    self.saccAvailable.addToWidgetList(child)
            self.saccAvailable.checkLabelMoveHere()
            self.saccLeft.checkLabelMoveHere()
            self.saccRight.checkLabelMoveHere()
        except:
            ReportBug.ReportBug()

    def whatDoesThisCommandDo(self):
        try:
            whatDoesSpecialCommandDo(self.getActionCommand(), True)
        except:
            ReportBug.ReportBug()

    def cbBookmarksChanged(self, _index):
        try:
            self.makeClear()
            if _index > 0:
                self.setActionCommand(eval(str(BookmarksOfSpecialTools.fetchAllByType()[_index - 1][2])))
                self.tbDeleteBookmark.setEnabled(True)
            else:
                self.tbDeleteBookmark.setEnabled(False)
        except:
            ReportBug.ReportBug()

    def addBookmark(self):
        try:
            if whatDoesSpecialCommandDo(self.getActionCommand()):
                BookmarksOfSpecialTools.insert(str(self.getActionCommand()))
                self.refreshBookmarks()
                self.cbBookmarks.setCurrentIndex(self.cbBookmarks.count() - 1)
        except:
            ReportBug.ReportBug()

    def deleteBookmark(self):
        try:
            if self.cbBookmarks.currentIndex() != -1 and self.cbBookmarks.currentIndex() != 0:
                BookmarksOfSpecialTools.delete(
                    BookmarksOfSpecialTools.fetchAllByType()[self.cbBookmarks.currentIndex() - 1][0])
                self.refreshBookmarks()
        except:
            ReportBug.ReportBug()

    def refreshBookmarks(self):
        try:
            self.makeClear()
            self.cbBookmarks.clear()
            self.cbBookmarks.addItem(translate("SpecialTools", "Please Select An Action!"))
            for fav in BookmarksOfSpecialTools.fetchAllByType():
                self.cbBookmarks.addItem(str(fav[1]))
        except:
            ReportBug.ReportBug()

    def checkCompleters(self):
        if uni.getBoolValue("isActiveCompleter"):
            pass

    def reFillCompleters(self):
        if uni.getBoolValue("isActiveCompleter"):
            pass

    def apply(self):
        self.checkCompleters()
        self.reFillCompleters()
        getMainTable().createHistoryPoint()
        actionCommand = self.getActionCommand()
        spliterIndex = actionCommand.index("~||~")
        leftKeys = actionCommand[:spliterIndex]
        rightKeys = actionCommand[spliterIndex + 1:]
        leftColumnKeys = []
        rightColumnKeys = []
        getMainTable().isAskShowHiddenColumn = True
        if len(leftKeys) > 0 and len(rightKeys) > 0:
            for objectNameAndPoint in leftKeys:
                leftColumnKeys.append(objectNameAndPoint)
            for objectNameAndPoint in rightKeys:
                objectNameAndPointList = objectNameAndPoint.split("~|~")
                objectName = objectNameAndPointList[0]
                if getMainTable().checkReadOnlyColumn(objectName):
                    rightColumnKeys.append(objectNameAndPoint)
        if len(leftColumnKeys) > 0 and len(rightColumnKeys) > 0:
            for rowNo in range(getMainTable().rowCount()):
                sourceString = ""
                sourceList = []
                sourceListLogical = []
                for no, objectNameAndPoint in enumerate(leftColumnKeys):
                    objectNameAndPointList = objectNameAndPoint.split("~|~")
                    objectName = objectNameAndPointList[0]
                    point = ""
                    if len(objectNameAndPointList) > 1:
                        point = objectNameAndPointList[1]
                    if objectName.find("Concatenate") == -1:
                        columnNo = getMainTable().tableColumnsKey.index(objectName)
                        valueOfField = str(getMainTable().item(rowNo, columnNo).text())
                        if objectName == "baseName":
                            valueOfField, ext = fu.getFileNameParts(valueOfField)
                        sourceString += valueOfField
                        sourceList.append(valueOfField)
                        if point != "":
                            sourceListLogical += valueOfField.split(point)
                        else:
                            sourceListLogical.append(valueOfField)
                        nextPoint = ""
                        if leftColumnKeys[-1] != objectNameAndPoint:
                            nextObjectNameAndPoint = leftColumnKeys[no + 1]
                            nextObjectNameAndPointList = nextObjectNameAndPoint.split("~|~")
                            nextObjectName = nextObjectNameAndPointList[0]
                            if len(nextObjectNameAndPointList) > 1:
                                nextPoint = nextObjectNameAndPointList[1]
                            if nextObjectName.find("Concatenate") == -1:
                                sourceString += "-"
                            else:
                                sourceString += nextPoint
                    else:
                        pass
                for no, objectNameAndPoint in enumerate(rightColumnKeys):
                    objectNameAndPointList = objectNameAndPoint.split("~|~")
                    columnKey = objectNameAndPointList[0]
                    columnNo = getMainTable().getColumnNoFromKey(columnKey)
                    if getMainTable().checkHiddenColumn(columnKey) is False:
                        continue
                    if getMainTable().isChangeableItem(rowNo, columnKey):
                        newString = ""
                        if len(rightColumnKeys) == 1:
                            newString = sourceString
                        elif len(sourceList) == len(rightColumnKeys):
                            newString = sourceList[no]
                        elif len(sourceListLogical) >= len(rightColumnKeys):
                            newString = sourceListLogical[no]
                        elif len(sourceListLogical) > no:
                            newString = sourceListLogical[no]
                        newString = Organizer.emend(newString)
                        if newString != "":
                            if self.specialTools.btChange.isChecked():
                                pass
                            elif self.specialTools.tbAddToBefore.isChecked():
                                newString += str(getMainTable().item(rowNo, columnNo).text())
                            elif self.specialTools.tbAddToAfter.isChecked():
                                newString = str(getMainTable().item(rowNo, columnNo).text()) + newString
                            getMainTable().item(rowNo, columnNo).setText(str(newString.strip()))


def whatDoesSpecialCommandDo(_actionCommand, _isShowAlert=False, _isReturnDetails=False):
    splitterIndex = _actionCommand.index("~||~")
    leftKeys = _actionCommand[:splitterIndex]
    rightKeys = _actionCommand[splitterIndex + 1:]
    if len(leftKeys) > 0 and len(rightKeys) > 0:
        details = ""
        leftNames = ""
        rightNames = ""
        for objectNameAndPoint in leftKeys:
            objectNameAndPointList = objectNameAndPoint.split("~|~")
            objectName = objectNameAndPointList[0]
            point = ""
            if len(objectNameAndPointList) > 1:
                point = objectNameAndPointList[1]
            if objectName.find("Concatenate") == -1:
                leftNames += getMainTable().getColumnNameFromKey(objectName)
            else:
                leftNames += translate("Organizer", "Concatenate")
            if point != "":
                if objectName.find("Concatenate") == -1:
                    leftNames += " " + (str(translate("Organizer", "(can be separated by \"%s\")")) % (point))
                else:
                    leftNames += " " + (str(translate("Organizer", "(can be concatenated by \"%s\")")) % (point))
            if leftKeys[-1] != objectNameAndPoint:
                leftNames += " ,"
        for objectNameAndPoint in rightKeys:
            objectNameAndPointList = objectNameAndPoint.split("~|~")
            objectName = objectNameAndPointList[0]
            point = ""
            if len(objectNameAndPointList) > 1:
                point = objectNameAndPointList[1]
            if objectName.find("Concatenate") == -1:
                rightNames += getMainTable().getColumnNameFromKey(objectName)
            else:
                rightNames += translate("Organizer", "Concatenate")
            if point != "":
                if objectName.find("Concatenate") == -1:
                    rightNames += " " + (str(translate("Organizer", "(can be separated by \"%s\")")) % (point))
                else:
                    rightNames += " " + (str(translate("Organizer", "(can be concatenated by \"%s\")")) % (point))
            if rightKeys[-1] != objectNameAndPoint:
                rightNames += " ,"

        details = str(translate("Organizer",
                                "\"%s\" will be concatenated and/or separated then it will be set as \"%s\" respectively.")) % (
                      leftNames, rightNames)

        if _isShowAlert:
            Dialogs.show(translate("Organizer", "What Does This Command Do?"), str(details))
        if _isReturnDetails is False:
            return True
        else:
            return details
    else:
        Dialogs.showError(translate("Organizer", "Missing Command"),
                          translate("Organizer", "You have to add at least a \"Column\"!.."))
        return False


class SpecialActionsCommandContainer(MFrame):
    def __init__(self, _parent, _containerKey, _moveHereLabel=False):
        MFrame.__init__(self, _parent)
        self.containerKey = _containerKey
        self.setAcceptDrops(True)
        self.HBox = MHBoxLayout()
        self.HBox1 = MHBoxLayout()
        self.HBox2 = MHBoxLayout()
        self.widgetList = []
        self.lblMoveHere = MLabel(_moveHereLabel, self)
        self.lblMoveHere.setObjectName("MoveHere")
        self.HBox.addWidget(self.lblMoveHere)
        self.VBox = MVBoxLayout()
        self.VBox.addLayout(self.HBox)
        self.VBox.addLayout(self.HBox1)
        self.VBox.addLayout(self.HBox2)
        self.setLayout(self.VBox)
        self.checkLabelMoveHere()
        self.setMinimumWidth(200)
        self.setContentsMargins(0, 0, 0, 0)
        self.layout().setContentsMargins(0, 0, 0, 0)
        self.setFrameShape(MFrame.StyledPanel)
        self.setFrameShadow(MFrame.Sunken)

    def addToLayout(self, _widget):
        if self.HBox.count() < 8:
            self.HBox.addWidget(_widget)
        elif self.HBox1.count() < 7:
            self.HBox1.addWidget(_widget)
        else:
            self.HBox2.addWidget(_widget)

    def addToWidgetList(self, _widget):
        try:
            self.removeFromOtherWidgetList(_widget)
            self.widgetList.append(_widget)
            self.addToLayout(_widget)
            self.checkLabelMoveHere()
            if self.parent().saccAvailable == self:
                _widget.hidePoint()
                if str(_widget.objectName()).find("Concatenate-") > -1:
                    _widget.hide()
            elif self.parent().saccLeft == self:
                _widget.showPoint()
            elif self.parent().saccRight == self:
                _widget.hidePoint()
        except:
            ReportBug.ReportBug()

    def removeFromOtherWidgetList(self, _widget):
        try:
            if _widget in self.parent().saccAvailable.widgetList:
                self.parent().saccAvailable.widgetList.remove(_widget)
                self.parent().saccAvailable.checkLabelMoveHere()
            if _widget in self.parent().saccLeft.widgetList:
                self.parent().saccLeft.widgetList.remove(_widget)
                self.parent().saccLeft.checkLabelMoveHere()
            if _widget in self.parent().saccRight.widgetList:
                self.parent().saccRight.widgetList.remove(_widget)
                self.parent().saccRight.checkLabelMoveHere()
        except:
            ReportBug.ReportBug()

    def dragEnterEvent(self, _e):
        if _e.mimeData().hasFormat("SpecialActionsCommandButton"):
            _e.accept()

    def dropEvent(self, _e):
        try:
            btn = _e.source()
            objectName = str(btn.objectName())
            if self.containerKey == "right" and objectName not in getMainTable().getWritableColumnKeys():
                Dialogs.toast(translate("SpecialTools", "This Column Is Readonly!"),
                              translate("SpecialTools", "You should move here writable columns!"))
            else:
                if objectName.find("Concatenate") == -1:
                    self.addToWidgetList(btn)
                else:
                    if btn not in self.widgetList:
                        if self == self.parent().saccAvailable:
                            self.addToWidgetList(btn)
                        elif self == self.parent().saccLeft:
                            child = SpecialActionsCommandButton(self.parent(), self.createNextConcatenateObjectName())
                            self.addToWidgetList(child)
                        elif self == self.parent().saccRight:
                            pass
                    else:
                        self.addToWidgetList(btn)  #
                _e.accept()
        except:
            ReportBug.ReportBug()

    def createNextConcatenateObjectName(self):
        objectName = "Concatenate-"
        i = 0
        while 1:
            newObjectName = objectName + str(i)
            isExist = False
            for _widget in (self.parent().saccAvailable.widgetList +
                            self.parent().saccLeft.widgetList +
                            self.parent().saccRight.widgetList):
                if str(_widget.objectName()) == newObjectName:
                    isExist = True
                    break
            if isExist:
                i += 1
            else:
                return newObjectName

    def checkLabelMoveHere(self):
        if len(self.widgetList) == 0:
            self.lblMoveHere.show()
        else:
            self.lblMoveHere.hide()


class SpecialActionsCommandButton(MFrame):
    def __init__(self, _parent, _columnNameKey):
        MFrame.__init__(self, _parent)
        self.setObjectName(_columnNameKey)
        if _columnNameKey.find("Concatenate") == -1:
            self.columnName = getMainTable().getColumnNameFromKey(_columnNameKey)
            toolTip = str(translate("SpecialActions",
                                    "If requires, \"%s\" will be separated by this. You can leave blank not to separate it.")) % (
                          self.columnName)
        else:
            self.columnName = translate("SpecialActions", "Concatenate")
            toolTip = str(translate("SpecialActions", "If requires, Side columns will be concatenated with this."))
        self.lblButton = MLabel(self.columnName, self)
        self.lblButton.setToolTip(self.columnName)
        self.lePoint = MLineEdit("", self)
        self.lePoint.setToolTip(toolTip)
        self.HBox = MHBoxLayout()
        self.HBox.addWidget(self.lblButton)
        self.HBox.addWidget(self.lePoint)
        self.setLayout(self.HBox)
        self.lePoint.hide()
        self.setMinimumHeight(20)
        self.setContentsMargins(1, 0, 1, 0)
        self.layout().setContentsMargins(1, 0, 1, 0)
        #self.setFrameShape(MFrame.Box)
        #self.setFrameShadow(MFrame.Plain)

    def setPoint(self, _value):
        self.lePoint.setText(str(_value))

    def getPoint(self):
        return str(self.lePoint.text())

    def showPoint(self):
        self.lePoint.show()
        self.lblButton.setText(self.columnName + ":")

    def hidePoint(self):
        self.lePoint.hide()
        self.lblButton.setText(self.columnName)

    def mouseMoveEvent(self, _e):
        try:
            if _e.buttons() != QtCore.Qt.LeftButton:
                return
            mimeData = QtCore.QMimeData()
            baData = MByteArray()
            baData.append(self.objectName())
            mimeData.setData("SpecialActionsCommandButton", baData)
            drag = QtGui.QDrag(self)
            drag.setMimeData(mimeData)
            dropAction = drag.start(QtCore.Qt.MoveAction)
        except:
            ReportBug.ReportBug()

    def mousePressEvent(self, _e):
        MFrame.mousePressEvent(self, _e)

            
    
    
