Summary:	RIPE Whois Server
Summary(pl):	Serwer RIPE Whois
Name:		ripe-dbase
Version:	3.2.0
Release:	0.2
License:	distributable
Group:		Applications/Networking
Source0:	ftp://ftp.ripe.net/ripe/dbase/software/%{name}-%{version}.tar.gz
# Source0-md5:	67c7cde734017727e091dba7084f18fd
BuildRequires:	glib-devel
BuildRequires:	gnupg
BuildRequires:	imap-static
BuildRequires:	libxml2-devel
BuildRequires:	libxslt-devel
BuildRequires:	mysql-client
BuildRequires:	mysql-devel
BuildRequires:	openssl-devel >= 0.9.7d
BuildRequires:	pam-devel
BuildRequires:	perl-devel
BuildRequires:	sed >= 4.0
BuildRequires:	zlib-devel
URL:		http://www.ripe.net/ripencc/pub-services/db/reimp/
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The server software of the RIPE Whois Server, also known as the RPSL
Implementation Project (RIP).

The RIPE version of the whois client program.

%description -l pl
Oprogramowanie serwerowe serwera RIPE Whois, znane tak¿e jako RPSL
Implementation Project (RIP).

Wersja RIPE programu klienckiego whois.

%prep
%setup -q

%build

# RIPE variant
cp -f defs/variants/RIPE/*.xml defs
cp -f defs/variants/RIPE/*.h defs
cp -f defs/variants/RIPE/Makefile.syntax defs
cp -f defs/variants/RIPE/*.def include

sed -i -e 's#c-client.a#libc-client.so#g' configure*
sed -i -e 's#$(CCLIENTLIBDIR)/c-client.a#$(CCLIENTLIBDIR)/libc-client.a#g' Makefile*

%configure \
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
install -d $RPM_BUILD_ROOT%{_bindir}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	prefix=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README* UPDATE* COPYING RELEASE*
#%attr(755,root,root) %{_bindir}/*
