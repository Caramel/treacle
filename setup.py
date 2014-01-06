#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
	name='treacle',
	version='0.1.1',
	description=
		'treacle is an AGI (Asterisk Gateway Interface) script which handles '
		'public holidays and opening hours in different offices with different '
		'timezones and different public holidays.',
	author='Caramel',
	author_email='support@caramel.com.au',
	url='https://github.com/Caramel/treacle',
	license='LGPL3+',
	zip_safe=False,
	include_package_data=True,
	install_requires=[
		'distribute>=0.6.35',
		'pytz>=2012j',

		# There is an issue with iCalendar not pulling in this dependency, which is
		# only fixed in the development version.
		'python-dateutil>=2.1',

		'icalendar>=3.3',
		'configparser>=3.2.0r2',
		'argparse>=1.2.1',
		'requests>=1.1.0',
	],
	extras_require=dict(test=['nose']),
	packages=find_packages(),
	
	entry_points={
		'console_scripts': [
			'treacle = treacle.__main__:main',
			'treacle_scrape = treacle.scrape_apple_ical:main',
		]
	},
	
	classifiers=[
		# TODO
	],
)

