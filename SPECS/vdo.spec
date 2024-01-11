%global commit           53745c3cb82498a19d9bfd901bc015094233ca76
%global gittag           6.2.9.7
%global shortcommit      %(c=%{commit}; echo ${c:0:7})

%define spec_release 14
Summary: Management tools for Virtual Data Optimizer
Name: vdo
Version: %{gittag}
Release: %{spec_release}%{?dist}
License: GPLv2
Source0: https://github.com/dm-vdo/%{name}/archive/%{commit}/%{name}-%{shortcommit}.tar.gz
Patch0:  fix_dmeventd_linking.patch
URL: http://github.com/dm-vdo/vdo
Requires: lvm2 >= 2.03
Requires: python3-PyYAML >= 3.10
Requires: libuuid >= 2.23
Requires: kmod-kvdo >= 6.2
Requires: util-linux >= 2.32.1-7
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
BuildRequires: python3
BuildRequires: python3-devel
BuildRequires: systemd
%ifarch %{valgrind_arches}
BuildRequires: valgrind-devel
%endif
BuildRequires: zlib-devel
%{?systemd_requires}

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
make install DESTDIR=$RPM_BUILD_ROOT INSTALLOWNER= name=%{name} \
  bindir=%{_bindir} defaultdocdir=%{_defaultdocdir} libexecdir=%{_libexecdir} \
  mandir=%{_mandir} presetdir=%{_presetdir} \
  python3_sitelib=/%{python3_sitelib} sysconfdir=%{_sysconfdir} \
  unitdir=%{_unitdir}

# Fix the python3 shebangs
for file in %{_bindir}/vdo \
            %{_bindir}/vdostats
do
  pathfix.py -pni "%{__python3}" $RPM_BUILD_ROOT${file}
done

%post
%systemd_post vdo.service

%preun
%systemd_preun vdo.service

%postun
%systemd_postun_with_restart vdo.service

%files
#defattr(-,root,root)
%{_bindir}/vdo
%{_bindir}/vdo-by-dev
%{_bindir}/vdostats
%{_bindir}/vdodmeventd
%{_bindir}/vdodumpconfig
%{_bindir}/vdoforcerebuild
%{_bindir}/vdoformat
%{_bindir}/vdosetuuid
%{_libexecdir}/vdoprepareforlvm
%dir %{python3_sitelib}/%{name}
%{python3_sitelib}/%{name}/__init__.py
%{python3_sitelib}/%{name}/__pycache__/__init__.cpython-36.opt-1.pyc
%{python3_sitelib}/%{name}/__pycache__/__init__.cpython-36.pyc
%dir %{python3_sitelib}/%{name}/vdomgmnt/
%{python3_sitelib}/%{name}/vdomgmnt/CommandLock.py
%{python3_sitelib}/%{name}/vdomgmnt/Configuration.py
%{python3_sitelib}/%{name}/vdomgmnt/Constants.py
%{python3_sitelib}/%{name}/vdomgmnt/Defaults.py
%{python3_sitelib}/%{name}/vdomgmnt/ExitStatusMixins.py
%{python3_sitelib}/%{name}/vdomgmnt/KernelModuleService.py
%{python3_sitelib}/%{name}/vdomgmnt/MgmntUtils.py
%{python3_sitelib}/%{name}/vdomgmnt/Service.py
%{python3_sitelib}/%{name}/vdomgmnt/SizeString.py
%{python3_sitelib}/%{name}/vdomgmnt/Utils.py
%{python3_sitelib}/%{name}/vdomgmnt/VDOArgumentParser.py
%{python3_sitelib}/%{name}/vdomgmnt/VDOService.py
%{python3_sitelib}/%{name}/vdomgmnt/VDOKernelModuleService.py
%{python3_sitelib}/%{name}/vdomgmnt/VDOOperation.py
%{python3_sitelib}/%{name}/vdomgmnt/__init__.py
%{python3_sitelib}/%{name}/vdomgmnt/__pycache__/CommandLock.cpython-36.opt-1.pyc
%{python3_sitelib}/%{name}/vdomgmnt/__pycache__/CommandLock.cpython-36.pyc
%{python3_sitelib}/%{name}/vdomgmnt/__pycache__/Configuration.cpython-36.opt-1.pyc
%{python3_sitelib}/%{name}/vdomgmnt/__pycache__/Configuration.cpython-36.pyc
%{python3_sitelib}/%{name}/vdomgmnt/__pycache__/Constants.cpython-36.opt-1.pyc
%{python3_sitelib}/%{name}/vdomgmnt/__pycache__/Constants.cpython-36.pyc
%{python3_sitelib}/%{name}/vdomgmnt/__pycache__/Defaults.cpython-36.opt-1.pyc
%{python3_sitelib}/%{name}/vdomgmnt/__pycache__/Defaults.cpython-36.pyc
%{python3_sitelib}/%{name}/vdomgmnt/__pycache__/ExitStatusMixins.cpython-36.opt-1.pyc
%{python3_sitelib}/%{name}/vdomgmnt/__pycache__/ExitStatusMixins.cpython-36.pyc
%{python3_sitelib}/%{name}/vdomgmnt/__pycache__/KernelModuleService.cpython-36.opt-1.pyc
%{python3_sitelib}/%{name}/vdomgmnt/__pycache__/KernelModuleService.cpython-36.pyc
%{python3_sitelib}/%{name}/vdomgmnt/__pycache__/MgmntUtils.cpython-36.opt-1.pyc
%{python3_sitelib}/%{name}/vdomgmnt/__pycache__/MgmntUtils.cpython-36.pyc
%{python3_sitelib}/%{name}/vdomgmnt/__pycache__/Service.cpython-36.opt-1.pyc
%{python3_sitelib}/%{name}/vdomgmnt/__pycache__/Service.cpython-36.pyc
%{python3_sitelib}/%{name}/vdomgmnt/__pycache__/SizeString.cpython-36.opt-1.pyc
%{python3_sitelib}/%{name}/vdomgmnt/__pycache__/SizeString.cpython-36.pyc
%{python3_sitelib}/%{name}/vdomgmnt/__pycache__/Utils.cpython-36.opt-1.pyc
%{python3_sitelib}/%{name}/vdomgmnt/__pycache__/Utils.cpython-36.pyc
%{python3_sitelib}/%{name}/vdomgmnt/__pycache__/VDOArgumentParser.cpython-36.opt-1.pyc
%{python3_sitelib}/%{name}/vdomgmnt/__pycache__/VDOArgumentParser.cpython-36.pyc
%{python3_sitelib}/%{name}/vdomgmnt/__pycache__/VDOKernelModuleService.cpython-36.opt-1.pyc
%{python3_sitelib}/%{name}/vdomgmnt/__pycache__/VDOKernelModuleService.cpython-36.pyc
%{python3_sitelib}/%{name}/vdomgmnt/__pycache__/VDOOperation.cpython-36.opt-1.pyc
%{python3_sitelib}/%{name}/vdomgmnt/__pycache__/VDOOperation.cpython-36.pyc
%{python3_sitelib}/%{name}/vdomgmnt/__pycache__/VDOService.cpython-36.opt-1.pyc
%{python3_sitelib}/%{name}/vdomgmnt/__pycache__/VDOService.cpython-36.pyc
%{python3_sitelib}/%{name}/vdomgmnt/__pycache__/__init__.cpython-36.opt-1.pyc
%{python3_sitelib}/%{name}/vdomgmnt/__pycache__/__init__.cpython-36.pyc
%dir %{python3_sitelib}/%{name}/statistics/
%{python3_sitelib}/%{name}/statistics/Command.py
%{python3_sitelib}/%{name}/statistics/Field.py
%{python3_sitelib}/%{name}/statistics/KernelStatistics.py
%{python3_sitelib}/%{name}/statistics/LabeledValue.py
%{python3_sitelib}/%{name}/statistics/StatFormatter.py
%{python3_sitelib}/%{name}/statistics/StatStruct.py
%{python3_sitelib}/%{name}/statistics/VDOReleaseVersions.py
%{python3_sitelib}/%{name}/statistics/VDOStatistics.py
%{python3_sitelib}/%{name}/statistics/__init__.py
%{python3_sitelib}/%{name}/statistics/__pycache__/Command.cpython-36.opt-1.pyc
%{python3_sitelib}/%{name}/statistics/__pycache__/Command.cpython-36.pyc
%{python3_sitelib}/%{name}/statistics/__pycache__/Field.cpython-36.opt-1.pyc
%{python3_sitelib}/%{name}/statistics/__pycache__/Field.cpython-36.pyc
%{python3_sitelib}/%{name}/statistics/__pycache__/KernelStatistics.cpython-36.opt-1.pyc
%{python3_sitelib}/%{name}/statistics/__pycache__/KernelStatistics.cpython-36.pyc
%{python3_sitelib}/%{name}/statistics/__pycache__/LabeledValue.cpython-36.opt-1.pyc
%{python3_sitelib}/%{name}/statistics/__pycache__/LabeledValue.cpython-36.pyc
%{python3_sitelib}/%{name}/statistics/__pycache__/StatFormatter.cpython-36.opt-1.pyc
%{python3_sitelib}/%{name}/statistics/__pycache__/StatFormatter.cpython-36.pyc
%{python3_sitelib}/%{name}/statistics/__pycache__/StatStruct.cpython-36.opt-1.pyc
%{python3_sitelib}/%{name}/statistics/__pycache__/StatStruct.cpython-36.pyc
%{python3_sitelib}/%{name}/statistics/__pycache__/VDOReleaseVersions.cpython-36.opt-1.pyc
%{python3_sitelib}/%{name}/statistics/__pycache__/VDOReleaseVersions.cpython-36.pyc
%{python3_sitelib}/%{name}/statistics/__pycache__/VDOStatistics.cpython-36.opt-1.pyc
%{python3_sitelib}/%{name}/statistics/__pycache__/VDOStatistics.cpython-36.pyc
%{python3_sitelib}/%{name}/statistics/__pycache__/__init__.cpython-36.opt-1.pyc
%{python3_sitelib}/%{name}/statistics/__pycache__/__init__.cpython-36.pyc
%dir %{python3_sitelib}/%{name}/utils/
%{python3_sitelib}/%{name}/utils/Command.py
%{python3_sitelib}/%{name}/utils/FileUtils.py
%{python3_sitelib}/%{name}/utils/Timeout.py
%{python3_sitelib}/%{name}/utils/Transaction.py
%{python3_sitelib}/%{name}/utils/YAMLObject.py
%{python3_sitelib}/%{name}/utils/__init__.py
%{python3_sitelib}/%{name}/utils/__pycache__/Command.cpython-36.opt-1.pyc
%{python3_sitelib}/%{name}/utils/__pycache__/Command.cpython-36.pyc
%{python3_sitelib}/%{name}/utils/__pycache__/FileUtils.cpython-36.opt-1.pyc
%{python3_sitelib}/%{name}/utils/__pycache__/FileUtils.cpython-36.pyc
%{python3_sitelib}/%{name}/utils/__pycache__/Timeout.cpython-36.opt-1.pyc
%{python3_sitelib}/%{name}/utils/__pycache__/Timeout.cpython-36.pyc
%{python3_sitelib}/%{name}/utils/__pycache__/Transaction.cpython-36.opt-1.pyc
%{python3_sitelib}/%{name}/utils/__pycache__/Transaction.cpython-36.pyc
%{python3_sitelib}/%{name}/utils/__pycache__/YAMLObject.cpython-36.opt-1.pyc
%{python3_sitelib}/%{name}/utils/__pycache__/YAMLObject.cpython-36.pyc
%{python3_sitelib}/%{name}/utils/__pycache__/__init__.cpython-36.opt-1.pyc
%{python3_sitelib}/%{name}/utils/__pycache__/__init__.cpython-36.pyc
%{_unitdir}/vdo.service
%{_unitdir}/vdo-start-by-dev@.service
%{_presetdir}/97-vdo.preset
%dir %{_sysconfdir}/bash_completion.d
%{_sysconfdir}/bash_completion.d/vdostats
%{_sysconfdir}/bash_completion.d/vdo
%{_sysconfdir}/udev/rules.d/69-vdo-start-by-dev.rules
%dir %{_defaultdocdir}/%{name}
%license %{_defaultdocdir}/%{name}/COPYING
%dir %{_defaultdocdir}/%{name}/examples
%dir %{_defaultdocdir}/%{name}/examples/ansible
%doc %{_defaultdocdir}/%{name}/examples/ansible/README.txt
%doc %{_defaultdocdir}/%{name}/examples/ansible/test_vdocreate.yml
%doc %{_defaultdocdir}/%{name}/examples/ansible/test_vdocreate_alloptions.yml
%doc %{_defaultdocdir}/%{name}/examples/ansible/test_vdoremove.yml
%dir %{_defaultdocdir}/%{name}/examples/monitor
%doc %{_defaultdocdir}/%{name}/examples/monitor/monitor_check_vdostats_logicalSpace.pl
%doc %{_defaultdocdir}/%{name}/examples/monitor/monitor_check_vdostats_physicalSpace.pl
%doc %{_defaultdocdir}/%{name}/examples/monitor/monitor_check_vdostats_savingPercent.pl
%dir %{_defaultdocdir}/%{name}/examples/systemd
%doc %{_defaultdocdir}/%{name}/examples/systemd/VDO.mount.example
%{_mandir}/man8/vdo.8.gz
%{_mandir}/man8/vdostats.8.gz
%{_mandir}/man8/vdodmeventd.8.gz
%{_mandir}/man8/vdodumpconfig.8.gz
%{_mandir}/man8/vdoforcerebuild.8.gz
%{_mandir}/man8/vdoformat.8.gz
%{_mandir}/man8/vdoprepareforlvm.8.gz
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
%{_bindir}/vdoregenerategeometry
%{_mandir}/man8/adaptlvm.8.gz
%{_mandir}/man8/vdoaudit.8.gz
%{_mandir}/man8/vdodebugmetadata.8.gz
%{_mandir}/man8/vdodumpblockmap.8.gz
%{_mandir}/man8/vdodumpmetadata.8.gz
%{_mandir}/man8/vdolistmetadata.8.gz
%{_mandir}/man8/vdoreadonly.8.gz
%{_mandir}/man8/vdoregenerategeometry.8.gz

%changelog
* Wed May 24 2023 - Susan LeGendre-McGhee <slegendr@redhat.com> - 6.2.9.7-14
- Enhanced vdoPrepareForLVM to repair misaligned conversions.
- Resolves: rhbz#2182739

* Wed Apr 12 2023 - Susan LeGendre-McGhee <slegendr@redhat.com> - 6.2.9.1-14
- Updated vdoPrepareForLVM to allow LVM to use larger extents.
- Resolves: rhbz#2182739

* Mon Jul 18 2022 - Andy Walsh <awalsh@redhat.com> - 6.2.7.17-14
- Fixed excessive vdo2lvm "Retrying" messages.
- Resolves: rhbz#1986595
- Fixed a pylint 2+ complaint in the vdo scripts.
- Resolves: rhbz#2072131
- Updated vdo script documentation and help text for the uuid option.
- Resolves: rhbz#2089957

* Fri Feb 11 2022 - Andy Walsh <awalsh@redhat.com> - 6.2.6.14-14
- Added a tool to make LVMVDO pools read/write so that support and
  debugging tools may access them.
- Resolves: rhbz#1999640

* Mon Nov 15 2021 - Andy Walsh <awalsh@redhat.com> - 6.2.6.7-14
- Fixed bugs in the vdopreparelvm check to determine whether a device has
  already been converted.
- Resolves: rhbz#2017843
- Fixed an issue in the vdo-by-dev tool which could result in a failure to
  start vdo devices when some devices in the vdo config file do not exist.
- Resolves: rhbz#2022154

* Wed Nov 03 2021 - Andy Walsh <awalsh@redhat.com> - 6.2.6.3-14
- Added a check to vdopreparelvm to determine whether it has already been
  converted.
- Resolves: rhbz#2017843

* Fri Aug 20 2021 - Andy Walsh <awalsh@redhat.com> - 6.2.5.74-14
- Renamed vdo2LVM to vdopreparelvm and moved its installation location to
  /usr/libexec so that it is not in common default paths as this utility is
  intended to be called from LVM, not directly by users.
- Related: rhbz#1986930

* Thu Jul 22 2021 - Andy Walsh <awalsh@redhat.com> - 6.2.5.65-14
- Fixed Coverity scan issues.
- Resolves: rhbz#1982878

* Thu Jul 15 2021 - Andy Walsh <awalsh@redhat.com> - 6.2.5.62-14
- Removed extraneous fields from the super block of a converted index.
- Resolves: rhbz#1965546
- Added a parameter to the lvm conversion tool to specify the amount of
  space to free up.
- Resolves: rhbz#1966827
- Fixed calculation of the number of expiring chapters in a converted
  index.
- Resolves: rhbz#1975546

* Tue Jun 01 2021 - Andy Walsh <awalsh@redhat.com> - 6.2.5.41-14
- Integrated the vdo to lvm conversion tool into the vdo management script
  and modified the tool itself to correctly convert the UDS index so that
  dedupe information is not lost by conversion.
- Resolves: rhbz#1928284

* Thu May 20 2021 - Andy Walsh <awalsh@redhat.com> - 6.2.5.21-14
- Added a tool for converting a VDO volume from the vdo management script
  to LVM. The tool can be invoked from the new vdo convert command.
- Related: rhbz#1928284
- Fixed a (relatively harmless) buffer overflow in vdo userspace tools.
- Resolves: rhbz#1927938

* Thu May 13 2021 - Andy Walsh <awalsh@redhat.com> - 6.2.5.11-14
- Introduced new memory size parameter values for UDS indexes which have
  been converted from vdo script management to LVM.
- Related: rhbz1928284
- Modified vdo script to fail if the same option is supplied multiple
  times.
- Resolves: rhbz#1944087
- Fixed permissions on the vdo script's lock directory.
- Resolves: rhbz#1952105

* Thu Oct 01 2020 - Andy Walsh <awalsh@redhat.com> - 6.2.4.14-14
- Added --pending option to the vdo status command to indicate
  configuration options which have been modified but will not take
  effect until the next device start.
- Resolves: rhbz#1838314

* Fri Jun 19 2020 - Andy Walsh <awalsh@redhat.com> - 6.2.3.107-14
- Fixed more Coverity errors.
- Resolves: rhbz#1827763

* Tue Jun 09 2020 - Andy Walsh <awalsh@redhat.com> - 6.2.3.100-14
- Modified vdoformat to display the minimum required physical size for the
  specified parameters if the format fails due to insufficient space.
- Resolves: rhbz#1683945
- Modified the vdo status command to report values from running devices
  rather than the config file when the devices are running.
- Resolves: rhbz#1790983
- Actually made the new summary mode of vdoaudit the default.
- Resolves: rhbz#1687996
- Fixed a bug in vdodumpmetadata and vdodumpblockmap which could result in
  the wrong block(s) being dumped.
- Resolves: rhbz#1643297

* Tue Jun 02 2020 - Andy Walsh <awalsh@redhat.com> - 6.2.3.91-14
- Removed unused UDS bio statistics
- Resolves: rhbz#1827762
- Added a summary mode to vdoaudit and made this mode the default. Also
  added histograms.
- Resolves: rhbz#1687996
- Modified vdostats to accept short (one character) options.
- Resolves: rhbz#1787472
- Modified vdo script to use lsblk to identify LVM created VDO volumes.
- Resolves: rhbz#1825344
- Modified vdo script to avoid unnecessary config file updates when
  removing VDO volumes.
- Resolves: rhbz#1804440
- Fixed a cast which caused a Coverity complaint.
- Resolves: rhbz#1827763
- Fixed a cut&paste error in the vdosetuuid man page.
- Resolves: rhbz#1643297
- Fixed documentation of logical threads.
- Resolves: rhbz#1827764
- Began creation of a package of binaries for investigating VDO issues.
- Resolves: rhbz#1643297
- Updated VDO to use udev/systemd rules for startup.
- Resolves: rhbz#1837759
- Modified VDO volume creation to use libblkid instead of pvcreate to
  determine whether the underlying storage is already in use. Moved
  these checks from the vdo script into the vdoformat utility.
- Resolves: rhbz#1771698
- Modified the vdo status command to treat a running vdo volume is
  authoratative over the config file.
- Resolves: rhbz#1790983
- Added a new utility, vdoregenerategeometry, which can be used to
  recover a VDO whose initial blocks have been overwritten
  accidentaly.
- Resolves: rhbz#1773421

* Tue Feb 11 2020 - Andy Walsh <awalsh@redhat.com> - 6.2.2.117-13
- Improved man pages and help text for vdo script and vdo utilities.
- Resolves: rhbz#1505748
- Resolves: rhbz#1636043
- Resolves: rhbz#1746539
- Modified vdoformat to display the maximum VDO size based on the
  configured slab size when formatting a volume. Modified vdo script to
  also display this output when creating a new VDO.
- Resolves: rhbz#1659173

* Mon Nov 25 2019 - Andy Walsh <awalsh@redhat.com> - 6.2.2.33-12
- Fixed bug in the import command of the vdo script which would fail if
  there were no active dm devices.
- Resolves: rhbz#1767491
- Added a version command to the vdo script to report the script version.
- Resolves: rhbz#1730429
- Added version options to vdo utilities which did not have one.
- Resolves: rhbz#1730429
- Removed deprecated vdoprepareupgrade utility.
- Resolves: rhbz#1774700

* Wed Oct 30 2019 - Andy Walsh <awalsh@redhat.com> - 6.2.2.24-11
- Began preparations for releasing more VDO analysis and debugging tools.
- Relates: rhbz#1687996
- Really added the ability to modify the UUID of a VDO device (the previous
  version omitted some of the files necessary for this feature).
- Resolves: rhbz#1713749

* Thu Oct 17 2019 - Andy Walsh <awalsh@redhat.com> - 6.2.2.18-11
- Added the ability to modify the UUID of a VDO device.
- Resolves: rhbz#1713749
- Added an import command to the vdo script to allow management of an
  existing VDO device which is not already in the vdo config file.
- Resolves: rhbz#1737619
- Modified the vdo script to warn the user when starting or stopping a VDO
  device if the device is already in the desired state.
- Resolves: rhbz#1738651

* Fri Aug 02 2019 - Andy Walsh <awalsh@redhat.com> - 6.2.1.134-11
- Added UUID filtering of underlying devices when running vdo create with
  the --force flag as this failed when run on certain PVs.
- Resolves: rhbz#1710017

* Fri Jun 14 2019 - Andy Walsh <awalsh@redhat.com> - 6.2.1.102-11
- Added bash command completion for the vdo command.
  - Resolves: rhbz#1540287
- Modified the vdo script's list command to not display VDO devices which
  were not created with the vdo command (i.e. via LVM or using raw dm
  commands).
  - Resolves: rhbz#1686091
- Modified vdostats to continue to work on VDO devices which were not
  created with the vdo script.
  - Resolves: rhbz#1686091
- Modified vdo script to always close the UDS index when disabling
  deduplication on a running VDO device.
  - Resolves: rhbz#1643291

* Sun May 05 2019 - Andy Walsh <awalsh@redhat.com> - 6.2.1.48-10
- Added bash command completion for vdostats.
  - Resolves: rhbz#1666425
- Added missing newline to the output from vdoFormat.
  - Resolves: rhbz#1669492
- Fixed bug in the value displayed by vdostats for statistics which are not
  currently available.
  - Resolves: rhbz#1668747
- Updated vdo script to reflect changes in lvm.
  - Resolves: rhbz#1684249
- Reduced error output when removing a VDO device whose backing storage is
  missing.
  - Resolves: rhbz#1684248
- Removed the VDO Ansible module and examples from the vdo package.
  - Resolves: rhbz#1669534
  - Resolves: rhbz#1663259
- Fixed bugs in vdo script argument parsing.
  - Resolves: rhbz#1679224

* Fri Dec 14 2018 - Andy Walsh <awalsh@redhat.com> - 6.2.0.293-10
- Fixed a bug in the vdo script when checking the logical thread count.
- Resolves: rhbz#1645325
- Corrected the vdo script manpage entry for maxDiscardSize.
- Resolves: rhbz#1651251
- Allowed VDO backing devices to be specified by major:minor device number.
- Resolves: rhbz#1594285
- Fixed bugs when the vdo script is invoked against an existing device
  which is not a VDO.
- Resolves: rhbz#1588083
- Update vdo manpage to reflect deleted statistics.
- Resolves: rhbz#1639792
- Updated vdo script to handle partitioned devices
- Resolves: rhbz#1658224

* Fri Nov 16 2018 - Andy Walsh <awalsh@redhat.com> - 6.2.0.273-9
- Fixed a build dependency issue with device-mapper-devel
- Resolves: rhbz#1650686
- Improved checking for existing LVM physical volumes when formatting a new VDO
  volume.
- Resolves: rhbz#1627859
- Removed read cache statistics, configuration options, and table line
  parameters.
- Resolves: rhbz#1639792
- Fixed a bug which would cause the default logical size to be 480 KB smaller
  than it could be without causing over-provisioning.
- Resolves: rhbz#1645690
- Limited the number of logical zones to 60.
- Resolves: rhbz#1645325
- Removed extraneous man pages.
- Resolves: rhbz#1649950

* Sun Oct 07 2018 - Andy Walsh <awalsh@redhat.com> - 6.2.0.239-8
- Modified vdo script to use the new physical and logical growth procedures
  including support for the new table line format (the old format is still
  supported as well).
- Resolves: rhbz#1631869

* Mon Sep 17 2018 - Andy Walsh <awalsh@redhat.com> - 6.2.0.219-8
- Fixed error path memory leaks in the UDS module.
- Resolves: rhbz#1609403
- Convered nagios scripts to monitor scripts
- Made all configuration load errors use generic messaging in the vdo
  script.
- Resolves: rhbz#1626237
- Added missing va_end() calls.
- Resolves: rhbz#1627953
- Modified Makefile to take build flags from rpmbuild.
- Resolves: rhbz#1624184

* Fri Aug  3 2018 - Florian Weimer <fweimer@redhat.com> - 6.2.0.187-8
- Honor %%{valgrind_arches}

* Mon Jul 30 2018 - Florian Weimer <fweimer@redhat.com> - 6.2.0.187-7
- Rebuild with fixed binutils

* Sun Jul 29 2018 - Andy Walsh <awalsh@redhat.com> - 6.2.0.187-6
- Improved man pages.
- Resolves: rhbz#1600247
- Modified vdo scripts to ignore (but preserve) unrecognized parameters in the
  vdo config file so that config files are compatible across versions.
- Resolves: rhbz#1604122

* Fri Jul 06 2018 - Andy Walsh <awalsh@redhat.com> - 6.2.0.132-6
- Converted to use %%{__python3} on utility scripts.

* Thu Jun 28 2018 - Andy Walsh <awalsh@redhat.com> - 6.2.0.132-5
- Fixed handling of relative paths supplied to the --confFile options of
  the vdo script.

* Thu Jun 21 2018 - Andy Walsh <awalsh@redhat.com> - 6.2.0.109-4
- Fixed a bug in the vdo script which would fail with a python backtrace
  when the script was invoked with no arguments.
- Resolves: rhbz#1581204
- Modified the vdo script to not allow creation of a VDO device on top of
  an already running VDO device.
- Made the ordering of the output of vdo list stable.
- Resolves: rhbz#1584823
- Fixed issues with UDS on platforms where "char" is an unsigned type.
- Converted UDS to use GCC's built-in macros for determining endianness.
- Fixed a bug in the --vdoLogLevel option to the vdo python script when
  using python 3
- Resolves: rhbz#1586043

* Mon Jun 04 2018 - Andy Walsh <awalsh@redhat.com> - 6.2.0.71-4
Note: This is a pre-release version, future versions of VDO may not support
VDO devices created with this version.
- Modified vdo script to reqiure --force to remove a VDO volume with no
  device.
- Improved man pages.
- Converted python tools to use python 3.

* Tue May 01 2018 - Andy Walsh <awalsh@redhat.com> - 6.2.0.35-3.py3
- Updated to python3
- Also added aarch64 as an architecture

* Fri Apr 27 2018 - Andy Walsh <awalsh@redhat.com> - 6.2.0.35-3
Note: This is a pre-release version, future versions of VDO may not support
      VDO devices created with this version.
- Added validation that the release version numbers in the geometry and
  super block match on load.
- Fixed bug where VDO would always be created with a dense index even when
  a sparse index was requested.
- Fixed compilation problems on newer versions of GCC.

* Wed Apr 25 2018 - Andy Walsh <awalsh@redhat.com> - 6.2.0.32-3.updated_vdoGeometry
- Experimental build that uses a different way to spell the loadable version

* Tue Apr 24 2018 - Andy Walsh <awalsh@redhat.com> - 6.2.0.32-3
Note: This is a pre-release version, future versions of VDO may not support
      VDO devices created with this version.
- Add a library, libuser.a, to provide easy access to VDO user space code
  for other projects.
- Fixed a bug in vdo script when /dev/disk/by-id does not exist.
- Fixed an internationalization bug in the vdo script's --indexMemory
  option.
- Changed vdo script to not accept --vdoSlabSize=0 as a way of specifying
  the default since it was confusing. The default can be obtained by merely
  omitting the parameter entirely.

* Thu Apr 19 2018 - Andy Walsh <awalsh@redhat.com> - 6.2.0.4-3
- Added dependency for lvm2

* Tue Apr 17 2018 - Andy Walsh <awalsh@redhat.com> - 6.2.0.4-2
- Added missing kmod-kvdo requirement
- Resolves: rhbz#1568039

* Fri Apr 13 2018 - Andy Walsh <awalsh@redhat.com> - 6.2.0.4-1
- Updated to use github for Source0
- Reformatted tags to be easier to read
- Initial RHEL8 RPM rhbz#1503786

* Fri Apr 13 2018 - J. corwin Coburn <corwin@redhat.com> - 6.2.0.4-1
- Initial pre-release for RHEL 8.
  - Please be aware that this version is not compatible with previous versions
    of VDO. Support for loading or upgrading devices created with VDO version
    6.1 will be available soon.
- Management tools will work with both python 2 and python 3.
- Dedupe path improvements.
- Beginnings of support for non-x86 architectures.
- Removed obsolete code from UDS.

* Fri Feb 16 2018 - Joseph Chapman <jochapma@redhat.com> - 6.1.0.149-16
- Sync mode is safe if underlying storage changes to requiring flushes
- Resolves: rhbz#1540777

* Wed Feb 07 2018 - Joseph Chapman <jochapma@redhat.com> - 6.1.0.146-16
- VDO start command now does index memory checking
- Module target is now "vdo" instead of "dedupe"
- VDO remove with no device no longer puts a spurious file in /dev
- ANsible module no longer fails on modification operations
- Resolves: rhbz#1510567
- Resolves: rhbz#1530358
- Resolves: rhbz#1535597
- Resolves: rhbz#1536214

* Tue Feb 06 2018 - Andy Walsh <awalsh@redhat.com> - 6.1.0.144-16
- Updated summary and description
- Resolves: rhbz#1541409

* Thu Feb 01 2018 - Joseph Chapman <jochapma@redhat.com> - 6.1.0.130-15
- vdo growLogical by less than 4K gives correct error
- Fix URL to point to GitHub tree
- Resolves: rhbz#1532653
- Resolves: rhbz#1539059

* Fri Jan 19 2018 - Joseph Chapman <jochapma@redhat.com> - 6.1.0.124-14
- Added a specific error for less than 1 block growLogical.
- Resolves: rhbz#1532653

* Wed Jan 10 2018 - Joseph Chapman <jochapma@redhat.com> - 6.1.0.114-14
- VDO automatically chooses the proper write policy by default
- Package uninstall removes vdo.service symlinks
- Resolves: rhbz#1525305
- Resolves: rhbz#1531047

* Thu Dec 21 2017 - Joseph Chapman <jochapma@redhat.com> - 6.1.0.106-13
- Handle bogus --confFile and --logfile arguments
- Produce more informative vdo manager high-level help
- Generate command-specific unrecognized argument messages
- Resolves: rhbz#1520927
- Resolves: rhbz#1522750
- Resolves: rhbz#1525560

* Tue Dec 12 2017 - Joseph Chapman <jochapma@redhat.com> - 6.1.0.97-13
- Remove vdo --noRun option
- Clean up vdo error handling
- Prevent python stack traces on vdo errors
- Add more bounds checking to indexMem
- Resolves: rhbz#1508544
- Resolves: rhbz#1508918
- Resolves: rhbz#1520991
- Resolves: rhbz#1522754

* Fri Dec 08 2017 - Joseph Chapman <jochapma@redhat.com> - 6.1.0.89-13
- Build changes for UUID
- Limit VDO physical size
- Limit command options to those applicable to the subcommand
- Fix vdo --modifyBlockMapPeriod
- Report missing command option appropriately for all subcommands
- Fix behavior of --indexMem when there's not enough memory
- Remove obsolete nagios plugin from examples
- Better error behavior for failing vdo status commands
- Fix boundary check error for vdoLogicalSize
- Resolves: rhbz#1507927
- Resolves: rhbz#1508452
- Resolves: rhbz#1508544
- Resolves: rhbz#1508918
- Resolves: rhbz#1509002
- Resolves: rhbz#1510567
- Resolves: rhbz#1512631
- Resolves: rhbz#1522943

* Fri Dec 01 2017 - Joseph Chapman <jochapma@redhat.com> - 6.1.0.72-12
- Don't corrupt an existing filesystem with "vdo create" without "--force"
- Resolves: rhbz#1510581

* Mon Nov 27 2017 - Ken Raeburn <raeburn@redhat.com> - 6.1.0.55-11
- Don't corrupt an existing filesystem with "vdo create" without "--force"
- Resolves: rhbz#1510581

* Fri Nov 17 2017 - Joseph Chapman <jochapma@redhat.com> - 6.1.0.55-10
- manual pages: note logical size limit of 4P
- manual pages: make cache size/thread count link clearer
- Resolves: rhbz#1508452
- Resolves: rhbz#1511042

* Fri Nov 03 2017 - Joseph Chapman <jochapma@redhat.com> - 6.1.0.46-9
- update manpage to not allow 0 as an option
- enforce maximum vdoPhysicalThreads
- update manpage to describe maximum vdoPhysicalThreads
- Resolves: rhbz#1510405
- Resolves: rhbz#1511075
- Resolves: rhbz#1511085
- Resolves: rhbz#1511091

* Fri Nov 03 2017 - Joseph Chapman <jochapma@redhat.com> - 6.1.0.34-8
- Bugfixes
- Resolves: rhbz#1480047

* Mon Oct 30 2017 - Joseph Chapman <jochapma@redhat.com> - 6.1.0.0-7
- Don't let make install try to set file ownerships itself
- Resolves: rhbz#1480047

* Thu Oct 12 2017 - Joseph Chapman <jochapma@redhat.com> - 6.1.0.0-6
- Added new man pages
- Resolves: rhbz#1480047

* Fri Oct  6 2017 - Joseph Chapman <jochapma@redhat.com> - 6.1.0.0-5
- Fixed a typo in the package description
- Fixed man page paths
- Resolves: rhbz#1480047

* Thu Oct  5 2017 - Joseph Chapman <jochapma@redhat.com> - 6.1.0.0-4
- Fix vdostats name in nagios examples
- Build only on the x86_64 architecture
- Add systemd files
- Resolves: rhbz#1480047

* Thu Oct  5 2017 - Joseph Chapman <jochapma@redhat.com> - 6.1.0.0-3
- Added missing Build-Requires and incorporated naming changes
- Resolves: rhbz#1480047

* Wed Oct  4 2017 - Joseph Chapman <jochapma@redhat.com> - 6.1.0.0-2
- Fixed requirements and tags in %files section
- Resolves: rhbz#1480047

* Tue Oct  3 2017 - Joseph Chapman <jochapma@redhat.com> - 6.1.0.0-1
- Initial implementation
- Resolves: rhbz#1480047
