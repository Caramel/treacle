******************
Installing treacle
******************

treacle requires either Python 2.6 or 2.7.  Python 3 isn't presently supported.

Installing stable version with ``pip``
=======================

.. highlight:: console

If you don't already have pip installed, you'll need to install it with ``easy_install`` first::

	# easy_install pip

Then you can install the current stable version of treacle::

	# pip install treacle

Then you're done, and treacle will be available in your PATH.


Installing development version from ``git``
===========================================

You can install the current development version of the code from the ``git`` repository::

	# git clone -b develop https://github.com/Caramel/treacle.git
	# cd treacle
	# pip install -r requirements.txt
	# python setup.py install

