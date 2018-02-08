#!/bin/sh
VENDOR="$1"
DISTRIBUTION="$2"
[ -z "${DISTRIBUTION}" ] && DISTRIBUTION="$VENDOR"

cat <<EOS
%if %{with grub}
install -d %{buildroot}%{_sysconfdir}/default/
cat > %{buildroot}%{_sysconfdir}/default/grub.${VENDOR} << EOF
GRUB_THEME=/boot/grub2/themes/${VENDOR}/theme.txt
GRUB_BACKGROUND=/boot/grub2/themes/${VENDOR}/terminal_background.png
GRUB_DISTRIBUTOR=\"${DISTRIBUTION}\"
%endif
EOF
EOS
