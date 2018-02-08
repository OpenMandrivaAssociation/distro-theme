VENDOR="$1"
FILES="$2"

cat <<EOF
%package	$1-screensaver
Summary:	$1 screensaver
Group:		Graphics
%rename		distro-theme-screensaver
%rename		mandriva-theme-Free-screensaver
%rename		mandriva-theme-Powerpack-screensaver
%rename		mandriva-theme-One-screensaver
%rename		mandriva-theme-Flash-screensaver
%rename		mandriva-theme-Rosa-screensaver
%rename		mandriva-screensaver
%rename		mandriva-theme-screensaver

%description	$1-screensaver
This package contains the $1 screensaver.

%files $1-screensaver
%dir %{_datadir}/mdk/screensaver
EOF
for i in $2; do
	echo %{_datadir}/mdk/screensaver/$i
done
