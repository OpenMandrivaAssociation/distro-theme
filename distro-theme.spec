%define scriptdir %{_datadir}/bootsplash/scripts
%define mdk_bg %{_datadir}/mdk/backgrounds
%define bg_res 1920x1080
%define debug_package %{nil}

%define theme_header() \
Summary:	%{vendor}%{?1:-%1} theme for plymouth and desktop background \
Group:		Graphics \
\
%description	%{?1} \
This package contains the %{?1:-%1} plymouth theme \
with its images and configuration for different resolution as well as \
the the desktop background image. \

%define theme_package(o:) \
%package	%{1} \
Requires:	plymouth-system-theme \
Requires:	plymouth-plugin-script >= 0.8.2 \
Provides:	mandrake_theme mandrake-theme mandrakelinux-theme mandriva-theme = %{version}-%{release} \
Provides:	distro-theme = %{EVRD} \
Provides:	plymouth(system-theme) \
Obsoletes:	mandrake_theme mandrake-theme mandrakelinux-theme %{?-o:%{-o*}} \
Requires:	distro-theme-common \
Suggests:	distro-theme-screensaver \
Conflicts:	kdebase-konsole <= 1:3.4.2-37mdk \
Conflicts:	grub2 < 2.00-23 \
Requires(post):	bootsplash >= 3.4.1 \
%ifarch x86_64 %{ix86} \
Requires(post):	bootloader \
%endif \
%rename		mandriva-theme-Flash \
%rename		mandriva-theme-Free \
%rename		mandriva-theme-One \
%rename		mandriva-theme-Powerpack \
%rename		mandriva-theme-Moondrake \
%rename		mandriva-theme-OpenMandriva \
%theme_header(%{1})

%define theme_scripts() \
%post -n %{name}-%{1} \
if [ $1 -ge 1 ] ; then \
 if [ -f /etc/sysconfig/bootsplash ]; then \
    perl -pi -e 's/^\s*SPLASH=.*/SPLASH=auto/; s/^\s*THEME=.*/THEME=%{1}/' /etc/sysconfig/bootsplash \
 fi \
# (tpg) install grub2 theme \
 if [ -e %{_sysconfdir}/default/grub ]; then \
# Remove trailing blank lines from /etc/default/grub \
    sed -i -e :a -e '/^\n*$/{$d;N;};/\n$/ba' %{_sysconfdir}/default/grub \
# Check that /etc/default/grub ends in a linefeed \
    [ "$(tail -n 1 %{_sysconfdir}/default/grub | wc --lines)" = "1" ] || echo >> %{_sysconfdir}/default/grub \
# Remove old theme \
    sed -i '/GRUB_THEME=/d' %{_sysconfdir}/default/grub \
    sed -i '/GRUB_BACKGROUND=/d' %{_sysconfdir}/default/grub \
# Add theme \
    echo "GRUB_THEME=/boot/grub2/themes/%{1}/theme.txt" >> %{_sysconfdir}/default/grub \
    echo "GRUB_BACKGROUND=/boot/grub2/themes/%{1}/terminal_background.png" >> %{_sysconfdir}/default/grub \
 fi \
fi \
\
if [ -z "$DURING_INSTALL" ]; then \
  if [ -x %scriptdir/switch-themes ]; then \
    %scriptdir/switch-themes %{1} \
  fi \
else \
  %{_sbindir}/plymouth-set-default-theme %{1} \
fi \
\
if [ -f %mdk_bg/%{1}-root.png -a ! -f %mdk_bg/root/default.png -o -L %mdk_bg/root/default.png ]; then \
  rm -f %mdk_bg/root/default.png \
  ln -s %{1}-root-1600x1200.png %mdk_bg/root/default.png \
fi \
if [ -f %mdk_bg/%{1}-%bg_res.jpg -a ! -f %mdk_bg/default.jpg -o -L %mdk_bg/default.jpg ]; then \
  rm -f %mdk_bg/default.jpg \
  ln -s %{1}-%bg_res.png %mdk_bg/default.jpg \
fi \
\
if [ -f %mdk_bg/%{1}-%bg_res.png -a ! -f %mdk_bg/default.png -o -L %mdk_bg/default.png ]; then \
  rm -f %mdk_bg/default.png \
  ln -s %{1}-%bg_res.png %mdk_bg/default.png \
fi \
\
%triggerpostun -n %{name}-%{1} -- mandriva-theme-%{1} < 1.2.4 \
for f in kdeglobals konsolerc; do \
  if [ "`readlink /usr/share/config/$f 2>/dev/null`" == "$f-%{1}" ]; then \
    rm -f /usr/share/config/$f \
  fi \
done \
\
%preun -n %{name}-%{1} \
if [ "$1" == "0" ]; then \
  if [ -x %scriptdir/remove-theme ]; then \
    %scriptdir/remove-theme %{1} \
  fi \
# remove grub2 theme \
  sed -i '/GRUB_THEME=\/boot\/grub2\/themes\/%{1}\/theme.txt/d' %{_sysconfdir}/default/grub \
  link=`readlink %mdk_bg/default.png` \
  slink=${link%%-*} \
  if [ "$slink" == "%{1}" ]; then rm -f %mdk_bg/default.png;fi \
  link=`readlink %mdk_bg/default.jpg` \
  slink=${link%%-*} \
  if [ "$slink" == "%{1}" ]; then rm -f %mdk_bg/default.jpg;fi \
  link=`readlink %mdk_bg/%{1}.png` \
  slink=${link%%-*} \
  if [ "$slink" == "%{1}" ]; then rm -f %mdk_bg/%{1}.png;fi \
  link=`readlink %mdk_bg/%{1}.jpg` \
  slink=${link%%-*} \
  if [ "$slink" == "%{1}" ]; then rm -f %mdk_bg/%{1}.jpg;fi \
  link=`readlink %mdk_bg/root/%{1}.png` \
  slink=${link%%-*} \
  if [ "$slink" == "%{1}-root" ]; then rm -f %mdk_bg/root/default.png;fi \
fi

%define theme_files() \
%files %{1} \
/boot/grub2/themes/%{1} \
%_datadir/plymouth/themes/%{1} \
%if %{1} == "OpenMandriva" \
%_iconsdir/*.*g \
%mdk_bg/flavor_of_freedom-01.jpg \
%mdk_bg/flavor_of_freedom-02.jpg \
%mdk_bg/flavor_of_freedom-03.jpg \
%mdk_bg/flavor_of_freedom-04.jpg \
%mdk_bg/flavor_of_freedom-05.jpg \
%mdk_bg/flavor_of_freedom-06.jpg \
%mdk_bg/flavor_of_freedom-07.jpg \
%mdk_bg/flavor_of_freedom-08.jpg \
%mdk_bg/flavor_of_freedom-09.jpg \
%mdk_bg/flavor_of_freedom-10.jpg \
%mdk_bg/flavor_of_freedom-11.jpg \
%endif \
%mdk_bg/%{1}* \

Name:		distro-theme
Version:	1.4.24
Release:	3
Url:		%{disturl}
Source0:	https://abf.rosalinux.ru/omv_software/distro-theme/%{name}-%{version}.tar.xz
License:	GPLv2+
BuildRequires:	imagemagick
%theme_header

%theme_package Moondrake      -o distro-theme
%theme_package OpenMandriva   -o distro-theme

%package	common
Summary:	%{vendor} common theme for plymouth
Group:		Graphics
Obsoletes:	plymouth-theme-mdv
%rename		mandriva-theme-common

%description	common
This package contains common images for the %{vendor}
plymouth themes.

%package	extra
Summary:	Additional backgrounds from %{distribution} users
Group:		Graphics
%rename		mandriva-theme-extra

%description	extra
This package contains winning picture from %{distribution} various
background contest.

%package	screensaver
Summary:	%{distribution} screensaver
Group:		Graphics
%rename		mandriva-theme-Free-screensaver
%rename		mandriva-theme-Powerpack-screensaver
%rename		mandriva-theme-One-screensaver
%rename		mandriva-theme-Flash-screensaver
%rename		mandriva-theme-Rosa-screensaver
%rename		mandriva-screensaver
%rename		mandriva-theme-screensaver

%description	screensaver
This package contains the %{vendor} screensaver.

%prep
%setup -q

%build
%make

%install
%make install DESTDIR=%{buildroot}

# Default wallpaper should be available without browsing file system
mkdir -p %{buildroot}%{_datadir}/wallpapers
ln -s Moondrake-1920x1440.jpg %{buildroot}%{_datadir}/mdk/backgrounds/Moondrake.jpg

ln -s ../mdk/backgrounds/default.jpg %{buildroot}%{_datadir}/wallpapers/default.jpg
ln -s ../mdk/backgrounds/default.jpg %{buildroot}%{_datadir}/wallpapers/default.png

%theme_scripts Moondrake
%theme_scripts OpenMandriva

%files common
%doc doc/*
%{_datadir}/wallpapers/default.jpg
%{_datadir}/wallpapers/default.png

%files extra
%{_datadir}/mdk/backgrounds/flavor_of_freedom-12.jpg
%{_datadir}/mdk/backgrounds/flavor_of_freedom-13.jpg
%{_datadir}/mdk/backgrounds/flavor_of_freedom-14.jpg
%{_datadir}/mdk/backgrounds/flavor_of_freedom-15.jpg
%{_datadir}/mdk/backgrounds/flavor_of_freedom-16.jpg
%{_datadir}/mdk/backgrounds/flavor_of_freedom-17.jpg
%{_datadir}/mdk/backgrounds/flavor_of_freedom-18.jpg
%{_datadir}/mdk/backgrounds/flavor_of_freedom-19.jpg
%{_datadir}/mdk/backgrounds/flavor_of_freedom-20.jpg
%{_datadir}/mdk/backgrounds/flavor_of_freedom-21.jpg
%{_datadir}/mdk/backgrounds/flavor_of_freedom-22.jpg
%{_datadir}/mdk/backgrounds/flavor_of_freedom-23.jpg
%{_datadir}/mdk/backgrounds/flavor_of_freedom-24.jpg
%{_datadir}/mdk/backgrounds/flavor_of_freedom-25.jpg
%{_datadir}/mdk/backgrounds/flavor_of_freedom-26.jpg
%{_datadir}/mdk/backgrounds/flavor_of_freedom-27.jpg
%{_datadir}/mdk/backgrounds/flavor_of_freedom-28.jpg
%{_datadir}/mdk/backgrounds/flavor_of_freedom-29.jpg
%{_datadir}/mdk/backgrounds/flavor_of_freedom-30.jpg
%{_datadir}/mdk/backgrounds/flavor_of_freedom-31.jpg
%{_datadir}/mdk/backgrounds/flavor_of_freedom-32.jpg
%{_datadir}/mdk/backgrounds/flavor_of_freedom-33.jpg
%{_datadir}/mdk/backgrounds/flavor_of_freedom-34.jpg
%{_datadir}/mdk/backgrounds/flavor_of_freedom-35.jpg
%{_datadir}/mdk/backgrounds/flavor_of_freedom-36.jpg
%{_datadir}/mdk/backgrounds/flavor_of_freedom-37.jpg
%{_datadir}/mdk/backgrounds/flavor_of_freedom-38.jpg
%{_datadir}/mdk/backgrounds/flavor_of_freedom-39.png
%{_datadir}/mdk/backgrounds/flavor_of_freedom-40.jpg
%{_datadir}/mdk/backgrounds/flavor_of_freedom-41.jpg
%{_datadir}/mdk/backgrounds/flavor_of_freedom-42.jpg
%{_datadir}/mdk/backgrounds/flavor_of_freedom-43.jpg
%{_datadir}/mdk/backgrounds/flavor_of_freedom-44.jpg
%{_datadir}/mdk/backgrounds/flavor_of_freedom-45.jpg
%{_datadir}/mdk/backgrounds/flavor_of_freedom-46.jpg
%{_datadir}/mdk/backgrounds/flavor_of_freedom-47.jpg
%{_datadir}/mdk/backgrounds/flavor_of_freedom-48.jpg
%{_datadir}/mdk/backgrounds/flavor_of_freedom-49.jpg
%{_datadir}/mdk/backgrounds/flavor_of_freedom-50.jpg
%{_datadir}/mdk/backgrounds/flavor_of_freedom-51.jpg
%{_datadir}/mdk/backgrounds/flavor_of_freedom-52.jpg
%{_datadir}/mdk/backgrounds/flavor_of_freedom-53.jpg
%{_datadir}/mdk/backgrounds/flavor_of_freedom-54.jpg
%{_datadir}/mdk/backgrounds/flavor_of_freedom-55.jpg
%{_datadir}/mdk/backgrounds/flavor_of_freedom-56.jpg
%{_datadir}/mdk/backgrounds/flavor_of_freedom-57.jpg
%{_datadir}/mdk/backgrounds/flavor_of_freedom-58.jpg
%{_datadir}/mdk/backgrounds/flavor_of_freedom-59.jpg
%{_datadir}/mdk/backgrounds/flavor_of_freedom-60.jpg
%{_datadir}/mdk/backgrounds/flavor_of_freedom-61.jpg
%{_datadir}/mdk/backgrounds/flavor_of_freedom-62.jpg
%{_datadir}/mdk/backgrounds/flavor_of_freedom-63.jpg
%{_datadir}/mdk/backgrounds/flavor_of_freedom-64.jpg
%{_datadir}/mdk/backgrounds/flavor_of_freedom-65.jpg
%{_datadir}/mdk/backgrounds/flavor_of_freedom-66.jpg
%{_datadir}/mdk/backgrounds/flavor_of_freedom-67.jpg
%{_datadir}/mdk/backgrounds/flavor_of_freedom-68.jpg
%{_datadir}/mdk/backgrounds/flavor_of_freedom-69.jpg
%{_datadir}/mdk/backgrounds/flavor_of_freedom-70.jpg
%{_datadir}/mdk/backgrounds/flavor_of_freedom-71.jpg
%{_datadir}/mdk/backgrounds/flavor_of_freedom-72.jpg
%{_datadir}/mdk/backgrounds/flavor_of_freedom-73.jpg
%{_datadir}/mdk/backgrounds/flavor_of_freedom-74.jpg
%{_datadir}/mdk/backgrounds/flavor_of_freedom-75.jpg
%{_datadir}/mdk/backgrounds/flavor_of_freedom-76.jpg

%files screensaver
%dir %{_datadir}/mdk/screensaver
%{_datadir}/mdk/screensaver/*-*.*g

%theme_files OpenMandriva
%theme_files Moondrake
