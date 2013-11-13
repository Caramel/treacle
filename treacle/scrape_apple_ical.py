#!/usr/bin/env python
"""
Scrape Apple's iCal public holiday feed for Australia

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
	
	states = ['ACT', 'NSW', 'NT', 'QLD', 'SA', 'TAS', 'VIC', 'WA']
	
	state_cal = {}
	all_cal = make_calendar()
	
	for state in states:	
		state_cal[state] = make_calendar()
	
	for event in cal.walk('VEVENT'):
		event_name = event.decoded('SUMMARY')
		if event_name.lower() in IGNORED_EVENTS:
			continue
		
		# see if there is a state or if it is for all
		if '(' in event_name and not 'day in lieu' in event_name:
			# it is just for certain states.
			# eg:
			#  - Easter Tuesday (TAS)
			#  - Labour Day (ACT, NSW, SA, QLD)
			states = event_name.split('(', 2)[1][:-1].split(',')
			
			for state in states:
				state = state.strip().upper()
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

