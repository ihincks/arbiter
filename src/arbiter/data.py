#!/usr/bin/python
# -*- coding: utf-8 -*-
##
# data.py: Structures for RB data storing and handling
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

## FEATURES ###################################################################

from __future__ import division # Ensures that a/b is always a float.

## IMPORTS ####################################################################

import numpy as np

## FUNCTIONS ##################################################################

## CLASSES ####################################################################

class RBData(object):
	r"""
	Structure that contains RB data and meta data corresponding to a 
	single fidelity decay.

	:param name str: Name to assign data
    :param numpy.ndarray data: Array of shape [1+2*referenced, n_seq, n_throws]
    :param numpy.ndarray seq_lengths: List of RB sequence lengths. If set to 
    	`None`, chooses sequential integers.
    :param int n_shots: Number of experiments per throw; binomial parameter.
    :param bool ragged: If `True`, negative data are interpretted as no data.
	"""

	def __init__(self, name, data, seq_lengths=None, n_shots=1, ragged=False):
		self._name = name
		self._data = data
		# TODO: implement ragged everywhere
		self._ragged = ragged
		self._n_shots = n_shots
		if seq_lengths is None:
			self._seq_lengths = np.arange(self.n_seq)+1
		else:
			self._seq_lengths = seq_lengths

	@property
	def name(self):
		# Human readable name of data
	    return self._name

	@property
	def seq_lengths(self):
		# List of sequence lengths (often labeled "m")
		return self._seq_lengths

	@property
	def n_seq(self):
		# Number of sequence lengths used
	    return self._data.shape[1]

	@property
	def referenced(self):
		# Whether or not the data is referenced to upper and lower calibration curves
		return self._data.shape[0] > 1

	@property
	def n_shots(self):
		# Number of experiments performed per throw; the binomial parameter
	    return self._n_shots
	
	@property
	def n_throws(self):
		# Number of random sequences chosen per sequence length
		return self._data.shape[2]

	@property
	def raw_data(self):
		# Raw unreferenced data
		return self._data[0,...]

	@property
	def references(self):
		# Upper and lower references
		if self.referenced:
			return self._data[1:,...]
		else:
			return np.concatenate(
				(
					self.n_shots * np.ones((1, self.n_seq, self.n_throws)),
					np.zeros((1, self.n_seq, self.n_throws))
				),
				axis=0
			)

	@property
	def upper_references(self):
		# Upper references; same shape as raw_data
		return self.references[0,...]

	@property
	def lower_references(self):
		# Lower references; same shape as raw_data
		return self.references[1:,...]

	@property
	def data(self):
		# Data referenced to (nominally) be between 0 and 1
		return (
			self.raw_data *
				(self.upper_references - self.lower_references)
			+ self.lower_references
		)
	
	


class RBDataCollection(object):
	r"""
    Structure that contains RB data and meta data for multiple 
    RB fidelity decay curves.
    
    :param arbitor.`RBData` data: Data to initially add to collection.
    """
	def __init__(self, data=None):
		self._data_list = []
		if data is not None:
			self.add_data(data)


	def add_data(self, data):
		"""
		Adds the given data to the data collection.

		:param arbitor.`RBData` data: Data to add.
		"""
		self._data_list.append(data)

	@property
	def data(self):
	    return self._data_list
	

