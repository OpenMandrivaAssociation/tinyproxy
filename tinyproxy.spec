%define name tinyproxy
%define their_version 1.6.3
%define release 2mdk

Name: %{name}
Version: 1.6.3
Release: %{release}
Summary: A lightweight, non-caching, optionally anonymizing http proxy
License: GPL
Source0: http://prdownloads.sourceforge.net/tinyproxy/%{name}-%{their_version}.tar.bz2
Source1: %{name}.init
Patch:	%name-makefile.patch.bz2
Group: System/Servers
Url:        http://tinyproxy.sourceforge.net
BuildRoot:  %{_tmppath}/%{name}-%{version}-root
PreReq: rpm-helper

%description
An anonymizing http proxy which is very light on system resources,
ideal for smaller networks and similar situations where other proxies
(such as Squid) may be overkill and/or a security risk. Tinyproxy can
also be configured to anonymize http requests (allowing for exceptions
on a per-header basis).

%prep
%setup -q

%patch0 -p1

%build
%serverbuild
rm -f Makefile
aclocal
automake -a
autoconf
%configure --enable-xtinyproxy --enable-filter \
	--enable-tunnel  --enable-upstream \
	--with-config=%{_sysconfdir}/tinyproxy  --with-stathost=localhost \
	--program-prefix=""

%make

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p  $RPM_BUILD_ROOT/%{_sysconfdir}/tinyproxy
mkdir -p  $RPM_BUILD_ROOT/%{_sysconfdir}/sysconfig
mkdir -p  $RPM_BUILD_ROOT/%{_initrddir}

%makeinstall bindir=$RPM_BUILD_ROOT/%{_sbindir}


install -m 644 doc/%{name}.conf $RPM_BUILD_ROOT/%{_sysconfdir}/tinyproxy/
touch $RPM_BUILD_ROOT/%{_sysconfdir}/tinyproxy/filter

install -m 755 %{SOURCE1} $RPM_BUILD_ROOT/%{_initrddir}/tinyproxy
echo "FLAGS=\" -c /etc/tinyproxy/tinyproxy.conf\"" > $RPM_BUILD_ROOT/%{_sysconfdir}/sysconfig/tinyproxy

%clean
[ -n "$RPM_BUILD_ROOT" -a "$RPM_BUILD_ROOT" != / ] && rm -rf $RPM_BUILD_ROOT

%post
%_post_service tinyproxy

%preun
%_preun_service tinyproxy

%files
%defattr(-,root,root)
%doc doc/{HTTP_ERROR_CODES,RFC_INFO,report.sh,tinyproxy.conf,filter-howto.txt}
%doc AUTHORS COPYING ChangeLog INSTALL NEWS README TODO 
%{_sbindir}/%{name}
%{_mandir}/man8/*
%dir %{_sysconfdir}/%{name}
%{_datadir}/%{name}
%config(noreplace) %{_sysconfdir}/sysconfig/tinyproxy
%config(noreplace) %{_sysconfdir}/tinyproxy/tinyproxy.conf
%config(noreplace) %{_sysconfdir}/tinyproxy/filter
%config(noreplace) %{_initrddir}/tinyproxy
