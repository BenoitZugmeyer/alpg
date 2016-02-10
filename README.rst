===========================
ArchLinux Package Generator
===========================

Generate PKGBUILDs from various package managers.


Install
=======

::

    bash <( curl https://raw.githubusercontent.com/BenoitZugmeyer/alpg/master/install.sh )

Don't worry, it will be installed through pacman.  Check
`install.sh <install.sh>`_ if you are unsure.


Usage
=====

::

    Usage: alpg [OPTIONS] <pkgtype> <pkgname>

      Generate PKGBUILDs from various package managers.  <pkgtype> should be a
      valid package type (see below), and <pkgname> the name of the package to
      generate the PKGBUILD for.

      Supported package types:
          nodejs (through npm)
          python2 (through pip2)

    Options:
      --maintainer TEXT   Prepend the maintainer as a comment to the PKGBUILD.
      --contributor TEXT  Prepend the contributor as a comment to the PKGBUILD.
                          May be used multiple times.
      -m, --make          Instead of printing the PKGBUILD, build it with makepkg
      -i, --install       Instead of printing the PKGBUILD, build and install it
                          with makepkg.
      --help              Show this message and exit.


Example
=======

::

    $ alpg -i nodejs eslint


Note
====

Everything is still experimental.  Use this at your own risk.


TODO / goals
============

* Continue implementing Python 2 and Node.js adaptors
* Support additional files next to the PKGBUILD (patches, licenses, ...)
* Add adaptors for:

  * Python 3 (through pip)
  * AUR
  * Rust (through cargo)
  * Ruby (through gem)

* Package search
