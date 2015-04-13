#!/usr/bin/python
# -*- coding: utf-8 -*-
##
# custom_widgets.py: Defines some custom widgets we will need
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

from PySide import QtGui, QtCore
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
 
from matplotlib.figure import Figure
 
## CLASSES ####################################################################

class MplCanvas(FigureCanvas):
 
    def __init__(self):
        self.fig = Figure()
        self.ax = self.fig.add_subplot(111)
        # set face color in RGBA -- not sure why it doesn't appear the same color as surroundings
        self.fig.set_facecolor([1,1,1,0])
 
        FigureCanvas.__init__(self, self.fig)
        FigureCanvas.setSizePolicy(self, QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
 
 
class MatplotlibWidget(QtGui.QWidget):
 
    def __init__(self, parent = None):
        QtGui.QWidget.__init__(self, parent)
        self.canvas = MplCanvas()
        self.vbl = QtGui.QVBoxLayout()
        self.vbl.addWidget(self.canvas)
        self.setLayout(self.vbl) 

class DataTableWidget(QtGui.QTableWidget):
    """
    Displays the data in a QTableWidget.

    :param data.`RBData` data: The data object.
    :param parent: Usual QtGui parent option, should be a QTabWidget in this case.
    """

    def __init__(self, parent=None, data=None):
        QtGui.QTableWidget.__init__(self, parent=parent)

        self.data = data

    def redraw(self):

        if self._data is None:
            self.clear()
            self.setRowCount(0)
            self.setColumnCount(0)
        else:
            self.clear()
            self.setRowCount(0)
            self.setColumnCount(0)

            hor_headers = []
            for idx_seq, seq_length in enumerate(self._data.seq_lengths):
                self.insertColumn(idx_seq)
                hor_headers.append("{}".format(seq_length))
            for idx_throw in xrange(self._data.n_throws):
                self.insertRow(idx_throw)
            self.setHorizontalHeaderLabels(hor_headers)
            #self.setVerticalHeaderLabels(["Sequence Lengths"])
            
            for idx_seq, seq_length in enumerate(self._data.seq_lengths):
                for idx_throw in xrange(self.data.n_throws):
                    item = QtGui.QTableWidgetItem("{}".format(self._data.raw_data[idx_seq, idx_throw]))
                    self.setItem(idx_throw, idx_seq, item)
            self.resizeColumnsToContents()
            self.resizeRowsToContents()

    @property
    def data(self):
        return self._data
    @data.setter
    def data(self, value):
        self._data = value
        self.redraw()
    

class DataTabWidget(QtGui.QWidget):
    """
    Represents the contents of a data tab.

    :param data.`RBData` data: The data object.
    :param parent: Usual QtGui parent option, should be a QTabWidget in this case.
    """

    def __init__(self, parent=None, data=None):
        QtGui.QWidget.__init__(self, parent=parent)

        # Most of the formatting commands invoked in this constructor were just copied 
        # from what pyside-uic does...no great thought went into them
        self.setObjectName("_bg_widget")

        self._hor_layout = QtGui.QHBoxLayout(self)
        self._hor_layout.setObjectName("_hor_layout")

        self.table = DataTableWidget(data=data, parent=self)
        size_policy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.MinimumExpanding)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(self.table.sizePolicy().hasHeightForWidth())
        self.table.setSizePolicy(size_policy)
        self.table.setMinimumSize(QtCore.QSize(0, 100))
        self.table.setObjectName("table_data_{}".format(self.table.data.name.replace(" ", "")))

        self._hor_layout.addWidget(self.table)

    def redraw(self):
        self.table.redraw()

    @property
    def data(self):
        return self._data
    @data.setter
    def data(self, value):
        self._data = value
        self.redraw()