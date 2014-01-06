#!/usr/bin/env python
"""
Scrape Apple's iCal public holiday feed for Australia.  This is part of Treacle.

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

import requests
from icalendar import Calendar, Event

IGNORED_EVENTS = [
	'mother\'s day',
	'father\'s day',
	'daylight saving time ends',
	'daylight saving time begins',
	'valentine\'s day',
	'remembrance day',

	# not full-day holidays, only from 19:00 - 00:00
	'christmas eve (sa)',
	'new year\'s eve (sa)',
]

def make_calendar():
	cal = Calendar()
	cal.add('prodid', '-//treacle-scrape_apple_ical//caramel.com.au//')
	cal.add('version', '2.0')
	
	return cal
	

def main():
	"""
	Scrapes Apple's iCal feed for Australian public holidays and generates per-
	state listings.
	
	"""
	print "Downloading Holidays from Apple's server..."
	r = requests.get('http://files.apple.com/calendars/Australian32Holidays.ics')
	
	cal = Calendar.from_ical(r.text)
	
	print "Processing calendar data..."
	
	valid_states = ['ACT', 'NSW', 'NT', 'QLD', 'SA', 'TAS', 'VIC', 'WA']
	
	state_cal = {}
	all_cal = make_calendar()
	
	for state in valid_states:
		state_cal[state] = make_calendar()
	
	for event in cal.walk('VEVENT'):
		event_name = event.decoded('SUMMARY').lower()
		if filter(lambda x: x in event_name, IGNORED_EVENTS):
			continue
		
		# see if there is a state or if it is for all
		if '(' in event_name: # and not 'day in lieu' in event_name:
			# it is just for certain states.
			# eg:
			#  - Easter Tuesday (TAS)
			#  - Labour Day (ACT, NSW, SA, QLD)
			states = event_name.split('(', 2)[1].split(')')[0].split(',')
			
			if states == ['day in lieu']:
				# only a day in lieu, switch to all-cal logic
				all_cal.add_component(event)
				continue

			for state in states:
				state = state.strip().upper()
				assert state in valid_states, 'state=%r' % state
				state_cal[state].add_component(event)
		else:
			# for all states
			all_cal.add_component(event)

	print "Writing to disk..."
	# done, write calendars.
	with open('au_holidays.ics', 'wb') as f:
		f.write(all_cal.to_ical())

	for state in state_cal.keys():
		with open('%s_holidays.ics' % state.lower(), 'wb') as f:
			f.write(state_cal[state].to_ical())
	
	print "All done!"


if __name__ == '__main__':
	main()

