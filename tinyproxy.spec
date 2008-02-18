Name:           tinyproxy
Version:        1.6.3
Release:        %mkrel 4
Epoch:          0
Summary:        Lightweight, non-caching, optionally anonymizing HTTP proxy
License:        GPL
URL:            http://tinyproxy.sourceforge.net/
Source0:        http://mesh.dl.sourceforge.net/sourceforge/tinyproxy/tinyproxy-%{version}.tar.gz
Source1:        %{name}.init
Patch0:         %{name}-makefile.patch
Group:          System/Servers
Requires(post): rpm-helper
Requires(preun): rpm-helper
Provides:	webproxy
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root

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
%{serverbuild}
%{_bindir}/autoreconf -i -v -f
%{configure2_5x} --enable-xtinyproxy \
                 --enable-filter \
                 --enable-tunnel \
                 --enable-upstream \
                 --with-config=%{_sysconfdir}/tinyproxy \
                 --with-stathost=localhost \
                 --program-prefix=""
%{make}

%install
%{__rm} -rf %{buildroot}
%{__mkdir_p} %{buildroot}%{_sysconfdir}/tinyproxy
%{__mkdir_p} %{buildroot}%{_sysconfdir}/sysconfig
%{__mkdir_p} %{buildroot}%{_initrddir}

%{makeinstall} bindir=%{buildroot}%{_sbindir}

%{__cp} -a doc/tinyproxy.conf %{buildroot}%{_sysconfdir}/tinyproxy/tinyproxy.conf
/bin/touch %{buildroot}%{_sysconfdir}/tinyproxy/filter

%{__cp} -a %{SOURCE1} %{buildroot}%{_initrddir}/tinyproxy
/bin/echo "FLAGS=\" -c /etc/tinyproxy/tinyproxy.conf\"" > %{buildroot}%{_sysconfdir}/sysconfig/tinyproxy

%clean
%{__rm} -rf %{buildroot}

%post
%_post_service tinyproxy

%preun
%_preun_service tinyproxy

%files
%defattr(0644,root,root,0755)
%doc doc/{HTTP_ERROR_CODES,RFC_INFO,report.sh,tinyproxy.conf,filter-howto.txt}
%doc AUTHORS COPYING ChangeLog INSTALL NEWS README TODO 
%attr(0755,root,root) %{_sbindir}/tinyproxy
%{_mandir}/man8/tinyproxy.8*
%{_datadir}/tinyproxy
%attr(0755,root,root) %{_initrddir}/tinyproxy
%config(noreplace) %{_sysconfdir}/sysconfig/tinyproxy
%dir %{_sysconfdir}/tinyproxy
%config(noreplace) %{_sysconfdir}/tinyproxy/tinyproxy.conf
%config(noreplace) %{_sysconfdir}/tinyproxy/filter
