import unittest

import alpg.adaptor.python2 as python2


class MockClient:

    _implem = python2.client
    _cache = {
        ('package_releases', 'Django'): ['1.8a1', '1.7.4', '1.7.3'],
        ('release_data', 'Django', '1.8a1'): {
            'maintainer': None,
            'platform': 'UNKNOWN',
            'cheesecake_documentation_id': None,
            'author': 'Django Software Foundation',
            'author_email': 'foundation@djangoproject.com',
            'downloads': {'last_week': 7824,
                          'last_month': 466369,
                          'last_day': 1162},
            'maintainer_email': None,
            '_pypi_ordering': 74,
            'requires_dist': ["bcrypt; extra == 'bcrypt'"],
            'bugtrack_url': '',
            'download_url': None,
            'stable_version': None,
            '_pypi_hidden': False,
            'version': '1.8a1',
            'cheesecake_code_kwalitee_id': None,
            'requires_python': None,
            'name': 'Django',
            'package_url': 'http://pypi.python.org/pypi/Django',
            'release_url': 'http://pypi.python.org/pypi/Django/1.8a1',
            'description': 'Django is a high-level Python Web framework that encourages rapid development\nand clean, pragmatic design. Thanks ...',
            'cheesecake_installability_id': None,
            'classifiers': ['Development Status :: 3 - Alpha',
                            'Environment :: Web Environment',
                            'Framework :: Django',
                            'Intended Audience :: Developers',
                            'License :: OSI Approved :: BSD License',
                            'Operating System :: OS Independent',
                            'Programming Language :: Python',
                            'Programming Language :: Python :: 2',
                            'Programming Language :: Python :: 2.7',
                            'Programming Language :: Python :: 3',
                            'Programming Language :: Python :: 3.2',
                            'Programming Language :: Python :: 3.3',
                            'Programming Language :: Python :: 3.4',
                            'Topic :: Internet :: WWW/HTTP',
                            'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
                            'Topic :: Internet :: WWW/HTTP :: WSGI',
                            'Topic :: Software Development :: Libraries :: Application Frameworks',
                            'Topic :: Software Development :: Libraries :: Python Modules'],
            'summary': 'A high-level Python Web framework that encourages rapid development and clean, pragmatic design.',
            'home_page': 'http://www.djangoproject.com/',
            'docs_url': '',
            'keywords': None,
            'license': 'BSD'},

        ('release_urls', 'Django', '1.8a1'): [{
            'size': 6899082,
            'filename': 'Django-1.8a1-py2.py3-none-any.whl',
            'url': 'https://pypi.python.org/packages/py2.py3/D/Django/Django-1.8a1-py2.py3-none-any.whl',
            'packagetype': 'bdist_wheel',
            'upload_time': None,
            'python_version': 'py2.py3', 'md5_digest': 'f7619792a8d8028c5be10f7d06a444ca', 'comment_text': '', 'has_sig': True, 'downloads': 3447}],
    }

    def __getattr__(self, name):
        def result(*args):
            key = (name,) + args
            if key not in self._cache:
                r = getattr(self._implem, name)(*args)
                self._cache[key] = r
                print("WARNING: you should add the following cache:")
                print("%s: %s," % (repr(key), repr(r)))
            return self._cache[key]

        return result


python2.client = MockClient()


class TestAdaptorNodejs(unittest.TestCase):

    def test_django(self):
        pkg = python2.make('Django')
        self.assertEqual(pkg.pkgname, 'python2-django')
        self.assertEqual(pkg.pkgver, '1.8a1')
        self.assertEqual(pkg.license, ('BSD',))
        self.assertEqual(pkg.source, (
            'https://pypi.python.org/packages/py2.py3/D/Django/'
            'Django-1.8a1-py2.py3-none-any.whl',))
        self.assertEqual(pkg.md5sums, ('f7619792a8d8028c5be10f7d06a444ca',))
        # TODO implement wheel suport
        # self.assertTrue(pkg.prepare)
        # self.assertTrue('# Rewrite python binary references' in pkg.prepare)
