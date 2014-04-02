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
from pytz import timezone
from datetime import datetime
from os.path import dirname, abspath, join


TEST_PATH = abspath(dirname(__file__))



def holidays_test():
	def parse_datetime(d):
		return datetime.strptime(d, '%Y-%m-%d %H:%M')

	HOLIDAYS = [
		# Friday is closed
		'2014-03-28 14:00',

		'2014-03-25 21:15', # part day
		'2014-03-27 20:00', # full day

		# multiple full days
		'2014-03-30 19:00',
		'2014-03-31 18:00',
	]

	WORK_DAYS = [
		# Part day
		'2014-03-25 15:00',

		# Normal days
		'2014-03-26 15:30',
		'2014-04-01 16:00',
	]

	sa = timezone('Australia/Adelaide')

	# setup some configuration for Treacle to use
	treacle = Treacle(config=dict(
	
		# default attributes.
		DEFAULT=dict(
			holidays=join(TEST_PATH, 'partdays.ics'),
			tz='Australia/Adelaide',
			hours='Mon,Tue,Wed,Thursday,Sat,Sun@12:00-23:00'
		),
		
		adel=dict(
		),
	), config_as_dict=True)

	# now use some days and see if we should work on them
	for d in HOLIDAYS:
		dt = sa.localize(parse_datetime(d))
		
		assert not treacle.in_hours(when=dt), ('holiday %r was not marked as a holiday' % (dt))

	for d in WORK_DAYS:
		dt = sa.localize(parse_datetime(d))
		assert treacle.in_hours(when=dt), ('work day %r was marked as a holiday' % (dt))


