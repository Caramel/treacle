************
Data sources
************

Data sources are given as iCalendar files.  You can create these yourself, or download them from various sources online.

Recurring events are not supported by this software.

All events inside of the iCalendar file are read using the `icalendar <https://pypi.python.org/pypi/icalendar>`_ library, so will inherit it's limitations.

Events that don't have a direct, Olson timezone name on them won't carry timezone information.  In this case, ``treacle`` will make the events be interpreted in the timezone for the office being read (this includes those inherited from defaults).  If any calendar entry lands within a daylight savings transition point, if the time is ambiguous or non-existent, it is assumed to be within "standard" time.

This applies even if there is ``VTIMEZONE`` information in the calendar file.  This is a `known issue in icalendar <https://github.com/collective/icalendar/issues/44>`_.


Australian Holiday Data
=======================

Official government data sources
--------------------------------

Some states release official iCalendar feeds of public holidays:

* `Australian Capital Territory <http://www.cmd.act.gov.au/communication/holidays/public-holidays-ical/public-holidays>`_
* `South Australia <http://www.safework.sa.gov.au/uploaded_files/holidayCalendar.ics>`_
* `Victoria <http://www.vic.gov.au/ical/holidays.html>`_


.. highlight:: console


Scraping Apple for public holidays
----------------------------------

For Australian users, a tool is included to scrape the Apple iCal public
holiday feeds. In order to use this after you have installed the
software::

	$ treacle_scrape

This will produce the following files in the current directory:

-  ``au_holidays.ics`` - Contains holidays specific to no state (national holidays)
-  ``act_holidays.ics`` - Contains holidays specific to ACT
-  ...and so on for ``nsw``, ``nt``, ``qld``, ``sa``, ``tas``, ``vic`` and ``wa``.

This script will blindly overwrite these files in the directory, so be
careful!

.. note::

	This doesn't take into account a number of quirks of public holidays in various states.

	For example, in South Australia, Christmas Eve and New Years Eve are public holidays for part of the day.  These aren't listed at all.

	In Tasmania, there are holidays that only apply for certain cities.  Apple appears to only provide information about holidays in Hobart.


Special office closures
=======================

If you wish to have a special calendar with office closures in it, you can create another iCalendar file with these closures in it, and add it as a holiday source.

Because this software doesn't run as a daemon, you can update the calendar file whenever you like, and this will apply to all calls recieved after this point.  For example::

	[DEFAULT]
	holidays = /etc/treacle/holidays/au_holidays.ics
	holidays_closed = /etc/treacle/holidays/exampleco_cloures.ics

	[adel]
	holidays_sa = /etc/treacle/holidays/sa_holidays.ics
	hours = Mon,Tue,Wed,Thu,Fri@09:00-17:30

The holidays ICS files can be updated from an external source, and :file:`exampleco_closures.ics` would contain information about your office closures.

treacle supports part-of-day events (as of v0.1.2), so you can add an event that would close your office early for the day, or start late.  You can also make these apply to only certain offices.

