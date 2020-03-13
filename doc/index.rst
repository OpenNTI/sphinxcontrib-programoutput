.. default-domain:: rst
.. highlight:: rest

===============================================================
 :py:mod:`sphinxcontrib.programoutput` – Insert command output
===============================================================

.. py:module:: sphinxcontrib.programoutput
   :synopsis:  Include the output of programs into documents

Sphinx_ extension to insert the output of arbitrary commands into documents.

The extension is available under the terms of the :ref:`BSD license <license>`.


Installation
============

Use ``pip`` to install this extension from PyPI_::

   pip install sphinxcontrib-programoutput

The extension requires Sphinx 1.3 and Python 2.7 or Python 3 at least.

You can now add this extension to ``extensions``::

   extensions = ['sphinxcontrib.programoutput']

Now you've two new directives ``program-output`` and ``command-output`` to
insert the output of programs.

Usage
=====

To include the output of a command into your document, use the
:dir:`program-output` directive provided by this extension::

   .. program-output:: python -V

The whole output of ``python -V``, including any messages on standard error, is
inserted into the current document, formatted as literal text without any
syntax highlighting:

.. program-output:: python -V

You can omit the content of the standard error stream with the ``nostderr``
option.

By default, commands are executed in the top-level source directory.  You can
choose an alternate working directory with the ``cwd`` option.  The argument of
this option is either a path relative to the current source file, or a absolute
path which means that it is relative to the top level source directory.


Shortening the output
---------------------

Lengthy output can be shortened with the ``ellipsis`` option.  Its value
denotes lines to omit when inserting the output of the command.  Instead, a
single ellipsis ``...`` is inserted.

If used with a single number, all lines after the specified line are omitted::

   .. program-output:: python --help
      :ellipsis: 2

The above omits all lines after the second one:

.. program-output:: python --help
   :ellipsis: 2

Negative numbers count from the last line backwards, thus replacing ``2`` with
``-2`` in the above example would only omit the last two lines.

If used with two comma-separated line numbers, all lines in between the
specified lines are omitted.  Again, a negative number counts from the last
line backwards::

   .. program-output:: python --help
      :ellipsis: 2,-2

The above omits all lines except the first two and the last two lines:

.. program-output:: python --help
   :ellipsis: 2,-2


Mimicing shell input
--------------------

You can mimic shell input with the :dir:`command-output` directive [#alias]_.
This directive inserts the command along with its output into the document::

   .. command-output:: python -V

.. command-output:: python -V

The appearance of this output can be configured with
:confval:`programoutput_prompt_template`.  When used in conjunction with
``ellipsis``, the command itself and any additional text is *never* omitted.
``ellipsis`` always refers to the *immediate output* of the command::

   .. command-output:: python --help
      :ellipsis: 2

.. command-output:: python --help
   :ellipsis: 2


Command execution and shell expansion
-------------------------------------

Normally the command is splitted according to the POSIX shell syntax (see
:py:mod:`shlex`), and executed directly.  Thus special shell features like
expansion of environment variables will not work::

   .. command-output:: echo "$USER"

.. command-output:: echo "$USER"

To enable these features, enable the ``shell`` option.  With this option, the
command is literally passed to the system shell::

   .. command-output:: echo "$USER"
      :shell:

.. command-output:: echo "$USER"
   :shell:

Other shell features like process expansion consequently work, too::

   .. command-output:: ls -l $(which grep)
      :shell:

.. command-output:: ls -l $(which grep)
   :shell:

Remember to use ``shell`` carefully to avoid unintented interpretation of shell
syntax and swallowing of fatal errors!


Error handling
--------------

If an unexpected exit code (also known as *return code*) is returned by a
command, it is considered to have failed.  In this case, a build warning is
emitted to help you to detect misspelled commands or similar errors.  By
default, a command is expected to exit with an exit code of 0, all other codes
indicate an error.  In some cases however, it may be reasonable to demonstrate
failed programs.  To avoid a (superfluous) warning in such a case, you can
specify the expected return code of a command with the ``returncode`` option::

   .. command-output:: python -c 'import sys; sys.exit(1)'
      :returncode: 1

The above command returns the exit code 1 (as given to :py:func:`sys.exit()`),
but no warning will be emitted.  On the contrary, a warning will be emitted,
should the command return 0!

.. note::

   Upon fatal errors which even prevent the execution of the command neither
   return code nor command output are available.  In this case an error message
   is inserted into the document instead.

   If ``shell`` is set however, most of these fatal errors are handled by the
   system shell and turned into return codes instead.  In this case the error
   message will only appear in the output of the shell.  If you're using
   ``shell``, double-check the output for errors.  Best avoid ``shell``, if
   possible.


Reference
=========

.. directive:: .. program-output:: command

   Include the output of ``command`` in the documentation.

   The output is formatted as literal text, without any syntax highlighting.

   By default, the command is split according to the POSIX shell syntax (using
   :py:func:`shlex.split()`), and executed directly.  Both standard output and
   standard error are captured from the invocation of ``command`` and included
   in the document.  However, if the option ``shell`` is given, ``command`` is
   literally passed to the system shell.  With the ``nostderr`` option,
   standard error is hidden from the output.

   The working directory of the command can be configured with the ``cwd``
   option.  The argument of this option is a directory path, relative to the
   current source file.  Absolute paths are interpreted as relative to the
   root of the source directory.  The default working directory is ``/``, i.e.
   the root of the source directory.

   If the ``prompt`` option is given, the ``command`` itself is included in the
   document, so that the output mimics input in a shell prompt.
   :confval:`programoutput_prompt_template` controls the appearance of this.
   The value of the ``extraargs`` option is appended at the end of ``command``
   (separated by a whitespace) before executing the command, but not included
   in the output of the ``prompt`` option.  Use this to pass extra arguments
   which should not appear in the document.

   The output can be shortened with the ``ellipsis`` option.  The value of this
   option is of the form ``start[,end]`` with ``start`` and ``end`` being
   integers which refer to lines in the output of ``command``.  ``end`` is
   optional and defaults to the last line.  Negative line numbers count
   backwards from the last line.  Everything in the interval ``[start, end[``
   is replaced with a single ellipsis ``...``.  The ``ellipsis`` option only
   affects the immediate output of ``command``, but never any additional text
   inserted by option ``prompt``.

   If the command does return an exit code different from the expected one, a
   build warning is issued.  The expected return code defaults to 0, and can be
   changed with the ``returncode`` option.

   A ``caption`` option can be given to show the given name, or by default the
   given command, before the output block.
   A ``name`` option with a target name can be provided to reference the
   command block by using ``ref``.


.. directive:: command-output

   Same as :dir:`program-output`, but with enabled ``prompt`` option.


Configuration
-------------

This extension understands the following configuration options:

.. confval:: programoutput_prompt_template

   A `format string`_ template for the output of the ``prompt`` option to
   :dir:`command-output`.  Defaults to ``$ {command}\n{output}`` which renders
   as follows:

   .. command-output:: python -V

   The following keys are provided to the format string:

   * ``command`` is replaced with the literal command as given to the
     directive, *without* any ``extraargs``.
   * ``output`` is the output of the command, after the ``ellipsis`` option has
     been applied.
   * ``returncode`` is the return code of the command as integer.

Support
=======

Please report issues to the `issue tracker`_ if you have trouble or found a bug
in this extension, but respect the following guidelines:

- Check that the issue has not already been reported.
- Check that the issue is not already fixed in the ``master`` branch.
- Open issues with clear title and a detailed description in grammatically
  correct, complete sentences.


Development
===========

The source code is hosted on Github_::

   git clone https://github.com/NextThought/sphinxcontrib-programoutput

Please fork the repository and send pull requests with your fixes or features,
but respect these guidelines:

- Read `how to properly contribute to open source projects on GitHub
  <https://gun.io/blog/how-to-github-fork-branch-and-pull-request/>`_.
- Use a topic branch to easily amend a pull request later, if necessary.
- Write `good commit messages
  <http://tbaggery.com/2008/04/19/a-note-about-git-commit-messages.html>`_.
- Squash commits on the topic branch before opening a pull request.
- Respect :pep:`8` (use `pep8`_ to check your coding style compliance)
- Add unit tests.
- Open a `new pull request <https://help.github.com/articles/using-pull-requests>`_
  that relates to but one subject with a clear title and description in
  grammatically correct, complete sentences.


Changelog
=========

.. include:: ../CHANGES.rst


.. _license:

License
=======

.. literalinclude:: ../LICENSE


.. rubric:: Footnotes

.. [#alias] This directive is just an alias for the :dir:`program-output`
            directive with the ``prompt`` option set.


.. _Sphinx: http://www.sphinx-doc.org/en/stable/
.. _PyPI: https://pypi.python.org/pypi/sphinxcontrib-programoutput
.. _github: https://github.com/NextThought/sphinxcontrib-programoutput
.. _readme: https://github.com/NextThought/sphinxcontrib-programoutput/blob/master/README.rst
.. _format string: https://docs.python.org/2/library/string.html#formatstrings
.. _issue tracker: https://github.com/NextThought/sphinxcontrib-programoutput/issues
.. _pep8: https://pypi.python.org/pypi/pep8/
