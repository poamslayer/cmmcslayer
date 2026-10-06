#!/usr/bin/env bash
# Install the pinned oscal-cli, the validator ADR-0007 names, and put it on PATH.
#
#   bash scripts/install_oscal_cli.sh
#
# This is the one step a local operator runs. The web-session start hook runs
# the same script. It downloads metaschema-framework oscal-cli from Maven
# Central, checks the archive against the SHA-256 pinned below, unpacks it into
# ~/.local/share/oscal-cli-<version>, and links ~/.local/bin/oscal-cli to it.
# Make sure ~/.local/bin is on your PATH.
#
# It needs Java 11 or later and fails loudly without it. Re-running it with the
# pinned version already installed does nothing.
#
# Moving the pin is a deliberate change: update VERSION and SHA256 together,
# from the .sha256 file Maven Central publishes next to the archive.

set -euo pipefail

VERSION="3.2.0"
SHA256="e001b353ee245da6f4ff0ad930c4dfaa88083c63243ca004bd5f5bcef44e8ec8"
ARCHIVE="dev/metaschema/oscal/oscal-cli-enhanced/${VERSION}/oscal-cli-enhanced-${VERSION}-oscal-cli.zip"
# Two hosts for the same Maven Central content: repo1 rate-limits some networks.
MIRRORS="https://repo.maven.apache.org/maven2 https://repo1.maven.org/maven2"

PREFIX="${OSCAL_CLI_PREFIX:-$HOME/.local}"
DEST="$PREFIX/share/oscal-cli-$VERSION"
BIN="$PREFIX/bin"

fail() {
  echo "install_oscal_cli: $*" >&2
  exit 1
}

# Java first: oscal-cli is useless without it, and a missing Java is a hard stop.
command -v java > /dev/null 2>&1 \
  || fail "java not found. Install Java 11 or later (for example OpenJDK 17) and re-run."
java_major=$(java -version 2>&1 | sed -n 's/.*version "\([0-9]*\).*/\1/p' | head -1)
if [ -z "$java_major" ] || [ "$java_major" -lt 11 ]; then
  fail "oscal-cli $VERSION needs Java 11 or later; found '${java_major:-unknown}'."
fi

if [ -x "$DEST/bin/oscal-cli" ]; then
  mkdir -p "$BIN"
  ln -sf "$DEST/bin/oscal-cli" "$BIN/oscal-cli"
  echo "oscal-cli $VERSION already installed at $DEST"
  exit 0
fi

tmp=$(mktemp -d)
trap 'rm -rf "$tmp"' EXIT

echo "downloading oscal-cli $VERSION"
got=""
for mirror in $MIRRORS; do
  URL="$mirror/$ARCHIVE"
  if curl -fsSL --retry 5 --retry-delay 3 -o "$tmp/oscal-cli.zip" "$URL"; then
    got="yes"
    break
  fi
done
[ -n "$got" ] || fail "download failed from every mirror: $MIRRORS (path $ARCHIVE)"

actual=$(python3 -c 'import hashlib,sys; print(hashlib.sha256(open(sys.argv[1],"rb").read()).hexdigest())' "$tmp/oscal-cli.zip")
[ "$actual" = "$SHA256" ] \
  || fail "checksum mismatch for $URL: expected $SHA256, got $actual"

mkdir -p "$tmp/unpacked"
python3 -m zipfile -e "$tmp/oscal-cli.zip" "$tmp/unpacked"

# The archive holds bin/ and lib/ either at its root or under one folder.
root="$tmp/unpacked"
if [ ! -f "$root/bin/oscal-cli" ]; then
  root=$(dirname "$(dirname "$(find "$tmp/unpacked" -path '*/bin/oscal-cli' | head -1)")")
fi
[ -f "$root/bin/oscal-cli" ] || fail "the archive has no bin/oscal-cli"
chmod +x "$root/bin/oscal-cli"

mkdir -p "$PREFIX/share" "$BIN"
rm -rf "$DEST"
mv "$root" "$DEST"
ln -sf "$DEST/bin/oscal-cli" "$BIN/oscal-cli"

"$BIN/oscal-cli" --version > /dev/null 2>&1 \
  || fail "installed, but '$BIN/oscal-cli --version' did not run"
echo "oscal-cli $VERSION installed at $DEST, linked from $BIN/oscal-cli"
