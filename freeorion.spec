Name:           freeorion
Version:        0.3.15
Release:        2%{?dist}.R
Summary:        FreeOrion is a free, open source, turn-based space empire and galactic conquest (4X) computer game.

License:        GPLv2
URL:            http://www.freeorion.org/
Source0:        %{name}-%{version}.tar.bz2
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Patch1:         freeorion-compile-error-fix.patch
Patch2:         freeorion-path-fix.patch
Source10:       freeorion.desktop
Source11:       freeorion.png
Source12:	freeoriond.desktop

BuildRequires:  openal-soft-devel freealut-devel libogg-devel libvorbis-devel bullet-devel
BuildRequires:  libgigi-devel libgigi-SDL-devel libgigi-ogre-devel
BuildRequires:  boost-devel mesa-libGLU-devel mesa-libGL-devel zlib-devel libpng-devel
BuildRequires:  python-devel libtool-ltdl
BuildRequires:  desktop-file-utils

# Fonts
Requires:       dejavu-sans-fonts %{name}-server = %{version}

# self data packages
Requires:       %{name}-data = %{version} %{name}-data-ai = %{version}

%package data
Summary:        Data files for FreeOrion game
License:        CCASv3
BuildArch:      noarch

%package data-ai
Summary:        Python data files for AI of FreeOrion game
BuildArch:      noarch

%package server
Summary:        Network daemon for FreeOrion game

%description
FreeOrion is a free, open source, turn-based space empire and galactic conquest (4X) computer game
being designed and built by the FreeOrion project. 
FreeOrion is inspired by the tradition of the Master of Orion games, 
but is not a clone or remake of that series or any other game. 

%description data
Data files for FreeOrion game. Art, music, fonts and other

%description data-ai
Python data files for AI of FreeOrion game

%description server
Network daemon for FreeOrion game

%prep
%setup -q
%patch1 -p2 -b .compile-error-fix
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
install -m 644 ogre_plugins.cfg $RPM_BUILD_ROOT%{_datadir}/%{name}/ogre_plugins.cfg

# install desktop and png files
install -m 644 -D %{SOURCE10} $RPM_BUILD_ROOT%{_datadir}/applications/%{name}.desktop
install -m 644 -D %{SOURCE11} $RPM_BUILD_ROOT%{_datadir}/icons/%{name}.png
install -m 644 -D %{SOURCE12} $RPM_BUILD_ROOT%{_datadir}/applications/%{name}d.desktop
install -m 644 -D %{SOURCE11} $RPM_BUILD_ROOT%{_datadir}/icons/%{name}d.png

desktop-file-install                                    \
--add-category="Game"                                   \
--dir=%{buildroot}%{_datadir}/applications              \
%{SOURCE10}
desktop-file-validate %{buildroot}/%{_datadir}/applications/%{name}.desktop
desktop-file-install                                    \
--add-category="Game"                                   \
--dir=%{buildroot}%{_datadir}/applications              \
%{SOURCE12}
desktop-file-validate %{buildroot}/%{_datadir}/applications/%{name}d.desktop


%files
%doc RELEASE-NOTES-V03.txt
%{_bindir}/%{name}
%{_bindir}/%{name}ca
%{_datadir}/%{name}/ogre_plugins.cfg
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/%{name}.png

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
%doc RELEASE-NOTES-V03.txt
%{_bindir}/%{name}d
%{_datadir}/applications/%{name}d.desktop
%{_datadir}/icons/%{name}d.png


%changelog
* Tue Aug  2 2011 Alexei Panov <elemc AT atisserv DOT ru> - 0.3.15-2.R
- Update for new ogre version

* Wed Jul 27 2011 Alexei Panov <elemc AT atisserv DOT ru> - 0.3.15-1
- Initial build
