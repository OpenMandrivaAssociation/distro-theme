import sys,rpm

def theme_package(Vendor, distribution, files=None, bg_ratio=None, bg_res=None, opaque=None):
    vendor = Vendor.lower()
    print(rpm.expandMacro("""
%%package 	"""+Vendor+"""
Summary:	"""+distribution+""" theme for plymouth and desktop background
Group:		Graphics
Provides:	mandrake_theme mandrake-theme mandrakelinux-theme mandriva-theme = %{version}-%{release}
Provides:	distro-theme = %{EVRD}
Provides:	plymouth(system-theme)
Obsoletes:	mandrake_theme mandrake-theme mandrakelinux-theme distro-theme
Requires:	distro-theme-common
Requires:	plymouth-plugin-script
Suggests:	distro-theme-screensaver
Conflicts:	kdebase-konsole <= 1:3.4.2-37mdk
Conflicts:	grub2 < 2.00-23
Requires(post):	bootsplash >= 3.4.1-13
%if %product_product == "OpenMandriva"
Requires:	distro-theme-OpenMandriva-grub2
Requires:	distro-theme-OpenMandriva-screensaver
%endif
%ifarch x86_64 %{ix86}
Requires(post):	bootloader
%endif
%rename		mandriva-theme-Flash
%rename		mandriva-theme-Free
%rename		mandriva-theme-One
%rename		mandriva-theme-Powerpack
%rename		mandriva-theme-Moondrake
%rename		mandriva-theme-OpenMandriva

%%description """+Vendor+"""
This package contains the """+Vendor+""" plymouth theme
with its images and configuration for different resolution as well as
the the desktop background image.

%%post		"""+Vendor+"""
if [ -z "$DURING_INSTALL" ]; then
  if [ -x %{scriptdir}/switch-themes ]; then
    %{scriptdir}/switch-themes """+Vendor+"""
  fi
else
  %{_sbindir}/plymouth-set-default-theme """+Vendor+"""
fi

if [ -f %{mdk_bg}/"""+Vendor+"""-root.png -a ! -f %{mdk_bg}/root/default.png -o -L %{mdk_bg}/root/default.png ]; then
  rm -f %{mdk_bg}/root/default.png
  ln -s """+Vendor+"""-root-1600x1200.png %{mdk_bg}/root/default.png
fi"""))
    if bg_res:
	print(rpm.expandMacro("""
if [ -f %{mdk_bg}/"""+Vendor+"""-"""+bg_res+""".jpg -a ! -f %{mdk_bg}/default.jpg -o -L %{mdk_bg}/default.jpg ]; then
  rm -f %{mdk_bg}/default.jpg
  ln -s """+Vendor+"""-"""+bg_res+""".png %{mdk_bg}/default.jpg
fi

if [ -f %{mdk_bg}/"""+Vendor+"""-"""+bg_res+""".png -a ! -f %{mdk_bg}/default.png -o -L %{mdk_bg}/default.png ]; then
  rm -f %{mdk_bg}/default.png
  ln -s """+Vendor+"""-"""+bg_res+""".png %{mdk_bg}/default.png
fi"""))
    if bg_ratio:
	print(rpm.expandMacro("""
if [ -f %{mdk_bg}/"""+Vendor+"""-"""+bg_ratio+""".png -a ! -f %{mdk_bg}/default.png -o -L %{mdk_bg}/default.png ]; then
  rm -f %{mdk_bg}/default.png
  ln -s """+Vendor+"""-"""+bg_ratio+""".png %{mdk_bg}/default.png
fi
if [ -f %{mdk_bg}/"""+Vendor+"""-"""+bg_ratio+""".jpg -a ! -f %{mdk_bg}/default.jpg -o -L %{mdk_bg}/default.jpg ]; then
  rm -f %{mdk_bg}/default.jpg
  ln -s """+Vendor+"""-"""+bg_ratio+""".png %{mdk_bg}/default.jpg
fi"""))
    print(rpm.expandMacro("""
%triggerpostun -n %{name}-"""+Vendor+""" -- mandriva-theme-"""+Vendor+""" < 1.2.4
for f in kdeglobals konsolerc; do
  if [ "`readlink /usr/share/config/$f 2>/dev/null`" == \"$f-"""+Vendor+"""\" ]; then
    rm -f /usr/share/config/$f
  fi
done

%preun """+Vendor+"""
if [ "$1" == "0" ]; then
  if [ -x %{scriptdir}/remove-theme ]; then
    %{scriptdir}/remove-theme """+Vendor+"""
  fi
  link=`readlink %{mdk_bg}/default.png`
  slink=${link%%-*}
  if [ "$slink" == \""""+Vendor+"""\" ]; then
	rm -f %{mdk_bg}/default.png;
  fi
  link=`readlink %{mdk_bg}/default.jpg`
  slink=${link%%-*}
  if [ "$slink" == \""""+Vendor+"""\" ]; then
	rm -f %{mdk_bg}/default.jpg;
  fi
  link=`readlink %{mdk_bg}/"""+Vendor+""".png`
  slink=${link%%-*}
  if [ "$slink" == \""""+Vendor+"""\" ]; then
	rm -f %{mdk_bg}/"""+Vendor+""".png;
  fi
  link=`readlink %{mdk_bg}/"""+Vendor+""".jpg`
  slink=${link%%-*}
  if [ "$slink" == \""""+Vendor+"""\" ]; then
	rm -f %{mdk_bg}/"""+Vendor+""".jpg;
  fi
  link=`readlink %{mdk_bg}/root/"""+Vendor+""".png`
  slink=${link%%-*}
  if [ "$slink" == \""""+Vendor+"""-root" ]; then
	rm -f %{mdk_bg}/root/default.png;
  fi
fi

%files """+Vendor+"""
%{_datadir}/plymouth/themes/"""+Vendor+"""
%{_datadir}/gfxboot/themes/"""+Vendor+"""
%{mdk_bg}/"""+Vendor+"*"))
    if opaque:
        print rpm.expandMacro("""
%exclude %{mdk_bg}/"""+opaque)

    if type(files) == str:
        print(rpm.expandMacro(files))
    elif type(files) == tuple or type(files) == list:
	for filename in files:
	    print(rpm.expandMacro(filename))

    # this isn't the niftiest, but if anyone else wants to add any similar,
    # vendor specific stuff, feel free to provide this with a more generic
    # package & file name...
    if opaque:
        print(rpm.expandMacro("""
%package        """+Vendor+"""-opaque-background
Summary:        Opaque background for """+Vendor+"""
Group:          Graphics
Provides:       %{name}-opaque-background = %{EVRD}
Requires(post,postun):  update-alternatives
Conflicts:      %{name} < 1.4.31-2

%description    """+Vendor+"""-opaque-background
Opaque version of splash background for use with SimpleWelcome (rosa-starter).


%%post """+Vendor+"""-opaque-background
update-alternatives --install %{mdk_bg}/default-opaque.png default-opaque-png %{mdk_bg}/"""+opaque+""" 10

%%postun """+Vendor+"""-opaque-background
if [ "$1" = "0" ]; then
        update-alternatives --remove default-opaque.png %{mdk_bg}/"""+opaque+"""
fi

%files """+Vendor+"""-opaque-background
%{mdk_bg}/"""+opaque))


def screensaver_package(Vendor, files):
    print(rpm.expandMacro("""
%package	"""+Vendor+"""-screensaver
Summary:	"""+Vendor+""" screensaver
Group:		Graphics
%rename		distro-theme-screensaver
%rename		mandriva-theme-Free-screensaver
%rename		mandriva-theme-Powerpack-screensaver
%rename		mandriva-theme-One-screensaver
%rename		mandriva-theme-Flash-screensaver
%rename		mandriva-theme-Rosa-screensaver
%rename		mandriva-screensaver
%rename		mandriva-theme-screensaver

%description	"""+Vendor+"""-screensaver
This package contains the """+Vendor+""" screensaver.

%files """+Vendor+"""-screensaver
%dir %{_datadir}/mdk/screensaver"""))
    if type(files) == str:
        print rpm.expandMacro("%{_datadir}/mdk/screensaver/"+files)
    elif type(files) == tuple or type(files) == list:
	for filename in files:
	    print rpm.expandMacro("%{_datadir}/mdk/screensaver/"+filename)

def boot_theme(Vendor):
    vendor = Vendor.lower()
    print(rpm.expandMacro("""
%package	"""+Vendor+"""-grub2
Summary:	Provides a graphical theme with a custom """+Vendor+""" background for grub2
Group:		Graphics
Conflicts:	distro-theme-"""+Vendor+""" < 1.4.29-2
Requires:	grub2
Requires(post,postun): update-alternatives
Requires(post):	grub2
Requires(post):	sed
Provides:	grub2-theme = %{EVRD}
%rename	grub2-"""+vendor+"""-theme 2.00-38

%description	"""+Vendor+"""-grub2
This package provides a custom """+Vendor+""" graphical theme.

%%post		"""+Vendor+"""-grub2
if [ $1 -ge 1 ] ; then
 if [ -f %{_sysconfdir}/sysconfig/bootsplash ]; then
    sed -e 's/^\\s*SPLASH=.*/SPLASH=auto/' -e 's/^\\s*THEME=.*/THEME="""+Vendor+"""/' -i %{_sysconfdir}/sysconfig/bootsplash
 fi
fi
if test -f %{_sysconfdir}/default/grub ; then
  . %{_sysconfdir}/default/grub
  if [ "x${GRUB_DISABLE_VENDOR_CONF}" = "x" ] || [ "x${GRUB_DISABLE_VENDOR_CONF}" = "xfalse" ]; then
    sed -e '/GRUB_DISTRIBUTOR/d' -e '/GRUB_THEME/d' -e '/GRUB_BACKGROUND/d' -i %{_sysconfdir}/default/grub
    if [ "x${GRUB_DISABLE_VENDOR_CONF}" = "x" ]; then
      echo -e "\n" >> %{_sysconfdir}/default/grub
      echo "GRUB_DISABLE_VENDOR_CONF=false" >> %{_sysconfdir}/default/grub
    fi
  fi
fi

update-alternatives --install %{_sysconfdir}/default/grub.vendor grub.vendor %{_sysconfdir}/default/grub."""+Vendor+""" 10

%%postun	"""+Vendor+"""-grub2
if [ "$1" = "0" ]; then
update-alternatives --remove grub.vendor %{_sysconfdir}/default/grub."""+Vendor+"""
fi

%files """+Vendor+"""-grub2
%dir /boot/grub2/themes/"""+Vendor+"""
/boot/grub2/themes/"""+Vendor+"""/*
%{_sysconfdir}/default/grub."""+Vendor))

def grub2conf(Vendor, Distribution):
    print(rpm.expandMacro("""
install -d %{buildroot}%{_sysconfdir}/default/
cat > %{buildroot}%{_sysconfdir}/default/grub."""+Vendor+""" << EOF
GRUB_THEME=/boot/grub2/themes/"""+Vendor+"""/theme.txt
GRUB_BACKGROUND=/boot/grub2/themes/"""+Vendor+"""/terminal_background.png
GRUB_DISTRIBUTOR=\""""+Distribution+"""\"
EOF"""))


def extra_files(files=None, start=None, stop=None, strfmt=None, printOut=False):
    filelist = []
    if files:
        filelist.append(files)
    if start and stop and strfmt:
        for i in range(start, stop):
            f = rpm.expandMacro(strfmt) % i 
            if printOut:
                print(f)
            else:
                filelist.append(f)
    if not printOut:
        return filelist
