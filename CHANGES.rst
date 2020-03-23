=========
 Changes
=========

0.16 (2020-03-23)
=================

- Add ``name`` and ``caption`` options. Added in
  `PR 41 <https://github.com/NextThought/sphinxcontrib-programoutput/pull/41>`_ 
  by Raphaël.
- Add support for Python 3.8.


0.15 (2019-09-16)
=================

- Make the test suite stop assuming the presence of a 'python'
  executable on the path. Instead it uses ``sys.executable`` (which
  shouldn't have spaces). Note that it does continue to assume the
  presence of other executables, such as 'echo'. Reported in `issue 38
  <https://github.com/NextThought/sphinxcontrib-programoutput/issues/38>`_
  by John Vandenberg.


0.14 (2019-04-08)
=================

- Add ``python_requires`` metadata to better allow tools like ``pip``
  to install a correct version.

- Add support for Sphinx 2.0 on Python 3.

- Avoid unicode errors when the program command or output produced
  non-ASCII output and the configured prompt was a byte string. This
  was most likely under Python 2, where the default configured prompt
  is a byte string. Reported by, and patch inspired by, `issue 33
  <https://github.com/NextThought/sphinxcontrib-programoutput/issues/33>`_
  by latricewilgus.

0.13 (2018-12-22)
=================

- Drop support for Sphinx < 1.7.

- Fix tests on Sphinx >= 1.8.0.

- Restore error message into the document by default from failed
  program runs on Sphinx >= 1.8.0b1.

- Fix deprecation warnings on Sphinx >= 1.8. Reported in `issue 29
  <https://github.com/NextThought/sphinxcontrib-programoutput/issues/29>`_
  by miili.


0.11 (2017-05-18)
=================

- Explicitly set ``parallel_read_safe`` to true in the extension
  metadata. See `issue 25
  <https://github.com/NextThought/sphinxcontrib-programoutput/issues/25>`_.
  With thanks to Adam J. Stewart and Stephen McDowell.

0.10 (2017-03-17)
=================

- Decode output from the program tolerantly, using the 'replace'
  handler. Based on a `pull request
  <https://github.com/habnabit/sphinxcontrib-programoutput/commit/592078e0386c2a36d50a6528b6e49d91707138bf>`_
  by Stefan C. Müller.


0.9 (2017-03-15)
================

- Forked and revived the project in `Gitub
  <https://github.com/NextThought/sphinxcontrib-programoutput>`_.

- Run the tests on Travis CI. Formatting and style is enforced by pylint.

- The oldest supported and tested Sphinx version is now 1.3.5. See
  `issue 17
  <https://github.com/NextThought/sphinxcontrib-programoutput/issues/17>`_.


- Remove support for Python 2.6, Python 3.2 and 3.3.

- 100% test coverage.

- Remove support for ``programoutput_use_ansi``. The
  ``sphinxcontrib.ansi`` extension is no longer available on PyPI.

0.8 (Oct 12, 2012)
==================

- Migrated to GitHub


0.7 (Apr 17, 2012)
==================

- Added ``cwd`` option to ``..program-output``
- Working directory of executed programs defaults to documentation root now


0.6 (Jan 07, 2012)
==================

- Python 3 support
- Require Sphinx 1.1 now


0.5 (Sep 19, 2011)
==================

- ``programoutput_prompt_template`` is interpreted as format string now!
- Require Python 2.6 now
- Added ``returncode`` option to ``program-output`` (thanks to
  Jan-Marek Glogowski)
- Support ``returncode`` formatting key in
  ``programoutput_prompt_template``
- Warn on unexpected return codes instead of raising
  ``subprocess.CalledProcessError``
- Turn fatal errors during command into document error messages
  instead of crashing the build


0.4.1 (Mar 11, 2011)
====================

- Some source code cleanups
- Fixed installation instructions in documentation


0.4 (May 21, 2010)
==================

- Initial release
