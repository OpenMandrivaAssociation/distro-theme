%define scriptdir %{_datadir}/bootsplash/scripts
%define mdk_bg %{_datadir}/mdk/backgrounds
%define debug_package %{nil}

# Not armx -- aarch64 has UEFI and can run grub
%ifarch %{arm}
%bcond_with grub
%else
%bcond_without grub
%endif

Name:		distro-theme
Version:	1.4.46.2
Release:	ZED'S DEAD BABY
Summary:	Distribution themes
Url:		https://github.com/OpenMandrivaSoftware/distro-theme
Source0:	https://github.com/OpenMandrivaSoftware/distro-theme/archive/v%{version}.tar.gz
Source10:	%{name}.rpmlintrc
Source100:	generate-theme-package.sh
Source101:	generate-screensaver-package.sh
Source102:	generate-grub-package.sh
Source103:	generate-grub-config.sh
License:	GPLv2+
BuildRequires:	imagemagick
%ifnarch %arm
BuildRequires:	grub2-extra
%endif
BuildRequires:	pngcrush
BuildRequires:	pngrewrite
BuildRequires:	fonts-ttf-dejavu
BuildRequires:	unifont-fonts
BuildRequires:	fonts-ttf-gliphmaker.com
BuildRequires:	distro-release-OpenMandriva

%description
This package contains the themes with its images and configuration
for different resolution as well as the desktop background image for different
distributions supported.

%package	common
Summary:	%{vendor} common theme
Group:		Graphics
Obsoletes:	plymouth-theme-mdv
%rename		mandriva-theme-common

%description	common
This package contains common images for the %{vendor} themes.

%package	extra
Summary:	Additional backgrounds from OpenMandriva LX users
Group:		Graphics
%rename		mandriva-theme-extra

%description	extra
This package contains winning picture from OpenMandriva LX various
background contest.

%{expand:%(sh %{S:100} OpenMandriva "OpenMandriva Lx" "16x9")}
%{_iconsdir}/*.*
%{_iconsdir}/hicolor/*/apps/*.*
%{_datadir}/plasma/look-and-feel/org.openmandriva4.desktop
%{expand:%(sh %{S:101} OpenMandriva energy*.jpg)}
%if %{with grub}
%{expand:%(sh %{S:102} OpenMandriva)}
%endif

%prep
%autosetup -p1

%build
%if !%{with grub}
NO_GRUB=true
%endif
pwd

%make_build THEMES=OpenMandriva NO_GRUB="$NO_GRUB"

%install
%if !%{with grub}
NO_GRUB=true
%endif

%make_install THEMES=OpenMandriva NO_GRUB="$NO_GRUB"

# Make sure the logo can be found where modern applications expect it
mkdir -p %{buildroot}%{_iconsdir}/hicolor/scalable/apps
cp %{buildroot}%{_iconsdir}/openmandriva.svg %{buildroot}%{_iconsdir}/hicolor/scalable/apps/
for i in 16 22 24 32 36 48 64 72 96 128 192 256 512; do
	mkdir -p %{buildroot}%{_iconsdir}/hicolor/${i}x${i}/apps
	convert -background none %{buildroot}%{_iconsdir}/openmandriva.svg %{buildroot}%{_iconsdir}/hicolor/${i}x${i}/apps/openmandriva.png
done

# Default wallpaper should be available without browsing file system
mkdir -p %{buildroot}%{_datadir}/wallpapers
ln -sf /usr/share/mdk/backgrounds/default.png %{buildroot}%{_datadir}/wallpapers/default.png
ln -sf /usr/share/mdk/backgrounds/default.png %{buildroot}%{_datadir}/wallpapers/default.jpg

%if %{with grub}
%{expand:%(sh %{S:103} "OpenMandriva" "OpenMandriva Lx")}
%else
rm -rf %{buildroot}/boot
%endif

mkdir -p %{buildroot}%{_datadir}/plasma/look-and-feel
mv OpenMandriva/splash %{buildroot}%{_datadir}/plasma/look-and-feel/org.openmandriva4.desktop

%if !%{with grub}
rm -rf %{buildroot}%{_sysconfdir}/grub.d
%endif

%files common
%doc doc/*
%{_datadir}/wallpapers/default.jpg
%{_datadir}/wallpapers/default.png

%files extra
%(for i in $(seq 12 76); do
	echo "%{mdk_bg}/flavor_of_freedom-$i.jpg"
done)
