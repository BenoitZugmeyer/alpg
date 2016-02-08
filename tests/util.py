import os.path


def read_fixture(path):
    pkgbuild_path = os.path.join(os.path.dirname(__file__),
                                 "fixtures",
                                 *path.split("/"))

    with open(pkgbuild_path, "r") as fp:
        return fp.read()
