#!/usr/bin/python
# -*- coding: utf-8 -*-
##
# main_window.py: Main window of Arbiter
##
# © 2015 Ian Hincks (ian.hincks@gmail.com)
#
# This file is a part of the Arbiter project.
# Licensed under the AGPL version 3.
##
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
##

## IMPORTS ####################################################################

import matplotlib
# Ensure that matplotlib is using Qt, so that the event loop is compatible.
matplotlib.use('Qt4Agg')
# Solve issue mentioned at:
# http://stackoverflow.com/questions/6723527/getting-pyside-to-work-with-matplotlib
matplotlib.rcParams['backend.qt4'] = 'PySide'
# Actually import pyplot now that the backend is correct.
import matplotlib.pyplot as plt


import ui.arbiter_gui
import data
import os, sys
import numpy as np
from PySide import QtGui
from ui.custom_widgets import DataTabWidget

# This needs to be done in order for the Windows task bar to group this 
# program separately from the IPython icon.
# http://stackoverflow.com/questions/1551605/how-to-set-applications-taskbar-icon
if sys.platform.startswith('win'):
    import ctypes
    myappid = 'arbiter.main_window' # arbitrary string
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

## FUNCTIONS ##################################################################

def tablewidget_text(tb_widget, row, col):
    item = tb_widget.item(row, col)
    if item is None:
        return None
    else:
        return item.text()

## CLASSES ####################################################################

class MainWindow(QtGui.QMainWindow):
    def __init__(self, parent=None):
        # Call the superclass constructor.
        super(MainWindow, self).__init__(parent)

        # Inflate the UI generated by pyside-uic.
        self._ui = ui.arbiter_gui.Ui_MainWindow()
        self._ui.setupUi(self)

        # Remove dummy tabs created by Qt Designer
        while self._ui.tabs_data.count() > 0:
            self._ui.tabs_data.removeTab(0)
        
        # Attach event handlers to the appropriate signals.
        self._ui.button_import.clicked.connect(
            lambda: self.add_data_tab(data.RBData("Oh Yeah", np.random.randint(5,size=(1,200,50))))
        )

    def add_data_tab(self, d):
        new_tab = DataTabWidget(data=d)
        self._ui.tabs_data.addTab(new_tab, d.name)

            
## MAIN #######################################################################

if __name__ == "__main__":
    app = QtGui.QApplication('"Arbiter"')
    app.setApplicationName("Arbiter")
    
    main_win = MainWindow()
    main_win.show()


    t = np.arange(0,10*np.pi,0.1)
    main_win._ui.plot_data.canvas.ax.plot(t, np.sin(t))
    main_win._ui.plot_data.canvas.draw()
    
    d = data.RBData("Oh Yeah",np.random.randint(5,size=(1,200,50)))
    main_win.add_data_tab(d)

    icon_path = os.path.realpath('../../img/icon.png')
    app.setWindowIcon(QtGui.QIcon(icon_path))
    main_win.setWindowIcon(QtGui.QIcon(icon_path))

    main_win.showMaximized()

    app.exec_()
