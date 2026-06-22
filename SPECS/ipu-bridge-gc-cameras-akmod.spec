%global akmod_name ipu-bridge-gc-cameras
%global kmod_name ipu_bridge
%global src_dir %{akmod_name}-%{version}

Name:           akmod-%{akmod_name}
Version:        0.1
Release:        1%{?dist}
Summary:        Akmods package for Intel IPU6 bridge support for GC camera sensors

License:        GPL-2.0-only
URL:            https://github.com/pdamonte/ipu-bridge-gc-cameras-akmod
BuildArch:      noarch

Source0:        ipu-bridge.c
Source1:        Makefile

Requires:       akmods
Requires:       gcc
Requires:       make
Requires:       kernel-devel
Requires(post): akmods
Requires(post): kmodtool

%description
Akmods source package for a patched Intel IPU6 bridge module that advertises
support for GalaxyCore GCTI5035 and GCTI8034 camera sensors.

%prep
rm -rf %{src_dir}
mkdir -p %{src_dir}
cp -p %{SOURCE0} %{src_dir}/ipu-bridge.c
cp -p %{SOURCE1} %{src_dir}/Makefile

cat > %{src_dir}/kmodtool.conf <<'EOF'
%define kmod_name ipu_bridge
%define kmod_driver_version 0.1
%define kmod_rpm_name ipu-bridge-gc-cameras-kmod
%define kmod_kernel_version %{?kernel_version}
%define kmod_common_package 1
EOF

cat > %{src_dir}/%{akmod_name}.kmodspec <<'EOF'
%global kmod_name ipu_bridge
%global kmod_driver_version 0.1

Name:           %{kmod_name}-kmod
Version:        %{kmod_driver_version}
Release:        1%{?dist}
Summary:        Intel IPU6 bridge module with GC camera sensor support
License:        GPL-2.0-only

%description
Patched Intel IPU6 bridge module with support for GCTI5035 and GCTI8034.

%prep

%build
make KERNEL_RELEASE=%{kernel_version} KERNEL_BUILD=/usr/src/kernels/%{kernel_version}

%install
install -D -m 0644 ipu-bridge.ko \
  %{buildroot}/usr/lib/modules/%{kernel_version}/extra/ipu-bridge.ko

%files
/usr/lib/modules/%{kernel_version}/extra/ipu-bridge.ko
EOF

%build

%install
install -d %{buildroot}%{_usrsrc}/akmods/%{akmod_name}
cp -a %{src_dir}/. %{buildroot}%{_usrsrc}/akmods/%{akmod_name}/

%post
akmods --akmod %{akmod_name} || true

%files
%{_usrsrc}/akmods/%{akmod_name}

%changelog
* Sun Jun 21 2026 pdamonte <pdamonte@users.noreply.github.com> - 0.1-1
- Initial akmod package for Intel IPU6 bridge GC camera support.
