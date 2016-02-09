
from alpg.pkgbuild import Pkgbuild


def test_name():
    pkg = Pkgbuild(pkgname='12')
    assert pkg.pkgname == '12'


def test_arch():
    pkg = Pkgbuild()

    assert pkg.arch == ('any',)
    pkg.arch = 'foo'
    assert pkg.arch == ('foo',)
