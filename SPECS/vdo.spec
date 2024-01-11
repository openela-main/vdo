%global commit           e7a687da9e25d563838a6d2f4ca5036c80033ceb
%global gittag           8.2.2.2
%global shortcommit      %(c=%{commit}; echo ${c:0:7})

%define spec_release 1
Summary: Management tools for Virtual Data Optimizer
Name: vdo
Version: %{gittag}
Release: %{spec_release}%{?dist}
License: GPLv2
Source0: https://github.com/dm-vdo/%{name}/archive/%{commit}/%{name}-%{shortcommit}.tar.gz
Patch0:  fix_dmeventd_linking.patch
URL: http://github.com/dm-vdo/vdo
# Requires: libuuid >= 2.23
Requires: kmod-kvdo >= 8.2
# Requires: util-linux >= 2.32.1-7
Provides: kvdo-kmod-common = %{version}
ExcludeArch: s390
ExcludeArch: ppc
ExcludeArch: ppc64
ExcludeArch: i686
BuildRequires: gcc
BuildRequires: libblkid-devel
BuildRequires: libuuid-devel
BuildRequires: device-mapper-devel
BuildRequires: device-mapper-event-devel
%ifarch %{valgrind_arches}
BuildRequires: valgrind-devel
%endif
BuildRequires: zlib-devel

# Disable an automatic dependency due to a file in examples/monitor.
%define __requires_exclude perl

%description
Virtual Data Optimizer (VDO) is a device mapper target that delivers
block-level deduplication, compression, and thin provisioning.

This package provides the user-space management tools for VDO.

%prep
%setup -q -n %{name}-%{commit}
%patch0 -p1

%build
make

%install
make install DESTDIR=$RPM_BUILD_ROOT INSTALLOWNER= bindir=%{_bindir} \
  defaultdocdir=%{_defaultdocdir} name=%{name} mandir=%{_mandir} \
  sysconfdir=%{_sysconfdir}

%files
#defattr(-,root,root)
%{_bindir}/vdostats
%{_bindir}/vdodmeventd
%{_bindir}/vdodumpconfig
%{_bindir}/vdoforcerebuild
%{_bindir}/vdoformat
%{_bindir}/vdosetuuid
%dir %{_sysconfdir}/bash_completion.d
%{_sysconfdir}/bash_completion.d/vdostats
%dir %{_defaultdocdir}/%{name}
%license %{_defaultdocdir}/%{name}/COPYING
%dir %{_defaultdocdir}/%{name}/examples
%dir %{_defaultdocdir}/%{name}/examples/monitor
%doc %{_defaultdocdir}/%{name}/examples/monitor/monitor_check_vdostats_logicalSpace.pl
%doc %{_defaultdocdir}/%{name}/examples/monitor/monitor_check_vdostats_physicalSpace.pl
%doc %{_defaultdocdir}/%{name}/examples/monitor/monitor_check_vdostats_savingPercent.pl
%{_mandir}/man8/vdostats.8.gz
%{_mandir}/man8/vdodmeventd.8.gz
%{_mandir}/man8/vdodumpconfig.8.gz
%{_mandir}/man8/vdoforcerebuild.8.gz
%{_mandir}/man8/vdoformat.8.gz
%{_mandir}/man8/vdosetuuid.8.gz

%package support
Summary: Support tools for Virtual Data Optimizer
License: GPLv2
Requires: libuuid >= 2.23

%description support
Virtual Data Optimizer (VDO) is a device mapper target that delivers
block-level deduplication, compression, and thin provisioning.

This package provides the user-space support tools for VDO.

%files support
%{_bindir}/adaptLVMVDO.sh
%{_bindir}/vdoaudit
%{_bindir}/vdodebugmetadata
%{_bindir}/vdodumpblockmap
%{_bindir}/vdodumpmetadata
%{_bindir}/vdolistmetadata
%{_bindir}/vdoreadonly
%{_bindir}/vdorecover
%{_bindir}/vdoregenerategeometry
%{_mandir}/man8/adaptlvm.8.gz
%{_mandir}/man8/vdoaudit.8.gz
%{_mandir}/man8/vdodebugmetadata.8.gz
%{_mandir}/man8/vdodumpblockmap.8.gz
%{_mandir}/man8/vdodumpmetadata.8.gz
%{_mandir}/man8/vdolistmetadata.8.gz
%{_mandir}/man8/vdoreadonly.8.gz
%{_mandir}/man8/vdorecover.8.gz
%{_mandir}/man8/vdoregenerategeometry.8.gz

%changelog
* Wed Jun 21 2023 - Susan LeGendre-McGhee - 8.2.2.2-1
- Updated manpages.
- Resolves: rhbz#2176778

* Tue Jul 19 2022 - Andy Walsh <awalsh@redhat.com> - 8.2.0.2-1
- Rebased to latest upstream candidate.
- Resolves: rhbz#2071648

* Sat Feb 12 2022 - Andy Walsh <awalsh@redhat.com> - 8.1.1.360-1
- Fixed vdostats output issues.
- Resolves: rhbz#2004576
- Removed incorrect assumptions about major device numbers in vdostats.
- Resolves: rhbz#2045885
- Made improvements to the vdorecover script.
- Resolves: rhbz#2047543
- Added a tool to make LVMVDO pools read/write so that support and
  debugging tools may access them.
- Resolves: rhbz#2047543

* Sun Jan 23 2022 - Andy Walsh <awalsh@redhat.com> - 8.1.1.287-1
- Fixed off-by-one issue in vdostats.
- Resolves: rhbz#1999056
- Improved error handling and path validation in vdostats.
- Resolves: rhbz#2004576

* Tue Aug 10 2021 Mohan Boddu <mboddu@redhat.com> - 8.1.0.316-1.1
- Rebuilt for IMA sigs, glibc 2.34, aarch64 flags
  Related: rhbz#1991688

* Sun Aug 08 2021 - Andy Walsh <awalsh@redhat.com> - 8.1.0.316-1
- Rebased to upstream candidate.
- Resolves: rhbz#1955374
- Removed all python based tools, and all management should now be done with
  LVM.
- Resolves: rhbz#1949159
- vdostats is now a C program
- Resolves: rhbz#1972302

* Thu Jul 29 2021 - Andy Walsh <awalsh@redhat.com> - 8.1.0.264-1
- Rebased to upstream candidate.
- Related: rhbz#1955374

* Tue May 04 2021 - Andy Walsh <awalsh@redhat.com> - 8.1.0.1-1
- Initial build for EL9
- Resolves: rhbz#1955374
