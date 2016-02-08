import unittest

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


class TestAdaptorNodejs(unittest.TestCase):

    def test_license(self):
        pkg = nodejs.makepkgbuild_from_infos(infos())
        self.assertEqual(pkg.license, ('MIT',))

    def test_licenses(self):
        pkg = nodejs.makepkgbuild_from_infos(
            infos(license=None,
                  licenses={'type': 'MIT'}))
        self.assertEqual(pkg.license, ('MIT',))
