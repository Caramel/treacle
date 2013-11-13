# treacle #

treacle is an AGI (Asterisk Gateway Interface) script which handles public holidays and opening hours in different offices with different timezones and different public holidays.

This allows conditional call routing in Asterisk, and also allows one system to route calls for different time zones and different offices.

This means if you have callers in Adelaide and callers in Melbourne, you can give each a different number, and their calls will be routed to voicemail after hours in their timezone, and not available on public holidays in their timezone.

## installation ##

This requires Python 2.6 or Python 2.7.

```sh
easy_install pip
pip install --upgrade -r requirements.txt
python setup.py install
```

If `pip` has problems installing `pytz`, run this first to upgrade distutils, then install `treacle`:

```sh
pip install 'distribute>=0.6.35'
```

## configuration ##

By default, treacle will look for it's configuration file in `/etc/treacle/treacle.ini`.

There is an example configuration included in this distribution (`treacle_example.ini`).  Please note that this configuration will be missing iCalendar feeds that it uses, so you will probably want to scrape Apple's feed (instructions below) in order to use it.

The configuration is in Python's ConfigParser INI format (similar to Windows INI files).

There is a `[DEFAULT]` section which applies to all offices in sections below.  The section names are offices, so `[adel]` contains rules for the office `adel`, for example.

### specifying multiple values and overrides ###

You can specify multiple values for some options.  This is done by specifying the option name followed by some other characters to make it unique.

The same option name cannot appear multiple times in the same section, but options in the `[DEFAULT]` section may be overridden by options in later sections by using an identical option name.

For example:

```ini
[DEFAULT]
holidays = au_holidays.ics

[adel]

[melb]
holidays2 = vic_holidays.ics

[auck]
holidays = nz_holidays.ics
```
	
In this example:

* `adel` office will only have the holidays in `au_holidays.ics`.
* `melb` office will have the holidays in `au_holidays.ics` and `vic_holidays.ics`.
* `auck` office will only have the holidays in `nz_holidays.ics`.

### section directives ###

Each section takes the following directives:

#### `tz` ####

An Olson-style (UNIX) timezone identifier for the office.  This needs to be defined for each office, or at least in the `[DEFAULT]` section.

For example, `Australia/Adelaide` or `America/Chicago`.

#### `holidays` ####

A reference to an iCalendar file where public holidays that apply to this office is located.

This may be specified as a relative path, however it is not recommended (and you should use an absolute path instead).

#### `hours` ####

The opening hours for the office.  It is specified in the following format:

```
Mon,Tue,Wed,Thu,Fri@09:00-17:00
```

Where:

* days of the week in your locale are specified in either long (`Monday`) or short (`Mon`) form, seperated by commas.
* open hours are specified in 24-hour format seperated by a `-`.
* there is an `@` seperator between the two parts.

Hours are always specified in the timezone of the office.

## using in dialplans ##

This program can be used in Asterisk dialplans as an AGI script, with the option `-a`:

```ini
[my_dialplan]
exten => s,1,AGI(/usr/local/bin/treacle,-a,-o,adel)

; Print returned output from treacle and make decision
exten => s,n,NoOp(Business Hours = ${CARHOURS})
exten => s,n,GotoIf(${CARHOURS}?open:closed)

; Business hours
exten => s,n(open),Queue(myqueue,t,,,30)

; Fall through if queue fails

; Not available, and failure mode for queue
exten => s,n(closed),Voicemail(100,u)

; Hangup when done.
exten => s,n,Hangup
```

This will set the dialplan variable `CARHOURS` on completion.  This will be set to `0` if it is not business hours, or `1` if it is business hours for the location.

In this example, it will send the caller into the queue `myqueue` if it is currently business hours, and if they have been in the queue for more than 30 seconds or it is not business hours, direct them to the voicemail box `100` with the `unavailable` state.

You can also check if any office is in business hours:

```ini
[my_dialplan]
exten => s,1,AGI(/usr/local/bin/treacle,-a,-A)
```

And set a different dialplan variable:

```ini
[my_dialplan]
exten => s,1,AGI(/usr/local/bin/treacle,-a,MYVAR,-o,melb)
```

**Note:** On some systems (such as Red Hat), `distutils` installs treacle to `/usr/bin`, not `/usr/local/bin`.  Adjust this accordingly for your system.


## using standalone ##

This can also be used outside of Asterisk, with the option `-s`:

```sh
treacle -s -o adel && echo "Adelaide Office Open"
treacle -s -o melb || echo "Melbourne Office Closed"
```

This will print `Adelaide Office Open` if the Adelaide office is currently open, and `Melbourne Office Closed` if the Melbourne office is closed.

Like in AGI, you can use this to find if any office is open:

```sh
treacle -s -A && echo "There is an office open"
```

This will print `There is an office open` if any office is currently open.

## scraping apple for public holidays ##

For Australian users, a tool is included to scrape the Apple iCal public holiday feeds.  In order to use this after you have installed the software:

```sh
treacle_scrape
```
	
This will produce the following files in the current directory:

* `au_holidays.ics` - Contains holidays specific to no state.
* `act_holidays.ics` - Contains holidays specific to ACT
* ...and so on for `nsw`, `nt`, `qld`, `sa`, `tas`, `vic` and `wa`.

This script will blindly overwrite these files in the directory, so be careful!

## licensing ##

Copyright 2013 [Caramel](http://www.caramel.com.au).

This program is free software: you can redistribute it and/or modify it under the terms of the GNU Lesser General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License along with this program.  If not, see <http://www.gnu.org/licenses/>.
