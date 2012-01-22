%global svnrev 4282

Name:	       freeorion
Version:       0.3.17
Release:       1%{?dist}.R
Summary:       FreeOrion is a free, open source, turn-based space empire and galactic conquest (4X) computer game

Group:	       Amusements/Games
License:       GPLv2
URL:	       http://www.freeorion.org/

# svn export -r 4282 https://freeorion.svn.sourceforge.net/svnroot/freeorion/trunk/FreeOrion freeorion-0.3.17
# tar -czvf freeorion-0.3.17.tar.gz freeorion-0.3.17/

Source0:    %{name}-%{version}.tar.gz

Source10:   freeorion.png
Source11:   freeorion.desktop
Source12:   freeoriond.desktop

Patch1:	    freeorion-0.3.17-compile-fix.patch
Patch2:	    freeorion-path-fix.patch

BuildRequires:	openal-soft-devel freealut-devel libogg-devel libvorbis-devel bullet-devel
BuildRequires:	libgigi-devel libgigi-SDL-devel libgigi-ogre-devel
BuildRequires:	mesa-libGLU-devel mesa-libGL-devel 
BuildRequires:	boost-devel zlib-devel libpng-devel
BuildRequires:	python-devel libtool-ltdl
BuildRequires:	desktop-file-utils

# fonts
Requires:	dejavu-sans-fonts
# server and data subpackages
Requires:    %{name}-server = %{version}
Requires:    %{name}-data = %{version} %{name}-data-ai = %{version}
# icon files
Requires:	hicolor-icon-theme

%package data
Summary:	Data files for FreeOrion game
License:	CCASv3
BuildArch:	noarch

%package data-ai
Summary:	Python data files for AI of FreeOrion game
BuildArch:	noarch

%package server
Summary:	Network daemon for FreeOrion game

%description 
FreeOrion is a free, open source, turn-based space empire and galactic
conquest (4X) computer game being designed and built by the FreeOrion
project.  FreeOrion is inspired by the tradition of the Master of
Orion games, but is not a clone or remake of that series or any other
game.

%description data
Art, music, fonts and other data files for FreeOrion game.

%description data-ai
Python data files for AI of FreeOrion game

%description server
Network daemon for FreeOrion game

%prep
%setup -q
%patch1 -p1 -b .compile-fix
%patch2 -p1 -b .path-fix

%build
%cmake .
make %{?_smp_mflags}

# Fix path to plugin
sed -i 's|PluginFolder=.|PluginFolder=%{_libdir}/OGRE|g' ogre_plugins.cfg

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

# remove COPYING (move it to doc)
rm -rf $RPM_BUILD_ROOT%{_datadir}/%{name}/default/COPYING

# remove existing fonts
rm -rf $RPM_BUILD_ROOT%{_datadir}/%{name}/default/DejaVu*.ttf
rm -rf $RPM_BUILD_ROOT%{_datadir}/%{name}/default/LICENSE.DejaVu

# links to font
for font in DejaVuSans.ttf DejaVuSans-Oblique.ttf DejaVuSans-BoldOblique.ttf DejaVuSans-Bold.ttf; do
    ln -sf %{_datadir}/fonts/dejavu/$font $RPM_BUILD_ROOT%{_datadir}/%{name}/default/
done

# install other files
install -m 644 ogre_plugins.cfg \
	$RPM_BUILD_ROOT%{_datadir}/%{name}/ogre_plugins.cfg

# install desktop files and icons
install -m 644 -D %{SOURCE10} \
	$RPM_BUILD_ROOT%{_datadir}/icons/hicolor/scalable/apps/%{name}.png
install -m 644 -D %{SOURCE10} \
	$RPM_BUILD_ROOT%{_datadir}/icons/hicolor/scalable/apps/%{name}d.png

desktop-file-install --dir=${RPM_BUILD_ROOT}%{_datadir}/applications %{SOURCE11}
desktop-file-install --dir=${RPM_BUILD_ROOT}%{_datadir}/applications %{SOURCE12}

%post
/bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%postun
if [ $1 -eq 0 ] ; then
    /bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    /usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi

%posttrans
/usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :

%files
%doc changelog.txt
%{_bindir}/%{name}
%{_bindir}/%{name}ca
%{_datadir}/%{name}/ogre_plugins.cfg
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/scalable/apps/%{name}.png

%files data
%doc default/COPYING
%{_datadir}/%{name}/default/*.txt
%{_datadir}/%{name}/default/*.xml
%{_datadir}/%{name}/default/data/*
%{_datadir}/%{name}/default/shaders/*
%{_datadir}/%{name}/default/DejaVu*.ttf

%files data-ai
%{_datadir}/%{name}/default/AI/*

%files server
%doc changelog.txt default/COPYING
%{_bindir}/%{name}d
%{_datadir}/applications/%{name}d.desktop
%{_datadir}/icons/hicolor/scalable/apps/%{name}d.png


%changelog
* Sat Jan 21 2012 Aleksandra Bookwar <alpha@bookwar.info> - 0.3.17-1.R
- Update to the latest stable version 0.3.17
- Various small fixes: Source0, icon paths, server license and so on.

* Tue Aug  2 2011 Alexei Panov <elemc AT atisserv DOT ru> - 0.3.15-2.R
- Update for new ogre version

* Wed Jul 27 2011 Alexei Panov <elemc AT atisserv DOT ru> - 0.3.15-1
- Initial build
