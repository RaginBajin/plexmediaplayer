Name:           plexmediaplayer
Version:        1.1.1.293
Release:        1%{?dist}
Summary:        Plex Media Player for Fedora 23

License:        GPLv2
URL:            https://plex.tv/
# See: https://fedoraproject.org/wiki/Packaging:SourceURL?rd=Packaging/SourceURL#Git_Tags
#Source0:        https://github.com/plexinc/plex-media-player/archive/v1.0.6.229-1ce41570.tar.gz#/%{name}-%{version}.tar.gz
Source0:        https://github.com/plexinc/plex-media-player/archive/v1.1.1.293-cc2cc067.tar.gz#/%{name}-%{version}.tar.gz
Source1:	%{name}.desktop
# https://raw.githubusercontent.com/plexinc/plex-media-player/master/resources/images/icon.png
Source2:	%{name}.png
Source3:	%{name}.appdata.xml
Source4:	%{name}.service
Source5:	%{name}.target
Source6:	%{name}.pkla.disabled
Source7:	%{name}-standalone
Source8:        %{name}.te
Source9:        %{name}.pp
Source10:       %{name}-standalone-enable
#Patch0:         %{name}-issue175.patch
Patch1:         %{name}-FIX-QT-PATHS.patch
Patch2:         %{name}-FIX-CPP-URL.patch

BuildRequires:	cmake
BuildRequires:  ninja-build
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  libmpv
BuildRequires:  libmpv-devel
BuildRequires:  libdrm-devel
BuildRequires:  mesa-libGL-devel
BuildRequires:  SDL2-devel
BuildRequires:  libcec-devel
BuildRequires:  qt5-qtbase-devel >= 5.6
BuildRequires:  qt5-qtdeclarative-devel >= 5.6
BuildRequires:  qt5-qtwebchannel-devel >= 5.6
BuildRequires:  qt5-qtwebengine-devel >= 5.6

Requires:	libmpv
Requires:       libdrm
Requires:       mesa-libGL
Requires:       SDL2
Requires:       libcec
Requires:       qt5-qtbase >= 5.6
Requires:       qt5-qtbase-gui >= 5.6
Requires:       qt5-qtdeclarative >= 5.6
Requires:       qt5-qtwebchannel >= 5.6
Requires:       qt5-qtwebengine >= 5.6
# User creation.
Requires(pre):	shadow-utils

%description
Plex Media Player - Client for Plex Media Server.

%prep
#%setup -n %{name}-%{version} -q
%setup -n plex-media-player-1.1.1.293-cc2cc067 -q
#%patch0 -p0
%patch1 -p0
# /!\ TEMPORARY PATCH FOR VERSION 1.6.0, TO REMOVE FOR NEXT VERSION /!\.
#%patch2 -p0

%build
rm -Rf build
mkdir build
cd build
cmake -GNinja -DCMAKE_BUILD_TYPE=RelWithDebInfo -DQTROOT=/usr/lib64/qt5 -DMPV_INCLUDE_DIR=/usr/include/mpv -DMPV_LIBRARY=/usr/lib64/libmpv.so.1 -DCMAKE_INSTALL_PREFIX=/usr ..
ninja-build

%install
rm -rf $RPM_BUILD_ROOT
%{__mkdir_p} %{_buildrootdir}/%{name}-%{version}-%{release}.%{_arch}%{_bindir}
%{__install} -m0755 %{_builddir}/%{buildsubdir}/build/src/plexmediaplayer %{_buildrootdir}/%{name}-%{version}-%{release}.%{_arch}%{_bindir}/plexmediaplayer
%{__install} -m0755 %{_builddir}/%{buildsubdir}/build/src/pmphelper       %{_buildrootdir}/%{name}-%{version}-%{release}.%{_arch}%{_bindir}/pmphelper
%{__install} -m0755 %{_sourcedir}/%{name}-standalone                      %{_buildrootdir}/%{name}-%{version}-%{release}.%{_arch}%{_bindir}/%{name}-standalone

%{__mkdir_p} %{_buildrootdir}/%{name}-%{version}-%{release}.%{_arch}%{_datadir}/icons/hicolor/256x256/apps
%{__install} -m0644 %{_sourcedir}/%{name}.png                             %{_buildrootdir}/%{name}-%{version}-%{release}.%{_arch}%{_datadir}/icons/hicolor/256x256/apps/%{name}.png

appstream-util validate-relax --nonet %{_sourcedir}/%{name}.appdata.xml
%{__mkdir_p} %{_buildrootdir}/%{name}-%{version}-%{release}.%{_arch}%{_datadir}/appdata
%{__install} -m0644 %{_sourcedir}/%{name}.appdata.xml                     %{_buildrootdir}/%{name}-%{version}-%{release}.%{_arch}%{_datadir}/appdata/%{name}.appdata.xml

%{__mkdir_p} %{_buildrootdir}/%{name}-%{version}-%{release}.%{_arch}%{_datadir}/%{name}
%{__install} -m0755 %{_sourcedir}/%{name}-standalone-enable               %{_buildrootdir}/%{name}-%{version}-%{release}.%{_arch}%{_datadir}/%{name}/%{name}-standalone-enable

%{__mkdir_p} %{_buildrootdir}/%{name}-%{version}-%{release}.%{_arch}%{_datadir}/%{name}/selinux
%{__install} -m0644 %{_sourcedir}/%{name}.te                              %{_buildrootdir}/%{name}-%{version}-%{release}.%{_arch}%{_datadir}/%{name}/selinux/%{name}.te
%{__install} -m0644 %{_sourcedir}/%{name}.pp                              %{_buildrootdir}/%{name}-%{version}-%{release}.%{_arch}%{_datadir}/%{name}/selinux/%{name}.pp

%{__mkdir_p} %{_buildrootdir}/%{name}-%{version}-%{release}.%{_arch}%{_prefix}/lib/systemd/system
%{__install} -m0644 %{_sourcedir}/%{name}.service                         %{_buildrootdir}/%{name}-%{version}-%{release}.%{_arch}%{_prefix}/lib/systemd/system/%{name}.service
%{__install} -m0644 %{_sourcedir}/%{name}.target                          %{_buildrootdir}/%{name}-%{version}-%{release}.%{_arch}%{_prefix}/lib/systemd/system/%{name}.target

%{__mkdir_p} %{_buildrootdir}/%{name}-%{version}-%{release}.%{_arch}%{_sysconfdir}/polkit-1/localauthority/50-local.d
%{__install} -m0644 %{_sourcedir}/%{name}.pkla.disabled	                  %{_buildrootdir}/%{name}-%{version}-%{release}.%{_arch}%{_sysconfdir}/polkit-1/localauthority/50-local.d/%{name}.pkla.disabled

desktop-file-validate %{_sourcedir}/%{name}.desktop
desktop-file-install --dir=%{_buildrootdir}/%{name}-%{version}-%{release}.%{_arch}%{_datadir}/applications %{_sourcedir}/%{name}.desktop


%files
/usr/bin/plexmediaplayer
/usr/bin/pmphelper
/usr/bin/plexmediaplayer-standalone
/usr/lib/systemd/system/plexmediaplayer.service
/usr/lib/systemd/system/plexmediaplayer.target
/usr/share/appdata/plexmediaplayer.appdata.xml
/usr/share/applications/plexmediaplayer.desktop
/usr/share/icons/hicolor/256x256/apps/plexmediaplayer.png
/usr/share/plexmediaplayer/plexmediaplayer-standalone-enable
/usr/share/plexmediaplayer/selinux/plexmediaplayer.te
/usr/share/plexmediaplayer/selinux/plexmediaplayer.pp
/etc/polkit-1/localauthority/50-local.d/plexmediaplayer.pkla.disabled


%pre
# Create "plexmediaplayer" if it not already exists.
#
# NEVER delete an user or group created by an RPM package. See:
# https://fedoraproject.org/wiki/Packaging:UsersAndGroups#Allocation_Strategies
/usr/bin/getent passwd plexmediaplayer >/dev/null || \
  /sbin/useradd -r -G dialout,video,lock,audio \
  -d %{_sharedstatedir}/plexmediaplayer --create-home -s /sbin/nologin \
  -c "Plex Media Player (Standalone)" plexmediaplayer
%{__chmod} 0750 %{_sharedstatedir}/plexmediaplayer
%{__chown} plexmediaplayer:plexmediaplayer %{_sharedstatedir}/plexmediaplayer


%post
%{__ln_s} -f %{_prefix}/lib/systemd/system/%{name}.service %{_sysconfdir}/systemd/system/
%{__ln_s} -f %{_prefix}/lib/systemd/system/%{name}.target  %{_sysconfdir}/systemd/system/

touch --no-create %{_datadir}/icons/hicolor
if [ -x %{_bindir}/gtk-update-icon-cache ]; then
  %{_bindir}/gtk-update-icon-cache -q %{_datadir}/icons/hicolor;
fi
update-mime-database %{_datadir}/mime &> /dev/null || :
update-desktop-database &> /dev/null || :


%postun
touch --no-create %{_datadir}/icons/hicolor
if [ -x %{_bindir}/gtk-update-icon-cache ]; then
  %{_bindir}/gtk-update-icon-cache -q %{_datadir}/icons/hicolor;
fi
update-mime-database %{_datadir}/mime &> /dev/null || :
update-desktop-database &> /dev/null || :


%changelog
* Tue May 3 2016 Joseph Bajin <josephbajin@gmail.com> - 1.1.1.293
- Updated to 1.1.1.293
* Sat Mar 26 2016 Jonathan Leroy <jonathan@harrycow.fr> - 1.0.6-2
- Fixes desktop file syntax.

* Sat Mar 26 2016 Jonathan Leroy <jonathan@harrycow.fr> - 1.0.6-1
- New upstream version 1.0.6.229.
- Workaround added for issue #244.
- Search! There is now global search in PMP. It's early days and doesn't work well with keyboards yet.
- The "three dots" indicating buffering could stick around for a very long time. We fixed that.
- MPEG-2 video direct playback is now working correctly.
- Switching servers from the dashboard is no longer slow.
- A variety of smaller fixes in the web-client.
- PMP will now open on the same physcial screen it was on last.
- Various resizing issues has been fixed where PMP could be stuck at very small size percentage.

* Wed Feb 24 2016 Jonathan Leroy <jonathan@harrycow.fr> - 1.0.5-1
- New upstream version 1.0.5.210.
- Updated web-client to 2.5.5. See https://forums.plex.tv/discussion/comment/1130675/#Comment_1130675 for details.
- Volume control: +/- is now mapped to volume control. Change your mapping to do increase/decrease_volume.
- Filter out the use of Num+ in the keymaps.
- Remove old update packages lying around on disk.
- Fix crash if we could not initialize Direct3D.
- The 7.1 audio OS X fixes described in 1.0.4 weren't actually shipped. Now they are.

* Tue Feb 02 2016 Jonathan Leroy <jonathan@harrycow.fr> - 1.0.4-1
- New upstream version 1.0.4.169.

* Sun Jan 03 2016 Jonathan Leroy <jonathan@harrycow.fr> - 1.0.3-7
- The "plexmediaplayer" user does not need a valid shell.

* Sun Jan 03 2016 Jonathan Leroy <jonathan@harrycow.fr> - 1.0.3-6
- Force permissions on /var/lib/plexmediaplayer.
- Adding SELinux rules for standalone mode.
- New script to enable standalone mode.

* Sun Jan 03 2016 Jonathan Leroy <jonathan@harrycow.fr> - 1.0.3-5
- Fixes user shell and home directory.
- Multiples fixes in Systemd files.

* Sun Jan 03 2016 Jonathan Leroy <jonathan@harrycow.fr> - 1.0.3-4
- Fixes user creation.

* Sun Jan 03 2016 Jonathan Leroy <jonathan@harrycow.fr> - 1.0.3-3
- Fixes standalone execution scripts.

* Sun Jan 03 2016 Jonathan Leroy <jonathan@harrycow.fr> - 1.0.3-2
- Standalone execution support.
- Updated AppData XML.

* Tue Dec 29 2015 Jonathan Leroy <jonathan@harrycow.fr> - 1.0.3-1
- Plex Media Player version 1.0.3.

