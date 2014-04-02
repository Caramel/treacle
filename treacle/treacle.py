#!/usr/bin/env python
"""
treacle: Business hours routing for Asterisk calls.
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

from configparser import ConfigParser, NoOptionError
from pytz import timezone, utc
from calendar import day_abbr, day_name
from datetime import datetime, date, time, timedelta
from icalendar import Calendar

__all__ = [
	'Office',
	'Treacle'
]


LOCALE_SHORT_DAYS = [x.lower() for x in day_abbr]
LOCALE_LONG_DAYS = [x.lower() for x in day_name]


class Office(object):
	"""
	Represents an office configuration for Treacle.

	This class should only be instantiated by :class:`~treacle.Treacle`, not by
	user applications.

	:param configparser.ConfigParser config: Configuration object to use.
	:param str section: Name of the section to read this office's configuration from.
	"""

	def __init__(self, config, section):
		# find all the holiday files that are referenced
		self.tz = utc
		self.name = section
		self.hours = {}
		self.holidays = []

		# Read time zone first, other things need it.  Throws error if invalid.
		try:
			self.tz = timezone(config.get(section, 'tz'))
		except NoOptionError: pass

		for option, value in config.items(section):
			if option.startswith('holidays'):
				# read in a holidays file
				self.holidays.extend(self._read_holidays(value))

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

			elif option == 'tz':
				# already parsed above.
				pass
			else:
				raise ValueError, 'unknown option %r' % option

	def _read_holidays(self, filename):
		"""
		Read holidays from an iCalendar-format file.
		"""
		cal = Calendar.from_ical(open(filename, 'rb').read())
		holidays = []

		for component in cal.walk('VEVENT'):
			start = component.decoded('DTSTART')
			try:
				end = component.decoded('DTEND')
			except KeyError:
				# RFC allows DTEND to be missing
				if isinstance(start, datetime):
					# For DATETIME instances, the event ends immediately.
					end = start
				elif isinstance(start, date):
					# For DATE instances, the event ends tomorrow
					end = start + timedelta(days=1)
				else:
					raise KeyError, 'DTEND is missing and DTSTART is not of DATE or DATETIME type'

			if isinstance(start, date) and not isinstance(start, datetime):
				assert (isinstance(end, date) and not isinstance(end, datetime)), \
					'DTSTART is of DATE type but DTEND is not of DATE type (got %r instead)' % type(end)
				# All-day event, set times to midnight local time
				start = datetime.combine(start, time.min)
				end = datetime.combine(end, time.min)

			# check for TZ data
			if start.tzinfo is None or end.tzinfo is None:
				# One of them is missing tzinfo, replace both with this office's
				# local time.  Assume standard time if ambiguous.
				start = self.tz.localize(start, is_dst=False)
				end = self.tz.localize(end, is_dst=False)

			yield (start, end)


	def in_hours(self, when):
		"""
		Find if the given :class:`~datetime.datetime` is in business hours for
		this office.

		:param datetime.datetime when: The time to check

		:returns: True if the given time is in business hours for the office, False otherwise.
		:rtype: bool

		"""

		# convert to local timezone
		when = when.astimezone(self.tz)

		# is it a work day?
		if when.weekday() not in self.hours:
			# not a work day
			return False

		# work out if it is one of the ranges
		for start, end in self.hours[when.weekday()]:
			if start <= when.time() <= end:
				# it's in that range

				# is it a public holiday?  check if it is any range
				for hstart, hend in self.holidays:
					if when >= hstart and when <= hend:
						# it's inside a holiday area.
						return False

				# not in a holiday zone, which means it's business time.
				return True

		# not in any range of hours, and was on a work day
		return False

class Treacle(object):
	"""
	Class for calculating office hours in multiple offices.

	:param config: Configuration source to use.  This uses syntax defined in :doc:`configuring`.
	:type config: file or dict

	:param boot config_as_dict: Treat the parameter ``config`` as a :class:`dict` rather than a :class:`file`, if True.  This is useful when passing in configuration from a non-file source, such as for unit testing.

	"""
	def __init__(self, config, config_as_dict=False):
		self.config = ConfigParser(strict=True)
		if config_as_dict:
			self.config.read_dict(config)
		else:
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
		:type office: str or None

		:param datetime.datetime when: When to check the office is open, or None for now.

		:returns: True if it is business hours, False otherwise.
		:rtype: bool

		:raises KeyError: If the office is unknown.

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

