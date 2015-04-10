#!/usr/bin/python
# -*- coding: utf-8 -*-
##
# matplotlib_widget.py: Defines QWidget subclass matplotlibWidget
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


from PySide import QtGui
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
 
from matplotlib.figure import Figure
 
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