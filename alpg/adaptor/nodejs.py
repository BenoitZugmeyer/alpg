import json

from alpg.pkgbuild import Pkgbuild
from alpg.process import run


def make(package):
    return makepkgbuild_from_infos(
        json.loads(run('/bin/npm', 'view', '--json', package)))


def makepkgbuild_from_infos(infos):
    assert 'name' in infos
    assert 'version' in infos
    assert 'description' in infos
    assert 'homepage' in infos
    assert 'dist' in infos

    if infos.get('license'):
        license = (infos['license'],)

    elif 'licenses' in infos and isinstance(infos['licenses'], dict):
        license = (infos['licenses']['type'],)

    else:
        license = None

    return Pkgbuild(
        pkgname='nodejs-%s' % infos['name'],
        pkgver=infos['version'],
        pkgdesc=infos['description'],
        url=infos['homepage'],
        license=license,
        depends=('nodejs',),
        source=(infos['dist']['tarball'],),
        sha1sums=(infos['dist']['shasum'],),
        package=r'''
        cd "$srcdir"

        npm install --user root -g --prefix "$pkgdir/usr" ./package
        ''')
