=============================
 sphinxcontrib-programoutput
=============================


https://sphinxcontrib-programoutput.readthedocs.org

A Sphinx_ extension to literally insert the output of arbitrary commands into
documents, helping you to keep your command examples up to date.


Installation
============

Install this extension from PyPI_::

   pip install sphinxcontrib-programoutput

The extension requires Sphinx 5.0 and Python 3.8+.

Usage
=====

Just add this extension to ``extensions``::

   extensions = ['sphinxcontrib.programoutput']

Now you've two new directives ``program-output`` and ``command-output`` to
insert the output of programs.  The former just inserts the output::

   .. program-output:: python -V

Output::

   Python 3.14.2

The latter directive mimics a shell session, and is intended to show examples::

   .. command-output:: python -V

Output::

   $ python -V
   Python 3.14.2


Please refer to the documentation_ for comprehensive information about usage and
configuration of this extension.


Development and Support
=======================

Please refer to the documentation_ for information on support and the
development process.


.. _Sphinx: http://www.sphinx-doc.org/en/stable/
.. _PyPI: http://pypi.org/project/sphinxcontrib-programoutput
.. _documentation: http://sphinxcontrib-programoutput.readthedocs.org
