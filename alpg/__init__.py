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


@click.command()
@click.argument('type')
@click.argument('name')
@click.option('--author')
@click.option('--make', '-m', is_flag=True)
@click.option('--install', '-i', is_flag=True)
def cli(type, name, author, make, install):
    try:
        module = importlib.import_module('.adaptor.%s' % type, __package__)
    except ImportError as e:
        click.echo("Can't handle type %s (%s)" % (type, e))
        sys.exit(1)

    try:
        pkgbuild = module.make(name)
    except PipkgException as e:
        click.echo(e)
        sys.exit(1)

    if author is not None:
        pkgbuild.author = author

    if make or install:
        make_package(pkgbuild, install)

    else:
        click.echo(pkgbuild)
