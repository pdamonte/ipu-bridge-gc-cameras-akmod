#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
RPM_TOPDIR="${ROOT_DIR}/rpmbuild"
MISSING=()

require_command() {
	local command="$1"
	local package="$2"

	if ! command -v "$command" >/dev/null 2>&1; then
		MISSING+=("$package")
	fi
}

require_command rpmbuild rpm-build
require_command make make
require_command gcc gcc

if ! rpm -q akmods >/dev/null 2>&1; then
	MISSING+=("akmods")
fi

if ! rpm -q "kernel-devel-$(uname -r)" >/dev/null 2>&1; then
	MISSING+=("kernel-devel-$(uname -r)")
fi

if [ "${#MISSING[@]}" -gt 0 ]; then
	echo "Missing required Fedora packages:" >&2
	printf '  %s\n' "${MISSING[@]}" >&2
	echo >&2
	echo "Install them first:" >&2
	printf '  sudo dnf install' >&2
	printf ' %q' "${MISSING[@]}" >&2
	echo >&2
	exit 1
fi

rm -rf "${RPM_TOPDIR}"
mkdir -p "${RPM_TOPDIR}/SOURCES" "${RPM_TOPDIR}/SPECS"
cp -a "${ROOT_DIR}/SOURCES/." "${RPM_TOPDIR}/SOURCES/"
cp -a "${ROOT_DIR}/SPECS/." "${RPM_TOPDIR}/SPECS/"

rpmbuild \
	--define "_topdir ${RPM_TOPDIR}" \
	-ba "${RPM_TOPDIR}/SPECS/ipu-bridge-gc-cameras-akmod.spec"

find "${RPM_TOPDIR}/RPMS" "${RPM_TOPDIR}/SRPMS" -type f -print
