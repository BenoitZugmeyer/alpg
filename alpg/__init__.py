import importlib
import sys

import click

from alpg.exception import PipkgException


def make_package(pkgbuild, install):
    import tempfile
    import os
    import subprocess

    cwd = os.getcwd()

    with tempfile.TemporaryDirectory() as tmp_path:
        os.chdir(tmp_path)

        with open('PKGBUILD', 'w') as fp:
            fp.write(str(pkgbuild))

        env = dict(os.environ)
        env['PKGDEST'] = cwd
        args = ('makepkg', '-f')

        if install:
            args += ('-i',)

        subprocess.check_call(args, env=env)


@click.command(
    help="""
        Generate PKGBUILDs from various package managers.  <pkgtype> should be
        a valid package type (see below), and <pkgname> the name of the package
        to generate the PKGBUILD for.

        \b
        Supported package types:
            nodejs (through npm)
            python2 (through pip2)
    """)
@click.argument('pkgtype', metavar='<pkgtype>')
@click.argument('pkgname', metavar='<pkgname>')
@click.option('--maintainer',
              help="Prepend the maintainer as a comment to the PKGBUILD.")
@click.option('--contributor',
              multiple=True,
              help="Prepend the contributor as a comment to the PKGBUILD. May "
              "be used multiple times.")
@click.option('--make', '-m',
              is_flag=True,
              help="Instead of printing the PKGBUILD, build it with makepkg")
@click.option('--install', '-i',
              is_flag=True,
              help="Instead of printing the PKGBUILD, build and install it "
              "with makepkg")
def cli(pkgtype, pkgname, maintainer, contributor, make, install):
    try:
        module = importlib.import_module('.adaptor.%s' % pkgtype, __package__)
    except ImportError as e:
        click.echo("Can't handle type %s (%s)" % (pkgtype, e))
        sys.exit(1)

    try:
        pkgbuild = module.make(pkgname)
    except PipkgException as e:
        click.echo(e)
        sys.exit(1)

    if maintainer:
        pkgbuild.maintainer = maintainer

    if contributor:
        pkgbuild.contributor = contributor

    if make or install:
        make_package(pkgbuild, install)

    else:
        click.echo(pkgbuild)
