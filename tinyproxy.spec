Summary:	Lightweight, non-caching, optionally anonymizing HTTP proxy
Name:		tinyproxy
Version:	1.6.4
Release:	%mkrel 3
Group:		System/Servers
# License bundled is gpl v3, but source code say gpl v2 or later
License:	GPLv2+
URL:		https://www.banu.com/%{name}/
Source0:	https://www.banu.com/pub/%{name}/1.6/%{name}-%{version}.tar.gz
Source1:	tinyproxy.init
Patch0:		tinyproxy-makefile.patch
Requires(post): rpm-helper
Requires(preun): rpm-helper
BuildRequires:   devel(libsocks)   
Provides:	webproxy
Epoch:		0
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
An anonymizing http proxy which is very light on system resources, ideal for
smaller networks and similar situations where other proxies (such as Squid) may
be overkill and/or a security risk. Tinyproxy can also be configured to
anonymize http requests (allowing for exceptions on a per-header basis).

%prep

%setup -q
%patch0 -p0

cp %{SOURCE1} tinyproxy.init

%build
%serverbuild
autoreconf -fis

%configure2_5x \
    --enable-xtinyproxy \
    --enable-socks \
    --enable-filter \
    --enable-tunnel \
    --enable-upstream \
    --enable-transparent-proxy \
    --with-config=%{_sysconfdir}/tinyproxy \
    --with-stathost=localhost \
    --program-prefix=""

%make

%install
rm -rf %{buildroot}

install -d %{buildroot}%{_sysconfdir}/tinyproxy
install -d %{buildroot}%{_sysconfdir}/sysconfig
install -d %{buildroot}%{_initrddir}

%makeinstall bindir=%{buildroot}%{_sbindir}

cp -a doc/tinyproxy.conf %{buildroot}%{_sysconfdir}/tinyproxy/tinyproxy.conf
/bin/touch %{buildroot}%{_sysconfdir}/tinyproxy/filter

install -m0755 tinyproxy.init %{buildroot}%{_initrddir}/tinyproxy

/bin/echo "FLAGS=\" -c /etc/tinyproxy/tinyproxy.conf\"" > %{buildroot}%{_sysconfdir}/sysconfig/tinyproxy

%post
%_post_service tinyproxy

%preun
%_preun_service tinyproxy

%clean
rm -rf %{buildroot}

%files
%defattr(0644,root,root,0755)
%doc doc/{HTTP_ERROR_CODES,RFC_INFO,report.sh,tinyproxy.conf,filter-howto.txt}
%doc AUTHORS COPYING ChangeLog INSTALL NEWS README TODO 
%attr(0755,root,root) %{_sbindir}/tinyproxy
%attr(0755,root,root) %{_initrddir}/tinyproxy
%config(noreplace) %{_sysconfdir}/sysconfig/tinyproxy
%dir %{_sysconfdir}/tinyproxy
%config(noreplace) %{_sysconfdir}/tinyproxy/tinyproxy.conf
%config(noreplace) %{_sysconfdir}/tinyproxy/filter
%{_mandir}/man8/tinyproxy.8*
%{_datadir}/tinyproxy
