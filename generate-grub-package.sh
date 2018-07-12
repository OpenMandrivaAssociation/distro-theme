#!/bin/sh
VENDOR="$1"
vendor="$(echo ${VENDOR} | tr A-Z a-z)"

cat <<EOF
%if %{with grub}
%package	${VENDOR}-grub2
Summary:	Provides a graphical theme with a custom ${VENDOR} background for grub2
Group:		Graphics
Conflicts:	distro-theme-${VENDOR} < 1.4.29-2
Requires:	grub2
Requires(post,postun): chkconfig
Requires(post):	grub2
Requires(post):	sed
Provides:	grub2-theme = %{EVRD}
%rename	grub2-${vendor}-theme 2.00-38

%description	${VENDOR}-grub2
This package provides a custom ${VENDOR} graphical theme.

%%post ${VENDOR}-grub2
if [ \$1 -ge 1 ] ; then
	if [ -f %{_sysconfdir}/sysconfig/bootsplash ]; then
		sed -e 's/^\\s*SPLASH=.*/SPLASH=auto/' -e 's/^\\s*THEME=.*/THEME=${VENDOR}/' -i %{_sysconfdir}/sysconfig/bootsplash
	fi
fi
if test -f %{_sysconfdir}/default/grub ; then
	. %{_sysconfdir}/default/grub
	if [ "x\${GRUB_DISABLE_VENDOR_CONF}" = "x" ] || [ "x\${GRUB_DISABLE_VENDOR_CONF}" = "xfalse" ]; then
		sed -e '/GRUB_DISTRIBUTOR/d' -e '/GRUB_THEME/d' -e '/GRUB_BACKGROUND/d' -i %{_sysconfdir}/default/grub
		if [ "x\${GRUB_DISABLE_VENDOR_CONF}" = "x" ]; then
			echo -e "\n" >> %{_sysconfdir}/default/grub
			echo "GRUB_DISABLE_VENDOR_CONF=false" >> %{_sysconfdir}/default/grub
		fi
	fi
fi

update-alternatives --install %{_sysconfdir}/default/grub.vendor grub.vendor %{_sysconfdir}/default/grub.${VENDOR} 10

%%postun	${VENDOR}-grub2
if [ "\$1" = "0" ]; then
	update-alternatives --remove grub.vendor %{_sysconfdir}/default/grub.${VENDOR}
fi

%files ${VENDOR}-grub2
%dir /boot/grub2/themes/${VENDOR}
/boot/grub2/themes/${VENDOR}/*
%{_sysconfdir}/default/grub.${VENDOR}
%endif
EOF
