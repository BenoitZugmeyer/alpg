#!/bin/bash

set -euo pipefail

TMP=$(mktemp --tmpdir -d alpg.XXXXXX)

function finish {
    rm -rf "$TMP"
}
trap finish EXIT

cd "$TMP"

cat << 'EOF' > PKGBUILD
pkgname=alpg
pkgver=1.0.dev0
pkgrel=1
pkgdesc="ArchLinux Package Generator"
arch=(any)
url="https://github.com/BenoitZugmeyer/alpg"
license=(Expat)
groups=()
depends=(python python-click)
makedepends=()
provides=()
conflicts=()
replaces=()
backup=()
options=(!emptydirs)
install=
source=(https://github.com/BenoitZugmeyer/alpg/archive/master.zip)
md5sums=(SKIP)

package() {
  cd "$pkgname-master"
  python setup.py install --root="$pkgdir/" --optimize=1
}

EOF

makepkg -i -s
