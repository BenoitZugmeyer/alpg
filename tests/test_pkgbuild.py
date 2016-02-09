import textwrap
from alpg.pkgbuild import Pkgbuild


def test_name():
    pkg = Pkgbuild(pkgname='12')
    assert pkg.pkgname == '12'


def test_arch():
    pkg = Pkgbuild()

    assert pkg.arch == ('any',)
    pkg.arch = 'foo'
    assert pkg.arch == ('foo',)


def test_maintainer():
    pkg = Pkgbuild(pkgname="a",
                   pkgver="1",
                   maintainer="John Doe <john@doe.org>")

    assert pkg.maintainer == "John Doe <john@doe.org>"

    assert str(pkg) == textwrap.dedent("""\
        # Maintainer: John Doe <john@doe.org>
        pkgname=a
        pkgver=1
        pkgrel=1
        arch=(any)
        """)


def test_contributors():
    pkg = Pkgbuild(pkgname="a",
                   pkgver="1",
                   contributor=("John Doe <john@doe.org>",
                                "Mary Doe <mary@doe.org>"))

    assert pkg.contributor == ("John Doe <john@doe.org>",
                               "Mary Doe <mary@doe.org>")

    assert str(pkg) == textwrap.dedent("""\
        # Contributor: John Doe <john@doe.org>
        # Contributor: Mary Doe <mary@doe.org>
        pkgname=a
        pkgver=1
        pkgrel=1
        arch=(any)
        """)
