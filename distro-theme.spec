%{python:import sys; sys.path.append(rpm.expandMacro("%{_sourcedir}"))}
%{python:import distrotheme}

%define scriptdir %{_datadir}/bootsplash/scripts
%define mdk_bg	%{_datadir}/mdk/backgrounds
%define debug_package %{nil}

%bcond_with moondrake

Name:		distro-theme
Version:	1.4.40
Release:	1
Url:		https://abf.io/software/distro-theme
Source0:	%{name}-%{version}.tar.xz
Source1:	%{name}.rpmlintrc
Source2:	distrotheme.py
License:	GPLv2+
BuildRequires:	imagemagick
BuildRequires:	gimp
BuildRequires:	gimp-python
BuildRequires:	python2-cairo
%ifnarch %armx
BuildRequires:	grub2
%endif
BuildRequires:	pngcrush
BuildRequires:	pngrewrite
BuildRequires:	fonts-ttf-dejavu
BuildRequires:	fonts-ttf-droid
BuildRequires:	fonts-ttf-gliphmaker.com

%description
This package contains the plymouth themes with its images and configuration
for different resolution as well as the desktop background image for different
distributions supported.

%package	common
Summary:	%{vendor} common theme for plymouth
Group:		Graphics
Obsoletes:	plymouth-theme-mdv
%rename		mandriva-theme-common

%description	common
This package contains common images for the %{vendor}
plymouth themes.

%package	extra
Summary:	Additional backgrounds from OpenMandriva LX users
Group:		Graphics
%rename		mandriva-theme-extra

%description	extra
This package contains winning picture from OpenMandriva LX various
background contest.

%if %{with moondrake}
%package -n	complete-moondrake-theme
Summary:	Meta package for installing all Moondrake theme packages
Suggests:	distro-theme-Moondrake
Suggests:	distro-theme-Moondrake-screensaver
Suggests:	faces-moondrake
Suggests:	sound-theme-moondrake
Suggests:	grub2-moondrake-theme
Suggests:	moondrake-kde4-config
#Suggests:	moondrake-lxde-config
Suggests:	distro-xfce-config-Moondrake

%description -n	complete-moondrake-theme
This package simply pulls in all the various packages that makes up the
complete Moondrake theme throughout the distribution.

%{python:distrotheme.theme_package("Moondrake", "Moondrake GNU/Linux", bg_ratio=None, bg_res="1920x1440", opaque="Moondrake-tux-1920x1440-opaque.png")}
%{python:distrotheme.screensaver_package("Moondrake", "*-TUX.png")}
%{python:distrotheme.boot_theme("Moondrake")}
%endif

%{python:distrotheme.theme_package("OpenMandriva", "OpenMandriva Lx", files=distrotheme.extra_files("%{_iconsdir}/*.*g"), bg_res=None, bg_ratio="16x9")}
%{python:distrotheme.screensaver_package("OpenMandriva", "energy*.jpg")}
%{python:distrotheme.boot_theme("OpenMandriva")}

%prep
%setup -q

%build
%if !%{with moondrake}
%make THEMES=OpenMandriva
%else
%make
%endif

%install
%if !%{with moondrake}
%makeinstall_std THEMES=OpenMandriva
%else
%makeinstall_std
%endif

# Default wallpaper should be available without browsing file system
mkdir -p %{buildroot}%{_datadir}/wallpapers
ln -sf /usr/share/mdk/backgrounds/default.png %{buildroot}%{_datadir}/wallpapers/default.png
ln -sf /usr/share/mdk/backgrounds/default.png %{buildroot}%{_datadir}/wallpapers/default.jpg

%if %{with moondrake}
touch %{buildroot}%{_datadir}/wallpapers/default-opaque.{png,jpg}
%{python:distrotheme.grub2conf("Moondrake", "Moondrake GNU/Linux")}
%endif
%{python:distrotheme.grub2conf("OpenMandriva", "OpenMandriva Lx")}

%files common
%doc doc/*
%{_datadir}/wallpapers/default.jpg
%{_datadir}/wallpapers/default.png
%if %{with moondrake}
%{_datadir}/wallpapers/default-opaque.jpg
%{_datadir}/wallpapers/default-opaque.png
%endif

%files extra
%{python:distrotheme.extra_files(start=12, stop=77,strfmt="%{mdk_bg}/flavor_of_freedom-%%.2d.jpg", printOut=True)}

%if %{with moondrake}
%files -n complete-moondrake-theme
%endif

