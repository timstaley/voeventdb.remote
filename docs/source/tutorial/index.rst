.. _tutorial:

Tutorial
=========

The tutorials take the form of Jupyter_ notebooks; you can either read them
online or download them to work with interactively. The notebook files can
be found in the `notebooks folder`_ of the source repository, or downloaded
using the links on each tutorial page.


.. _Jupyter: http://jupyter.org/
.. _notebooks folder: https://github.com/timstaley/voeventdb.remote/tree/master/docs/source/notebooks

.. toctree::
   :maxdepth: 2

   quickstart
   tutorial1
   tutorial2
   tutorial3
   tutorial4
   tutorial5
   demo


.. note:: Optional dependencies:

   For trying out the basic functionality in the tutorials, all you need to
   install is the `voeventdb.remote` library itself (and optionally,
   the Jupyter_ notebook dependency, if you are running the code from the notebooks
   rather than pasting it in at the command line).
   However, there are a few sections where
   we make use of other libraries for generating plots, etc. If you want to
   run those cells, you can ensure you have all the required libraries by
   installing the list found in
   :download:`docs/requirements.txt <../../requirements.txt>`, i.e.

   .. literalinclude:: ../../requirements.txt

