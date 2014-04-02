#!/usr/bin/env python
"""
Unit tests for treacle.
Copyright 2013-2014 Caramel <http://www.caramel.com.au/>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
from __future__ import absolute_import

# before importing Treacle, force locale
from os import environ
environ['LANG'] = 'C'
from treacle.treacle import Treacle
from os.path import dirname, abspath, join


TEST_PATH = abspath(dirname(__file__))


def dtend_missing_test():
	# setup some configuration for Treacle to use
	treacle = Treacle(config=dict(
	
		# default attributes.
		DEFAULT=dict(
			holidays=join(TEST_PATH, 'dtend_missing.ics'),
			tz='Australia/Adelaide',
			hours='Mon,Tue,Wed,Thu,Fri@09:00-17:30'
		),
		
		adel=dict(
		),
	), config_as_dict=True)

	# Exception for bug is thrown by Treacle constructor.

