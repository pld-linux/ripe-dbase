# TODO:
# - make logrotate file
# - remove stupid scripts from package
# - rename configs and move examples to docs
# - restore functionality of scripts from original package
Summary:	RIPE Whois Server
Summary(pl.UTF-8):	Serwer RIPE Whois
Name:		ripe-dbase
Version:	3.2.0
Release:	0.4
License:	distributable (see COPYING)
Group:		Applications/Networking
Source0:	ftp://ftp.ripe.net/ripe/dbase/software/%{name}-%{version}.tar.gz
# Source0-md5:	67c7cde734017727e091dba7084f18fd
Source1:	%{name}.init
Source2:	%{name}.sysconfig
Patch0:		%{name}-DESTDIR.patch
Patch1:		%{name}-ac_fixes.patch
Patch2:		%{name}-logdir.patch
URL:		http://www.ripe.net/ripencc/pub-services/db/reimp/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	glib-devel
BuildRequires:	gnupg
BuildRequires:	imap-static
BuildRequires:	libxml2-devel
BuildRequires:	libxslt-devel
BuildRequires:	mysql-client
BuildRequires:	mysql-devel
BuildRequires:	openssl-devel >= 0.9.6m
BuildRequires:	pam-devel
BuildRequires:	perl-devel
BuildRequires:	sed >= 4.0
BuildRequires:	zlib-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_confdir	/etc/%{name}

%description
The server software of the RIPE Whois Server, also known as the RPSL
Implementation Project (RIP).

%description -l pl.UTF-8
Oprogramowanie serwerowe serwera RIPE Whois, znane także jako RPSL
Implementation Project (RIP).

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
# RIPE variant
cp -f defs/variants/RIPE/*.xml defs
cp -f defs/variants/RIPE/*.h defs
cp -f defs/variants/RIPE/Makefile.syntax defs
cp -f defs/variants/RIPE/*.def include

sed -i -e 's#c-client.a#libc-client.so#g' configure*
sed -i -e 's#$(CCLIENTLIBDIR)/c-client.a#$(CCLIENTLIBDIR)/libc-client.a#g' Makefile*

%{__autoconf}
%{__aclocal}
%configure \
	--with-config-dir=%{_confdir} \
	--with-gpgcmd=%{_bindir}/gpg \
	--with-glibconfig=%{_bindir}/glib-config \
	--with-mysqlinc=%{_includedir}/mysql \
	--with-mysqllib=%{_libdir} \
	--with-mysqlbin=%{_bindir} \
	--with-xsltconfig=%{_bindir}/xslt-config \
	--with-xmlconfig=%{_bindir}/xml2-config \
	--with-cclientinc=%{_includedir}/imap \
	--with-cclientlib=%{_libdir}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/etc/{rc.d/init.d,sysconfig}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/%{name}
install %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/%{name}

# Remove junk replaced by things provided with spec:
rm -f $RPM_BUILD_ROOT%{_datadir}/ripe/scripts/whoisd.server

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README* UPDATE* COPYING RELEASE* doc/[!M]* modules/MODULES
%attr(751,root,root) %dir %{_confdir}
%attr(640,root,root) %config(noreplace) %{_confdir}/*
%attr(640,root,root) %config(noreplace) /etc/sysconfig/%{name}
%attr(755,root,root) %{_bindir}/*
%attr(754,root,root) /etc/rc.d/init.d/%{name}
# Everything from that place should be in %docs. Not needed
%dir %{_datadir}/ripe
%dir %{_datadir}/ripe/scripts
%dir %{_datadir}/ripe/scripts/SQL
%{_datadir}/ripe/scripts/SQL/*
%attr(755,root,root) %{_datadir}/ripe/scripts/*.sh
%attr(755,root,root) %{_datadir}/ripe/scripts/make_db
%attr(755,root,root) %{_datadir}/ripe/scripts/ripe2rpsl
%dir %{_libdir}/ripe
%dir %{_libdir}/ripe/utils
%attr(755,root,root) %{_libdir}/ripe/utils/*

%dir /var/log/ripe
%dir /var/log/ripe/*
