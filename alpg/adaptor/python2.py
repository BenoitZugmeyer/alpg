from xmlrpc.client import ServerProxy
import re

from alpg.pkgbuild import Pkgbuild
from alpg.exception import PipkgException

client = ServerProxy('http://pypi.python.org/pypi')

SOURCEFILE_TYPE_RE = re.compile(".*\.(tar|zip|gz|z|bz2?|xz|whl)",
                                re.IGNORECASE)


def is_sourcefile(url):
    return bool(url and SOURCEFILE_TYPE_RE.match(url))


def get_source(data):
    raw_urls = client.release_urls(data['name'], data['version'])
    if raw_urls:
        for url in raw_urls:
            if url['packagetype'] in ('sdist', 'bdist_wheel') and \
                    'py2' in url['python_version']:
                return url

    if data.get('download_url'):
        return {
            'url': data['download_url'],
            'packagetype': 'sdist'
        }

    raise PipkgException("Couldn't find any suitable source")


def get_license(data):
    license = data.get('license', 'UNKNOWN')
    return 'CUSTOM' if len(license) > 10 else license


def get_arch(data):
    if data['platform'] in ('i686', 'x86_64'):
        return data['platform']
    return 'any'


def make(package):
    versions = client.package_releases(package)

    if not versions:
        raise PipkgException('Package not found %s' % package)

    else:
        # TODO add an option to chose the version, or select the last stable
        version = versions[0]

    data = client.release_data(package, version)

    if not data:
        raise PipkgException('PyPi did not return any information '
                             'for version %s' % version)

    source = get_source(data)

    output_directory = '%s-%s' % (data['name'], data['version'])
    egg_path = '%s.egg-info' % data['name'].lower()

    pkgbuild = Pkgbuild(
        pkgname='python2-%s' % data['name'].lower(),
        pkgver=data['version'],
        pkgdesc=data['summary'],
        arch=(get_arch(data),),
        license=(get_license(data),),
        depends=('python2', 'python2-setuptools'),
        source=(source['url'],),
        md5sums=(source.get('md5_digest') or 'SKIP',),
    )

    if source['packagetype'] == 'bdist_wheel':
        print('WHEEL')

    else:
        pkgbuild.prepare = r'''
        find "$srcdir/{output_directory}" -name '*.py' | \
            xargs sed -i "s|#!/usr/bin/env python$|#!/usr/bin/env python2|"
        '''.format(**locals()),

        pkgbuild.build = r'''
        cd {output_directory}

        python2 setup.py build
        '''.format(**locals()),

        pkgbuild.package = r'''
        cd {output_directory}

        depends=($(cat src/{egg_path}/requires.txt |
            sed 's/\(\w\+\).*/python2-\L\1/'))

        python2 setup.py install --root="$pkgdir" --optimize=1
        '''.format(**locals()),

    return pkgbuild
