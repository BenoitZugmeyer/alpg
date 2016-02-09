import json
import shlex

from alpg.pkgbuild import Pkgbuild
from alpg.process import run


def make(package):
    return makepkgbuild_from_infos(
        json.loads(run('/bin/npm', 'view', '--json', package)))


def makepkgbuild_from_infos(infos):
    assert 'name' in infos
    assert 'version' in infos
    assert 'description' in infos
    assert 'dist' in infos

    if infos.get('license'):
        license = (infos['license'],)

    elif 'licenses' in infos and isinstance(infos['licenses'], dict):
        license = (infos['licenses']['type'],)

    else:
        license = None

    source_url = infos['dist']['tarball']
    source_basename = source_url.rpartition("/")[2]

    return Pkgbuild(
        pkgname='nodejs-%s' % infos['name'],
        pkgver=infos['version'],
        pkgdesc=infos['description'],
        url=infos.get('homepage'),
        license=license,
        depends=('nodejs',),
        source=(source_url,),
        sha1sums=(infos['dist']['shasum'],),
        noextract=(source_basename,),
        package=r'''
        cd "$srcdir"

        npm install --user root -g --prefix "$pkgdir/usr" "$srcdir"/{}
        '''.format(shlex.quote(source_basename)))
