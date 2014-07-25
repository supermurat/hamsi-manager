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


import sys
import os

def checkMyModules(_HamsiManagerApp):
    try:
        import SpecialTools
        import Tables
        from Core import FileManager
        import Bars

        return True
    except ImportError as error:
        from PyQt4 import QtGui
        from PyQt4 import QtCore

        errorForm = QtGui.QWidget()
        errorForm.vblMain = QtGui.QVBoxLayout(errorForm)
        if str(error)[16:].find(" ") == -1:
            title = str(QtGui.QApplication.translate("ReportBug", "Missing Module"))
            startNumber = 16
            details = str(
                QtGui.QApplication.translate("ReportBug", "Application will not work without the module \"%s\"."))
        else:
            title = str(QtGui.QApplication.translate("ReportBug", "Error In Module"))
            startNumber = 19
            details = str(QtGui.QApplication.translate("ReportBug",
                                                       "\"%s\" is not in this module.Please download and install Hamsi Manager again."))
        lblDetails = QtGui.QLabel(str("<b>" + title + ":</b><br>" + (details % (str(error)[startNumber:]))))
        pbtnOk = QtGui.QPushButton(QtGui.QApplication.translate("ReportBug", "OK"))
        errorForm.connect(pbtnOk, QtCore.SIGNAL("clicked()"), _HamsiManagerApp.quit)
        hbox0 = QtGui.QHBoxLayout()
        hbox0.addStretch(2)
        hbox0.addWidget(pbtnOk, 1)
        errorForm.vblMain.addWidget(lblDetails)
        errorForm.vblMain.addLayout(hbox0)
        errorForm.setWindowTitle(QtGui.QApplication.translate("ReportBug", "Critical Error!"))
        errorForm.show()
        sys.exit(_HamsiManagerApp.exec_())


def checkMandatoryModules():
    try:
        from PyQt4 import QtGui, QtCore

        if os.name == "nt":
            pywin32IsAvailable = False
            try:
                import win32api, win32con, win32com

                pywin32IsAvailable = True
            except: pass
            if pywin32IsAvailable is False:
                app = QtGui.QApplication(sys.argv)
                w = QtGui.QWidget()
                l = QtGui.QVBoxLayout(w)
                pbtn = QtGui.QPushButton('Quit', w)
                pbtn.clicked.connect(QtCore.QCoreApplication.instance().quit)
                lblAlert = QtGui.QLabel(
                    "<br><b><a href='https://sourceforge.net/projects/pywin32/'>'Python for Windows Extensions'</a> (pywin32) named module has NOT installed on your system.</b><br><br>You have to install it on your system to run Hamsi Manager.<br><br>",
                    w)
                lblAlert.setOpenExternalLinks(True)
                l.addWidget(lblAlert)
                l.addWidget(pbtn)
                w.setLayout(l)
                w.setWindowTitle('Critical Error!')
                w.show()
                w.setMinimumWidth(400)
                sys.exit(app.exec_())
        return True
    except:
        try:
            import qt

            qtHamsiManagerApp = qt.QApplication(sys.argv)
            panel = qt.QWidget()
            panel.vblMain = qt.QVBoxLayout(panel)
            lblInfo = qt.QLabel(
                "<br><b>PyQt4 is not installed:</b><br>You have to install \"PyQt4\" on your system to run Hamsi Manager.",
                panel)
            pbtnClose = qt.QPushButton("OK", panel)
            panel.connect(pbtnClose, qt.SIGNAL("clicked()"), qtHamsiManagerApp.quit)
            hbox0 = qt.QHBoxLayout()
            hbox0.addStretch(2)
            hbox0.addWidget(pbtnClose, 1)
            vbox0 = qt.QVBoxLayout()
            vbox0.addWidget(lblInfo)
            vbox0.addLayout(hbox0)
            hbox1 = qt.QHBoxLayout()
            hbox1.addStretch(20)
            hbox1.addLayout(vbox0, 500)
            hbox1.addStretch(5)
            panel.vblMain.addLayout(hbox1)
            panel.setCaption("Critical Error!")
            panel.show()
            panel.setMinimumWidth(400)
            qtHamsiManagerApp.enter_loop()
        except:
            try:
                import gtk

                def destroy(widget, data=None):
                    gtk.main_quit()

                window = gtk.Window(gtk.WINDOW_TOPLEVEL)
                window.connect("destroy", destroy)
                window.set_title("Critical Error!")
                button = gtk.Button("OK")
                label = gtk.Label("PyQt4 is not installed.")
                label2 = gtk.Label("You have to install \"PyQt4\" on your system to run Hamsi Manager.")
                label2.set_line_wrap(True)
                button.connect("clicked", gtk.main_quit, None)
                vbox = gtk.VBox(False, 5)
                hbox = gtk.HBox(window)
                window.add(hbox)
                hbox.pack_start(vbox, False, False, 0)
                window.set_border_width(5)
                hbox0 = gtk.HBox(False)
                hbox0.pack_start(label, 0, 0, 0)
                hbox1 = gtk.HBox(False)
                label3 = gtk.Label("")
                hbox1.pack_start(label3, 0, 0, 0)
                hbox1.pack_start(button, 0, 0, 0)
                vbox.pack_start(hbox0, False, False, 0)
                vbox.pack_start(label2, False, False, 0)
                vbox.pack_start(hbox1, False, False, 0)
                layout = gtk.Layout(None, None)
                button.set_size_request(120, 25)
                label2.set_size_request(350, 35)
                label3.set_size_request(230, 25)
                window.show_all()
                gtk.main()
            except:
                try:
                    import Tkinter

                    tMainWindow = Tkinter.Tk()
                    tMainWindow.geometry("350x100")
                    tMainWindow.title("Critical Error!")
                    lbl1 = Tkinter.Label(text="PyQt4 is not installed.")
                    lbl1.pack()
                    lbl2 = Tkinter.Label(text="You have to install \"PyQt4\"")
                    lbl2.pack()
                    lbl3 = Tkinter.Label(text="on your system to run HamsiManager.")
                    lbl3.pack()
                    btnClose = Tkinter.Button(text="OK", command=tMainWindow.quit)
                    btnClose.pack(side=Tkinter.RIGHT)
                    Tkinter.mainloop()
                except:
                    print ("Critical Error!")
                    print ("You have to install \"PyQt4\" on your system to run Hamsi Manager.")
        return False




