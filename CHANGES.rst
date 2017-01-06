0.8 (Oct 12, 2012)
==================

- Migrated to GitHub


0.7 (Apr 17, 2012)
==================

- Added ``cwd`` option to :rst:dir:`program-output`
- Working directory of executed programs defaults to documentation root now


0.6 (Jan 07, 2012)
==================

- Python 3 support
- Require Sphinx 1.1 now


0.5 (Sep 19, 2011)
==================

- :confval:`programoutput_prompt_template` is interpreted as format string now!
- Require Python 2.6 now
- Added ``returncode`` option to :rst:dir:`program-output` (thanks to Jan-Marek
  Glogowski)
- Support ``returncode`` formatting key in
  :confval:`programoutput_prompt_template`
- Warn on unexpected return codes instead of raising
  :py:exc:`~subprocess.CalledProcessError`
- Turn fatal errors during command into document error messages instead of
  crashing the build


0.4.1 (Mar 11, 2011)
====================

- Some source code cleanups
- Fixed installation instructions in documentation


0.4 (May 21, 2010)
==================

- Initial release
