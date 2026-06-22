#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

"${ROOT_DIR}/build-rpm.sh"

sudo dnf install -y "${ROOT_DIR}"/rpmbuild/RPMS/noarch/akmod-ipu-bridge-gc-cameras-*.rpm
sudo akmods --akmod ipu-bridge-gc-cameras --force
sudo modprobe -r intel_ipu6_isys intel_ipu6 ipu_bridge 2>/dev/null || true
sudo modprobe intel_ipu6_isys

modinfo ipu_bridge | grep '^filename:'
