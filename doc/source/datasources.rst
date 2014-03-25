************
Data sources
************

Data sources are given as iCalendar files.  You can create these yourself, or download them from various sources online.

Recurring events are not supported by this software.

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

