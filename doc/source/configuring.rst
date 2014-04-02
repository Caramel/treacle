*******************
Configuring treacle
*******************

Treacle, by default, looks for it's configuration file in :file:`/etc/treacle/treacle.ini`.

You can override this with the ``-c`` option to treacle, which is covered in a later section.  For the purposes of this document, I'll assume you're working with treacle's configuration at that location.

This file uses the same format as Python's :class:`~configparser.ConfigParser` module, which is similar to Windows INI format.

The first thing that treacle reads when determining holidays is the ``[DEFAULT]`` section.  Options in there are then overridden by the other sections which represent offices (in the example below, ``adel``, ``melb`` and ``nuri``).

Example configuration
=====================

.. highlight:: ini

::

	[DEFAULT]
	holidays = /etc/treacle/holidays/au_holidays.ics

	[adel]
	holidays_sa = /etc/treacle/holidays/sa_holidays.ics

	tz = Australia/Adelaide
	hours1 = Mon,Tue,Wed,Thu,Fri@08:30-18:00

	[melb]
	holidays_vic = /etc/treacle/holidays/vic_holidays.ics

	tz = Australia/Melbourne
	hours1 = Mon,Tue,Wed,Thu,Fri@08:00-16:00

	[nuri]
	holidays_sa = /etc/treacle/holidays/sa_holidays.ics
	holidays_nuri = /etc/treacle/holiday/nuri_holidays.ics

	tz = Australia/Adelaide
	hours1 = Mon,Tue,Wed,Thu,Fri@07:00-19:00
	hours2 = Sat@12:00-15:00

The ``adel`` office will use the holidays files ``au_holidays.ics`` and ``sa_holidays.ics``, uses the ``Australia/Adelaide`` time zone, and is open from Monday to Friday, 08:30 to 18:00 local time.

The ``melb`` office will use the holidays files ``au_holidays.ics`` and ``vic_holidays.ics``, uses the ``Australia/Melbourne`` time zone, and is open from Monday to Friday, 08:00 to 16:00 local time.

The ``nuri`` office will use the holidays files ``au_holidays.ics``, ``sa_holidays.ics`` and ``nuri_holidays.ics``.  It uses the ``Australia/Adelaide`` time zone, and is open from Monday to Friday, 07:00 to 19:00 and on Saturdays from 12:00 to 15:00.

Options reference
=================

The options available are as follows:

``tz``
	An Olson (UNIX) time zone name representing the time zone at the location.  If this is not specified, :abbr:`UTC (Coordinated Universal Time)` is assumed.

	For example, ``Australia/Adelaide`` or ``Australia/Melbourne``.

	.. versionchanged:: 0.1.2

		As of v0.1.2, a default time zone of :abbr:`UTC (Coordinated Universal Time)` is assumed if no default or office timezone is specified.  In previous versions of treacle, this was an invalid configuration and would cause an error.


``holidays*``
	A path to an iCalendar file where public holidays that apply to this office is located.

	This should be specified as an absolute path, as relative paths are treated relative to the working directory that treacle is run from, which can lead to unpredictable results.

	Option names starting with ``holidays`` are allowed, which will allow you to specify multiple holiday files for a single location.  In the example above, this is indicated with multiple option names (``holidays``, ``holidays_sa``, ``holidays_vic``).

``hours*``
	The opening hours for the office, specified in the time zone of the office.

	It is specified in the following format::

		Mon,Tue,Wed,Thu,Fri@09:00-17:00

	Where:

	* The days that these hours apply to and the hours are separated by an ``@`` symbol.
	* The days of the week are specified in your locale in either long (``Monday``) or short (``Mon``) form, with multiple days separated by commas ``,``.
	* Opening hours are specified in 24-hour format, with the start and end time separated by a dash ``-``.

	Multiple sets of hours may be specified by providing multiple options that start with the string ``hours``.  For example, ``hours1``, ``hours2``, etc.

	Localised day names are generated using the ``%a`` and ``%A`` :ref:`strftime formatting codes <strftime-strptime-behavior>`.  If localised day names are not desired, set the environment variables ``LANG=C LC_TIME=C`` when running treacle.


