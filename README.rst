###########################
sphinxcontrib-programoutput
###########################

.. image:: https://secure.travis-ci.org/NextThought/sphinxcontrib-programoutput.png
   :target: http://travis-ci.org/NextThought/sphinxcontrib-programoutput

.. image:: https://coveralls.io/repos/github/NextThought/sphinxcontrib-programoutput/badge.svg
   :target: https://coveralls.io/github/NextThought/sphinxcontrib-programoutput



http://sphinxcontrib-programoutput.readthedocs.org

A Sphinx_ extension to literally insert the output of arbitrary commands into
documents, helping you to keep your command examples up to date.


Installation
------------

Install this extension from the Cheeseshop_::

   pip install sphinxcontrib-programoutput

The extension requires Sphinx 1.1 and Python 2.7 or Python 3 (Python
3.6 is tested) at least.


Usage
-----

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


Support
-------

Please report issues to the `issue tracker`_ if you have trouble or found a bug
in this extension, but respect the following guidelines:

- Check that the issue has not already been reported.
- Check that the issue is not already fixed in the ``master`` branch.
- Open issues with clear title and a detailed description in grammatically
  correct, complete sentences.


Development
-----------

The source code is hosted on Github_::

   git clone https://github.com/NextThought/sphinxcontrib-programoutput

Please fork the repository and send pull requests with your fixes or features,
but respect these guidelines:

- Read `how to properly contribute to open source projects on GitHub
  <http://gun.io/blog/how-to-github-fork-branch-and-pull-request/>`_.
- Use a topic branch to easily amend a pull request later, if necessary.
- Write `good commit messages
  <http://tbaggery.com/2008/04/19/a-note-about-git-commit-messages.html>`_.
- Squash commits on the topic branch before opening a pull request.
- Respect :pep:`8` (use `pep8`_ to check your coding style compliance)
- Add unit tests.
- Open a `pull request <https://help.github.com/articles/using-pull-requests>`_
  that relates to but one subject with a clear title and description in
  grammatically correct, complete sentences.


.. _Sphinx: http://sphinx.pocoo.org/latest
.. _Cheeseshop: http://pypi.python.org/pypi/sphinxcontrib-programoutput
.. _documentation: http://sphinxcontrib-programoutput.readthedocs.org
.. _issue tracker: https://github.com/NextThought/sphinxcontrib-programoutput/issues/
.. _Github: https://github.com/NextThought/sphinxcontrib-programoutput
.. _pep8: http://pypi.python.org/pypi/pep8/
