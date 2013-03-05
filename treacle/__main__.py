#!/usr/bin/env python
"""
treacle: Business hours routing for Asterisk calls.
Written by Michael Farrell @ Caramel (2013)
"""

from __future__ import absolute_import
from treacle.treacle import Treacle
from argparse import ArgumentParser, FileType

DEFAULT_CONFIG = '/etc/treacle/treacle.ini'


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
		print "SET VARIABLE %s \"%s\"" % (options.agi_variable, 1 if r else 0)
		
	
	


if __name__ == '__main__':
	main()
