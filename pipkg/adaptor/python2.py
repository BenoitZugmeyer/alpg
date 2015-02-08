from xmlrpc.client import ServerProxy
import re

from pipkg.pkgbuild import Pkgbuild
from pipkg.exception import PipkgException

client = ServerProxy('http://pypi.python.org/pypi')

SOURCEFILE_TYPE_RE = re.compile(".*\.(tar|zip|gz|z|bz2?|xz|whl)",
                                re.IGNORECASE)


def is_sourcefile(url):
    return bool(url and SOURCEFILE_TYPE_RE.match(url))


def get_source(data):
    source = None
    md5sum = None

    raw_urls = client.release_urls(data['name'], data['version'])
    if raw_urls:
        for url in raw_urls:
            if is_sourcefile(url['url']):
                source = url['url']
                md5sum = url.get('md5_digest')
                break

    if not source and is_sourcefile(data.get('download_url')):
        source = data['download_url']

    if not source:
        raise PipkgException("Couldn't find any suitable source")

    return source, md5sum or 'SKIP'


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

    source, md5sum = get_source(data)

    output_directory = '%s-%s' % (data['name'], data['version'])
    egg_path = '%s.egg-info' % data['name'].lower()

    return Pkgbuild(
        pkgname='python2-%s' % data['name'].lower(),
        pkgver=data['version'],
        pkgdesc=data['summary'],
        arch=(get_arch(data),),
        license=(get_license(data),),
        depends=('python2', 'python2-setuptools'),
        source=(source,),
        md5sums=(md5sum,),

        prepare=r'''
        find "$srcdir/{output_directory}" -name '*.py' | \
            xargs sed -i "s|#!/usr/bin/env python$|#!/usr/bin/env python2|"
        '''.format(**locals()),

        build=r'''
        cd {output_directory}

        python2 setup.py build
        '''.format(**locals()),

        package=r'''
        cd {output_directory}

        depends=($(cat src/{egg_path}/requires.txt |
            sed 's/\(\w\+\).*/python2-\L\1/'))

        python2 setup.py install --root="$pkgdir" --optimize=1
        '''.format(**locals()),
    )
