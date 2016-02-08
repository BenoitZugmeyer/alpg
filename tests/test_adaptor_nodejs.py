
import alpg.adaptor.nodejs as nodejs


def infos(**kwargs):
    infos = {
        'name': 'foo',
        'description': 'foo',
        'homepage': 'http://example.org',
        'version': '1.0.0',
        'dist': {'tarball': 'http://example.org/foo.tgz', 'shasum': '123'},
        'license': 'MIT',
    }
    infos.update(kwargs)
    return infos


def test_license():
    pkg = nodejs.makepkgbuild_from_infos(infos())
    assert pkg.license == ('MIT',)


def test_licenses():
    pkg = nodejs.makepkgbuild_from_infos(
        infos(license=None,
              licenses={'type': 'MIT'}))
    assert pkg.license == ('MIT',)
