***********************************
Using treacle in Asterisk dialplans
***********************************

Treacle can be used inside of Asterisk dialplans as an :abbr:`AGI (Asterisk Gateway Interface)` script, with the option ``-a``.

.. highlight:: ini

For example::

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

The dialplan variable ``CARHOURS`` will be set by the :abbr:`AGI (Asterisk Gateway Interface)` script on completion.  This will be set to ``0`` if it is not business hours for the location, and ``1`` if it is business hours for the location.

In this example, it will send the caller into the queue ``myqueue`` if it is currently business hours, and if they have been in the queue for more than 30 seconds or it is not business hours, direct them to the voicemail box ``100`` with the ``unavailable`` state.

You can also check if any office is in business hours::

	[my_dialplan]
	exten => s,1,AGI(/usr/local/bin/treacle,-a,-A)

And set a different dialplan variable::

	[my_dialplan]
	exten => s,1,AGI(/usr/local/bin/treacle,-a,MYVAR,-o,melb)
	exten => s,n,NoOp(Business Hours = ${MYVAR})

Or use a different configuration file::

	[my_dialplan]
	exten => s,1,AGI(/usr/local/bin/treacle,-c,/etc/treacle/examplecorp.ini,-o,gamb)

.. note::

	On some systems (such as Red Hat and CentOS), ``distutils`` installs treacle to ``/usr/bin``, not ``/usr/local/bin``. Adjust this accordingly for your system.

