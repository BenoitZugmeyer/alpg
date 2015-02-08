import subprocess
import shlex

from pipkg.exception import PipkgException


class ProcessError(PipkgException):
    pass


def run(exe, *args):
    try:
        p = subprocess.Popen((exe,) + args,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE)
    except FileNotFoundError:
        raise ProcessError('Executable not found: %s' % exe)

    if p.wait():
        raise ProcessError(p.stderr.read().decode() or
                           ('Unknown error while running command: %s' %
                            ' '.join(shlex.quote(a) for a in args)))

    return p.stdout.read().decode()
