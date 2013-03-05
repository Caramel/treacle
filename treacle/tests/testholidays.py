#!/usr/bin/env python

from __future__ import absolute_import

# before importing Treacle, force locale
from os import environ
environ['LANG'] = 'C'

from treacle.treacle import Treacle
from os.path import dirname, abspath, join


TEST_PATH = abspath(dirname(__file__))


def exampleHolidaysTest():
	# setup some configuration for Treacle to use
	t = Treacle(config=dict(
	
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

