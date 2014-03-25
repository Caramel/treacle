*******************************************
Using treacle in shell scripts (standalone)
*******************************************

.. highlight:: shell

Treacle be used outside of Asterisk, with the option ``-s``::

	treacle -s -o adel && echo "Adelaide Office Open"
	treacle -s -o melb || echo "Melbourne Office Closed"

This will print ``Adelaide Office Open`` if the Adelaide office is
currently open, and ``Melbourne Office Closed`` if the Melbourne office
is closed.

The exit code ``0`` will be given if the office is open, and the exit code
``1`` will be given if the office is closed.

Like in AGI, you can use this to find if any office is open::

	treacle -s -A && echo "There is an office open"

This will print ``There is an office open`` if any office is currently
open.

