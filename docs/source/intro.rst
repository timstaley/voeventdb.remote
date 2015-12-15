.. _intro:

Introduction
==============

voeventdb.remote is a Python library for performing remote queries against
a voeventdb_ REST interface, like the one hosted by the `4 Pi Sky`_
research group at http://voeventdb.4pisky.org.

You can use this library to easily retrieve information
about transient astronomical events, if that information was sent via the public
VOEvent_ network.

For a fuller introduction, see the main
:ref:`voeventdb introduction <voeventdb:introduction>`.
Alternatively, jump right in to the :ref:`tutorial <tutorial>` to learn by example.


.. _voeventdb: http://voeventdb.readthedocs.org/
.. _4 Pi Sky: http://4pisky.org/voevents/
.. _VOEvent: http://voevent.readthedocs.org/


Installation
=============

voeventdb.remote is available via
`PyPi <https://pypi.python.org/pypi/voeventdb.remote>`_, which means that
if you are using a virtualenv_ then you should be able to simply type::

    pip install --pre voeventdb.remote

at the command line. Alternatively, you can
`install into your user-area <https://pip.pypa.io/en/latest/user_guide/#user-installs>`_
using::

    pip install --user --pre voeventdb.remote

.. note::

    The ``--pre`` flag is temporary - it only applies while using the
    'pre-release' version.

.. _virtualenv: http://virtualenv.readthedocs.org/