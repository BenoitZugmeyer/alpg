import os.path
import json


def read_fixture(path):
    pkgbuild_path = os.path.join(os.path.dirname(__file__),
                                 "fixtures",
                                 *path.split("/"))

    with open(pkgbuild_path, "r") as fp:
        return fp.read()

def read_fixture_json(path):
    return json.loads(read_fixture(path))
