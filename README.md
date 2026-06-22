# Intel IPU6 bridge support for GC camera sensors on Fedora

Fedora akmods package for a patched Intel IPU6 bridge module that advertises
support for:

- `GCTI5035` / GalaxyCore GC5035-compatible sensors
- `GCTI8034` / GalaxyCore GC8034-compatible sensors

The built kernel module is `ipu_bridge`.

## Why this exists

The camera sensor modules can probe, but Intel IPU6 also needs the ACPI HIDs in
`ipu_supported_sensors[]` before it connects the cameras into the media graph.
This bridge adds:

```c
IPU_SENSOR_CONFIG("GCTI5035", 1, 438000000),
IPU_SENSOR_CONFIG("GCTI8034", 1, 336000000),
```

## Build Locally

```sh
sudo dnf install rpm-build akmods gcc make "kernel-devel-$(uname -r)"
./build-rpm.sh
```

The RPM output is written under `rpmbuild/RPMS/` and `rpmbuild/SRPMS/`.

## Install Locally

```sh
./install-local.sh
```

## Verify

```sh
modinfo ipu_bridge | grep filename
dmesg --ctime | grep -Ei 'GCTI5035|GCTI8034|Connected [0-9]+ cameras|intel-ipu6'
v4l2-ctl --list-devices
media-ctl -d /dev/media0 -p
```

## Related Sensor Modules

Use this package together with Fedora packages for:

- `gc5035` / `gti5035`
- `gc8034`

## Notes

This repo is Fedora-oriented. For Ubuntu/Debian-style DKMS packaging, use a
separate DKMS package instead.
