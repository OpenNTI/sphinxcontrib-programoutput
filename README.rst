=============================
 sphinxcontrib-programoutput
=============================

.. image:: https://secure.travis-ci.org/NextThought/sphinxcontrib-programoutput.png
   :target: http://travis-ci.org/NextThought/sphinxcontrib-programoutput

.. image:: https://coveralls.io/repos/github/NextThought/sphinxcontrib-programoutput/badge.svg
   :target: https://coveralls.io/github/NextThought/sphinxcontrib-programoutput


https://sphinxcontrib-programoutput.readthedocs.org

A Sphinx_ extension to literally insert the output of arbitrary commands into
documents, helping you to keep your command examples up to date.


Installation
============

Install this extension from PyPI_::

   pip install sphinxcontrib-programoutput

The extension requires Sphinx 1.7.0 and Python 2.7 or Python 3 (Python
3.5+ is tested) at least.

Usage
=====

Just add this extension to ``extensions``::

   extensions = ['sphinxcontrib.programoutput']

Now you've two new directives ``program-output`` and ``command-output`` to
insert the output of programs.  The former just inserts the output::

   .. program-output:: python -V

Output::

   Python 2.7.1

The latter directive mimics a shell session, and is intended to show examples::

   .. command-output:: python -V

Output::

   $ python -V
   Python 2.7.1


Please refer to the documentation_ for comprehensive information about usage and
configuration of this extension.


Development and Support
=======================

Please refer to the documentation_ for information on support and the
development process.


.. _Sphinx: http://www.sphinx-doc.org/en/stable/
.. _PyPI: http://pypi.python.org/pypi/sphinxcontrib-programoutput
.. _documentation: http://sphinxcontrib-programoutput.readthedocs.org
