%define scriptdir %{_datadir}/bootsplash/scripts
%define mdk_bg	%{_datadir}/mdk/backgrounds
%define debug_package %{nil}

%bcond_with moondrake
%ifarch %armx
%bcond_with grub
%else
%bcond_without grub
%endif

Name:		distro-theme
Version:	1.4.40
Release:	6
Summary:	Distribution plymouth theme
Url:		https://abf.io/software/distro-theme
Source0:	%{name}-%{version}.tar.xz
Source1:	%{name}.rpmlintrc
Source100:	generate-theme-package.sh
Source101:	generate-screensaver-package.sh
Source102:	generate-grub-package.sh
Source103:	generate-grub-config.sh
Patch0:		distro-theme-no-grub.patch
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
BuildRequires:	distro-release-OpenMandriva

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

%{expand:%(sh %{S:100} Moondrake "Moondrake GNU/Linux" "" "1920x1440" "Moondrake-tux-1920x1440-opaque.png")}
%{expand:%(sh %{S:101} Moondrake *-TUX.png)}
%{expand:%(sh %{S:102} Moondrake)}
%endif

%{expand:%(sh %{S:100} OpenMandriva "OpenMandriva Lx" "16x9")}
%{_iconsdir}/*.*
%{expand:%(sh %{S:101} OpenMandriva energy*.jpg)}
%if %{with grub}
%{expand:%(sh %{S:102} OpenMandriva)}
%endif

%prep
%setup -q
%apply_patches

%build
%if !%{with grub}
NO_GRUB=true
%endif
pwd
%if !%{with moondrake}
%make THEMES=OpenMandriva NO_GRUB="$NO_GRUB"
%else
%make NO_GRUB="$NO_GRUB"
%endif

%install
%if !%{with grub}
NO_GRUB=true
%endif
%if !%{with moondrake}
%makeinstall_std THEMES=OpenMandriva NO_GRUB="$NO_GRUB"
%else
%makeinstall_std NO_GRUB="$NO_GRUB"
%endif

# Default wallpaper should be available without browsing file system
mkdir -p %{buildroot}%{_datadir}/wallpapers
ln -sf /usr/share/mdk/backgrounds/default.png %{buildroot}%{_datadir}/wallpapers/default.png
ln -sf /usr/share/mdk/backgrounds/default.png %{buildroot}%{_datadir}/wallpapers/default.jpg

%if %{with grub}
%if %{with moondrake}
touch %{buildroot}%{_datadir}/wallpapers/default-opaque.{png,jpg}
%{expand:%(sh %{S:103} "Moondrake" "Moondrake GNU/Linux")}
%endif
%{expand:%(sh %{S:103} "OpenMandriva" "OpenMandriva Lx")}
%endif

%files common
%doc doc/*
%{_datadir}/wallpapers/default.jpg
%{_datadir}/wallpapers/default.png
%if %{with moondrake}
%{_datadir}/wallpapers/default-opaque.jpg
%{_datadir}/wallpapers/default-opaque.png
%endif

%files extra
%(for i in $(seq 12 76); do
	echo "%{mdk_bg}/flavor_of_freedom-$i.jpg"
done)

%if %{with moondrake}
%files -n complete-moondrake-theme
%endif
