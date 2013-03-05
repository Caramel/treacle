#!/usr/bin/env python
"""
treacle: Business hours routing for Asterisk calls.
Written by Michael Farrell (2013)
"""


from configparser import ConfigParser
from argparse import ArgumentParser, FileType
from pytz import timezone, utc
from calendar import day_abbr, day_name
from datetime import datetime
from icalendar import Calendar


DEFAULT_CONFIG = '/etc/treacle.ini'
LOCALE_SHORT_DAYS = [x.lower() for x in day_abbr]
LOCALE_LONG_DAYS = [x.lower() for x in day_name]


class Office(object):
	"""
	Parses an configuration of an office which has hours.
	
	"""
	
	def __init__(self, config, section):
		# find all the holiday files that are referenced
		self.tz = None
		self.name = section
		self.hours = {}
		self.holidays = []
		
		for option, value in config.items(section):
			if option.startswith('holidays'):
				# read in a holidays file
				self.holidays.extend(self._read_holidays(value))
				
				
			elif option == 'tz':
				# read timezone
				# throws error if invalid
				self.tz = timezone(value)
				
			elif option.startswith('hours'):
				# read hours
				
				days, hours = value.split('@', 2)
				days = [x.lower() for x in days.split(',')]

				# day offsets all found, parse the time range
				# eg: "09:00-17:00"
				start, end = [datetime.strptime(t.strip(), '%H:%M').time() for t in hours.split('-', 2)]
				
				assert start < end, 'start time is after end time'
				
				# attempt to parse days specified, using long-form days (Monday) before short-form (Mon)
				days_i = []
				for day in days:
					try:
						day_i = LOCALE_LONG_DAYS.index(day)
					except ValueError:
						try:
							day_i = LOCALE_SHORT_DAYS.index(day)
						except ValueError:
							# not valid
							raise ValueError, '%r does not appear to be a valid short or long-form day in your locale' % day
					
					# now push this into the hours dict
					
					if day_i not in self.hours:
						self.hours[day_i] = []
					
					self.hours[day_i].append((start, end))
				
				
			else:
				raise ValueError, 'unknown option %r' % option
	
	def _read_holidays(self, filename):
		"""
		Read holidays from an iCalendar-format file.
		"""
		cal = Calendar.from_ical(open(filename, 'rb').read())
		
		for component in cal.walk('VEVENT'):
			yield component.decoded('DTSTART')
			
	def in_hours(self, when):
		"""
		Find if the given datetime is in business hours.
		
		:param when: The time to check
		:type when: datetime.datetime
		
		:returns: True if the given time is in business hours for the office, False otherwise.
		:rtype: bool
		
		"""
		
		# convert to local timezone
		when = when.astimezone(self.tz)
		
		# is it a public holiday?
		if when.date() in self.holidays:
			return False
		
		# is it a work day?
		if when.weekday() not in self.hours:
			# not a work day
			return False
		
		# work out if it is one of the ranges
		for start, end in self.hours[when.weekday()]:
			if start <= when.time() <= end:
				# it's in that range
				return True
				
		# not in any range of hours, and was on a work day
		return False

class Treacle(object):
	def __init__(self, config=None):
		self.config = ConfigParser(strict=True)
		self.config.read_file(config)

		self._parse_config()
		
	def _parse_config(self):
		self.offices = {}
		for section in self.config.sections():
			self.offices[section] = Office(self.config, section)
			
			
		
	def in_hours(self, office=None, when=None):
		"""
		Finds if it is business hours in the given office.
		
		:param office: Office ID to look up, or None to check if any office is in business hours.
		:type office: str or NoneType
		
		:param when: When to check the office is open, or None for now.
		:type when: datetime.datetime
		
		
		:returns: True if it is business hours, False otherwise.
		:rtype: bool
		
		Raises KeyError if the office is unknown.
		
		"""
		
		if when == None:
			when = datetime.now(tz=utc)
		
		if office == None:
			for office in self.offices.itervalues():
				if office.in_hours(when):
					return True
			
			return False
			
		else:
			# check specific office
			return self.offices[office].in_hours(when)
		
		
	


def main():
	parser = ArgumentParser(
		description="treacle provides in-hours call routing for Asterisk"
	)
	
	group = parser.add_mutually_exclusive_group(required=True)

	group.add_argument('-a', '--agi',
		dest='agi_variable',
		default='CARHOURS',
		metavar='VAR',
		nargs='?',
		help=
			'Expect an Asterisk AGI session to handle hours-routing, setting '
			'the following dialplan variable to 1 in the case of it being '
			'office hours. '
			'[default: %(default)s]'
	)

	group.add_argument('-s', '--standalone',
		dest='standalone',
		action='store_true',
		default=False,
		help=
			'Run in stand-alone mode, returning error code 0 if in-hours, and '
			'1 otherwise.'
		
	)

	parser.add_argument('-c', '--config',
		dest='config',
		default=None,
		type=FileType('rb'),
		help='Configuration INI file to use [default: %s]' % DEFAULT_CONFIG,
		required=False
	)
	
	group = parser.add_mutually_exclusive_group(required=True)
	
	group.add_argument('-o', '--office',
		metavar='OFFICE',
		dest='office',
		nargs='?',
		help='Office to look up'
	)
	
	group.add_argument('-A', '--any',
		dest='any_state',
		action='store_true',
		default=False,
		help='Look up if any state may take calls at this time.'
	)

	options = parser.parse_args()
	
	if not options.config:
		options.config = open(DEFAULT_CONFIG, 'rb')
	
	# start doing things!
	# parse configuration
	t = Treacle(options.config)
	
	if options.any_state:
		r = t.in_hours()
	else:
		r = t.in_hours(options.office)
	
	if options.standalone:
		# throw exit code as appropriate
		exit(0 if r else 1)
	else:
		# handle agi
		print "lol agi %r" % r
		
	
	


if __name__ == '__main__':
	main()
