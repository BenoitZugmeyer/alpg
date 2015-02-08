import shlex
import textwrap

from pipkg.exception import PipkgException


class PkgbuildError(PipkgException):
    pass


class Field(object):

    _id = 0

    def __init__(self,
                 required=False,
                 default=None,
                 multi=False):

        Field._id += 1
        self._id = Field._id
        self.required = required
        self.default = default

    def __set__(self, pkgbuild, value):

        if value is not None:
            value = self.cast(value)

        if value is None:
            value = self.default

        pkgbuild._field_values[self] = value

    def __get__(self, pkgbuild, cls):
        return self.get(pkgbuild)

    def __lt__(self, other):
        return self._id < other._id

    def cast(self, value):
        return value

    def get(self, pkgbuild):
        return pkgbuild._field_values.get(self, self.default)

    def format_pkgbuild(self, pkgbuild):
        value = self.get(pkgbuild)
        if value is None:
            if self.required:
                raise PkgbuildError('%s is required' % self.name)
            return
        else:
            return self.format(value)


class Single(Field):

    def cast(self, value):

        if not isinstance(value, str):
            raise PkgbuildError('%s should be a string' % self.name)

        return value

    def format(self, value):
        return '%s=%s' % (self.name, shlex.quote(value))


class Comment(Single):

    def format(self, value):
        return '# %s: %s' % (self.name.capitalize(), value)


class Code(Single):

    def format(self, value):
        return '\n%s() {%s}' % (self.name,
                                textwrap.indent(textwrap.dedent(value), '  '))


class Multi(Field):

    def cast(self, value):

        if isinstance(value, str):
            value = (value,)

        elif isinstance(value, tuple):
            for v in value:
                if not isinstance(v, str):
                    raise PkgbuildError('Field %s contains a non-string '
                                        'value' % self.name)

        else:
            raise PkgbuildError('Unsupported type %s for field %s' %
                                (type(value), self.name))

        return value

    def format(self, value):
        return '%s=(%s)' % (self.name, (' '.join(shlex.quote(v)
                                                 for v in value)))


class PkgbuildMeta(type):

    def __new__(cls, name, bases, attrs):
        fields = []
        for n, value in attrs.items():
            if isinstance(value, Field):
                value.name = n
                fields.append(value)
        attrs['_fields'] = sorted(fields)

        return super().__new__(cls, name, bases, attrs)


class Pkgbuild(object, metaclass=PkgbuildMeta):

    _field_values = None

    author = Comment()
    maintainer = Comment()

    pkgname = Single(required=True)
    pkgver = Single(required=True)
    pkgrel = Single(required=True, default='1')
    pkgdesc = Single()
    arch = Multi(required=True, default=('any',))
    url = Single()
    license = Multi()
    depends = Multi()
    optdepends = Multi()
    source = Multi()

    sha1sums = Multi()
    md5sums = Multi()

    prepare = Code()
    build = Code()
    package = Code()

    def __init__(self, **kwargs):
        self._field_values = {}
        self.update(kwargs)

    def __str__(self):
        def iterlines():
            for field in self._fields:
                line = field.format_pkgbuild(self)
                if line:
                    yield line

        return '\n'.join(iterlines())

    def __setattr__(self, attr, value):
        if not hasattr(self, attr):
            raise PkgbuildError('Unknown field %s' % attr)

        super().__setattr__(attr, value)

    def update(self, *args, **kwargs):
        if kwargs:
            lst = kwargs.items()
        elif len(args):
            lst = args[0].items() if isinstance(args[0], dict) else args[0]
        else:
            lst = tuple()

        for field, value in lst:
            setattr(self, field, value)


if __name__ == '__main__':
    pkg = Pkgbuild(
        pkgname='12',
        pkgver='12.31')
    print(pkg.pkgname)
    print(pkg.arch)
    pkg.arch = 'foo'
    print(pkg.arch)
    print(pkg)
