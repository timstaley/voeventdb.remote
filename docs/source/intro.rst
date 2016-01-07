.. _intro:

Introduction
==============

voeventdb.remote is a Python library for performing remote queries against
a voeventdb_ REST interface, like the one hosted by the `4 Pi Sky`_
research group at http://voeventdb.4pisky.org.

You can use this library to easily retrieve information
about transient astronomical events, if that information was sent via the public
VOEvent_ network.

For a fuller introduction including a list of features, see the main
:ref:`voeventdb.server docs <voeventdbserver:introduction>`.
Alternatively, jump right in to the :ref:`tutorial <tutorial>` to learn by example.


.. _voeventdb: http://voeventdb.readthedocs.org/
.. _4 Pi Sky: http://4pisky.org/voevents/
.. _VOEvent: http://voevent.readthedocs.org/


Installation
=============

voeventdb.remote is available via
`PyPi <https://pypi.python.org/pypi/voeventdb.remote>`_, which means that
if you are using a virtualenv_ then you should be able to simply type::

    pip install voeventdb.remote

at the command line. Alternatively, you can
`install into your user-area <https://pip.pypa.io/en/latest/user_guide/#user-installs>`_
using::

    pip install --user voeventdb.remote

.. _virtualenv: http://virtualenv.readthedocs.org/