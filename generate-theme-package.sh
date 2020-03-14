#!/bin/sh
VENDOR="$1"
DISTRIBUTION="$2"
BG_RATIO="$3"
BG_RES="$4"
OPAQUE="$5"

vendor="$(echo ${VENDOR} |tr A-Z a-z)"
cat <<EOF
%package 	${VENDOR}
Summary:	${DISTRIBUTION} theme for plymouth and desktop background
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
%if "%product_product" == "OpenMandriva"
%if %{with grub}
Requires:	distro-theme-OpenMandriva-grub2
%endif
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

%description ${VENDOR}
This package contains the ${VENDOR} plymouth theme
with its images and configuration for different resolution as well as
the the desktop background image.

%post ${VENDOR}
if [ -z "\$DURING_INSTALL" ]; then
	if [ -x %{scriptdir}/switch-themes ]; then
		%{scriptdir}/switch-themes ${VENDOR}
	fi
else
	%{_sbindir}/plymouth-set-default-theme ${VENDOR}
fi

if [ -f %{mdk_bg}/${VENDOR}-root.png -a ! -f %{mdk_bg}/root/default.png -o -L %{mdk_bg}/root/default.png ]; then
	rm -f %{mdk_bg}/root/default.png
	ln -s ${VENDOR}-root-1600x1200.png %{mdk_bg}/root/default.png
fi
EOF

if [ -n "$BG_RES" ]; then
	cat <<EOF
if [ -f %{mdk_bg}/${VENDOR}-${BG_RES}.jpg -a ! -f %{mdk_bg}/default.jpg -o -L %{mdk_bg}/default.jpg ]; then
	rm -f %{mdk_bg}/default.jpg
	ln -s ${VENDOR}-${BG_RES}.png %{mdk_bg}/default.jpg
fi

if [ -f %{mdk_bg}/${VENDOR}-${BG_RES}.png -a ! -f %{mdk_bg}/default.png -o -L %{mdk_bg}/default.png ]; then
	rm -f %{mdk_bg}/default.png
	ln -s ${VENDOR}-${BG_RES}.png %{mdk_bg}/default.png
fi
EOF
fi

if [ -n "$BG_RATIO" ]; then
	cat <<EOF
if [ -f %{mdk_bg}/${VENDOR}-${BG_RATIO}.png -a ! -f %{mdk_bg}/default.png -o -L %{mdk_bg}/default.png ]; then
	rm -f %{mdk_bg}/default.png
	ln -s ${VENDOR}-${BG_RATIO}.png %{mdk_bg}/default.png
fi
if [ -f %{mdk_bg}/${VENDOR}-${BG_RATIO}.jpg -a ! -f %{mdk_bg}/default.jpg -o -L %{mdk_bg}/default.jpg ]; then
	rm -f %{mdk_bg}/default.jpg
	ln -s ${VENDOR}-${BG_RATIO}.png %{mdk_bg}/default.jpg
fi
EOF
fi


cat <<EOF
%triggerpostun -n %{name}-${VENDOR} -- mandriva-theme-${VENDOR} < 1.2.4
for f in kdeglobals konsolerc; do
	if [ "\`readlink /usr/share/config/\$f 2>/dev/null\`" == "\$f-${VENDOR}" ]; then
		rm -f /usr/share/config/\$f
	fi
done


%preun ${VENDOR}
if [ "\$1" == "0" ]; then
	if [ -x %{scriptdir}/remove-theme ]; then
		%{scriptdir}/remove-theme ${VENDOR}
	fi
	link=\`readlink %{mdk_bg}/default.png\`
	slink=\${link%%-*}
	if [ "\$slink" == "${VENDOR}" ]; then
		rm -f %{mdk_bg}/default.png;
	fi
	link=\`readlink %{mdk_bg}/default.jpg\`
	slink=\${link%%-*}
	if [ "\$slink" == "${VENDOR}" ]; then
		rm -f %{mdk_bg}/default.jpg
	fi
	link=\`readlink %{mdk_bg}/${VENDOR}.png\`
	slink=\${link%%-*}
	if [ "\$slink" == "${VENDOR}" ]; then
		rm -f %{mdk_bg}/${VENDOR}.png
	fi
	link=\`readlink %{mdk_bg}/"${VENDOR}".jpg\`
	slink=\${link%%-*}
	if [ "\$slink" == "${VENDOR}" ]; then
		rm -f %{mdk_bg}/${VENDOR}.jpg
	fi
	link=\`readlink %{mdk_bg}/root/${VENDOR}.png\`
	slink=\${link%%-*}
	if [ "\$slink" == "${VENDOR}-root" ]; then
		rm -f %{mdk_bg}/root/default.png
	fi
fi
EOF

[ -n "$OPAQUE" ] && echo "%exclude %{mdk_bg}/${OPAQUE}"

if [ -n "${OPAQUE}" ]; then
	# this isn't the niftiest, but if anyone else wants to add any similar,
	# vendor specific stuff, feel free to provide this with a more generic
	# package & file name...
	cat <<EOF
%package        ${VENDOR}-opaque-background
Summary:        Opaque background for ${VENDOR}
Group:          Graphics
Provides:       %{name}-opaque-background = %{EVRD}
Requires(post,postun):  update-alternatives
Conflicts:      %{name} < 1.4.31-2

%description    ${VENDOR}-opaque-background
Opaque version of splash background for use with SimpleWelcome (rosa-starter).


%post ${VENDOR}-opaque-background
update-alternatives --install %{mdk_bg}/default-opaque.png default-opaque-png %{mdk_bg}/${OPAQUE} 10

%postun ${VENDOR}-opaque-background
if [ "\$1" = "0" ]; then
        update-alternatives --remove default-opaque.png %{mdk_bg}/${OPAQUE}
fi

%files ${VENDOR}-opaque-background
%{mdk_bg}/${OPAQUE}
EOF
fi

# Let's put %%files last so extras can be added in the spec...
cat <<EOF
%files ${VENDOR}
%{_datadir}/plymouth/themes/${VENDOR}
%optional %{_datadir}/gfxboot/themes/${VENDOR}
%{mdk_bg}/${VENDOR}*
%optional %{_datadir}/pixmaps/system-logo-white.png
EOF

