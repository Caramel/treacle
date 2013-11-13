#!/usr/bin/env python
"""
Unit tests for treacle.
Copyright 2013 Caramel <http://www.caramel.com.au/>

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
	def parse_date(d):
		return datetime.strptime(d, '%Y-%m-%d').date()
	
	def parse_time(t):
		return datetime.strptime(t, '%H:%M').time()

	HOLIDAYS = [
		# anzac day
		'2011-04-25',
	
		# australia day
		'2011-01-26',
	
		# xmas
		'2011-12-25',
	
		# weekends
		'2012-06-02',
		'2012-06-30',
		'2012-07-07',
	]
	
	WORK_DAYS = [
		'2013-03-05',
		'2012-10-08',
	]

	VIC_HOLIDAYS = [	
		# melbourne cup
		'2012-11-06',
	]

	SA_HOLIDAYS = [
		# new years eve
		'2012-12-31',
	]


	ALL_HOURS = [
		'09:00',
		'10:00',
		'11:15',
		'14:00',
		'17:00'
	]
	
	NOT_ADEL_HOURS = [
		'08:15',
	]
	
	NOT_MELB_HOURS = [
		# expressed in adelaide time, -0.5hr
		'17:45',
	]

	NEVER_HOURS = [
		'00:00',
		'03:00',
		'19:00',
		'21:00'
	]
	
	sa = timezone('Australia/Adelaide')

	# setup some configuration for Treacle to use
	treacle = Treacle(config=dict(
	
		# default attributes.
		DEFAULT=dict(
			holidays=join(TEST_PATH, 'au_holidays_test.ics'),
			tz='Australia/Adelaide',
			hours='Mon,Tue,Wed,Thursday,Fri@08:00-18:00'
		),
		
		melb=dict(
			holidays_vic=join(TEST_PATH, 'vic_holidays_test.ics'),
			# Melbourne has a different timezone to default
			tz='Australia/Melbourne',
			# Use mix of short and long days for testing
			hours='Mon,Tuesday,Wed,Thu,Friday@08:30-18:00'
		),
		
		adel=dict(
			holidays_sa=join(TEST_PATH, 'sa_holidays_test.ics'),
			hours='Monday,Tue,Wed,Thu,Fri@08:30-18:00',
		
		),
		nuri=dict(
			holidays_sa=join(TEST_PATH, 'sa_holidays_test.ics')
		
		)
	), config_as_dict=True)
	
	# now use some days and see if we should work on them
	for d in HOLIDAYS:
		d = parse_date(d)
		
		for t in ALL_HOURS + NEVER_HOURS:
			dt = sa.localize(datetime.combine(d, parse_time(t)))
			
			assert not treacle.in_hours(when=dt), ('holiday %r was not marked as a global holiday' % (dt))

	
	for d in VIC_HOLIDAYS:
		d = parse_date(d)
		for t in ALL_HOURS:
			dt = sa.localize(datetime.combine(d, parse_time(t)))
			assert not treacle.in_hours(office='melb', when=dt), ('%r should not be work time' % dt)
			assert treacle.in_hours(office='adel', when=dt), ('%r should be work time' % dt)
		
		for t in NEVER_HOURS + NOT_MELB_HOURS:
			dt = sa.localize(datetime.combine(d, parse_time(t)))
			assert not treacle.in_hours(office='melb', when=dt), ('%r should not be work time' % dt)
	
	for d in WORK_DAYS:
		d = parse_date(d)
		for t in ALL_HOURS:
			dt = sa.localize(datetime.combine(d, parse_time(t)))
			for o in ('adel', 'nuri', 'melb'):
				assert treacle.in_hours(office=o, when=dt), ('%r should be work time in %r' % (dt, o))
				
		for t in NEVER_HOURS:
			dt = sa.localize(datetime.combine(d, parse_time(t)))
			for o in ('adel', 'nuri', 'melb'):
				assert not treacle.in_hours(office=o, when=dt), ('%r should not be work time in %r' % (dt, o))

		for t in NOT_ADEL_HOURS:
			dt = sa.localize(datetime.combine(d, parse_time(t)))
			assert not treacle.in_hours(office='adel', when=dt), ('%r should not be work time in adel' % dt)
			
			assert treacle.in_hours(office='melb', when=dt), ('%r should be work time in melb' % dt)
			assert treacle.in_hours(office='nuri', when=dt), ('%r should be work time in nuri' % dt)
			
		for t in NOT_MELB_HOURS:
			dt = sa.localize(datetime.combine(d, parse_time(t)))
			assert treacle.in_hours(office='adel', when=dt), ('%r should be work time in adel' % dt)
			
			assert not treacle.in_hours(office='melb', when=dt), ('%r should not be work time in melb' % dt)
			assert treacle.in_hours(office='nuri', when=dt), ('%r should be work time in nuri' % dt)
	

