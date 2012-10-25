Summary:	Lightweight, non-caching, optionally anonymizing HTTP proxy
Name:		tinyproxy
Version:	1.8.3
%define subrel	1
Release:	%mkrel 1
Group:		System/Servers
# License bundled is gpl v3, but source code say gpl v2 or later
License:	GPLv2+
URL:		https://www.banu.com/%{name}/
Source0:	https://www.banu.com/pub/%{name}/1.8/%{name}-%{version}.tar.bz2
Source1:	tinyproxy.init
Patch0:		tinyproxy-CVE-2012-3505-randomized-hashmaps.patch
Patch1:		tinyproxy-CVE-2012-3505-limit-headers.patch
BuildRequires:	asciidoc
BuildRequires:	xsltproc
BuildRequires:  docbook-style-xsl
BuildRequires:  docbook-dtd45-xml
Requires(post): rpm-helper
Requires(preun): rpm-helper

%description
An anonymizing http proxy which is very light on system resources, ideal for
smaller networks and similar situations where other proxies (such as Squid) may
be overkill and/or a security risk. Tinyproxy can also be configured to
anonymize http requests (allowing for exceptions on a per-header basis).

%prep

%setup -q
%patch0 -p1 -b .randomized-hashmaps
%patch1 -p1 -b .limit-headers

cp %{SOURCE1} tinyproxy.init

%build
%serverbuild

%configure2_5x \
    --enable-xtinyproxy \
    --enable-filter \
    --enable-upstream \
    --enable-transparent \
    --enable-reverse \
    --sysconfdir=%{_sysconfdir}/tinyproxy \
    --with-stathost=localhost \
    --program-prefix=""

%make

%install
%__rm -rf %{buildroot}

%__install -d %{buildroot}%{_sysconfdir}/tinyproxy
%__install -d %{buildroot}%{_sysconfdir}/logrotate.d
%__install -d %{buildroot}%{_sysconfdir}/sysconfig
%__install -d %{buildroot}%{_initrddir}

%__install -d %{buildroot}%{_logdir}/tinyproxy
%__install -d %{buildroot}%{_var}/run/tinyproxy

%makeinstall bindir=%{buildroot}%{_sbindir}

mv %{buildroot}%{_sysconfdir}/tinyproxy.conf %{buildroot}%{_sysconfdir}/tinyproxy/tinyproxy.conf
/bin/touch %{buildroot}%{_sysconfdir}/tinyproxy/filter

%__install -m0755 tinyproxy.init %{buildroot}%{_initrddir}/tinyproxy

/bin/echo "FLAGS=\" -c /etc/tinyproxy/tinyproxy.conf\"" > %{buildroot}%{_sysconfdir}/sysconfig/tinyproxy

cat > %{buildroot}%{_sysconfdir}/logrotate.d/tinyproxy <<EOF
/var/log/tinyproxy.log {
    rotate 7
    daily
    compress
    missingok
    postrotate
    if [ -f /var/run/tinyproxy.pid ]; then
       /etc/init.d/tinyproxy restart > /dev/null
    fi
    endscript
}
EOF

%post
%_post_service tinyproxy

%preun
%_preun_service tinyproxy


%files
%doc docs/*.txt
%doc AUTHORS COPYING ChangeLog INSTALL NEWS README TODO 
%attr(0755,root,root) %{_sbindir}/tinyproxy
%attr(0755,root,root) %{_initrddir}/tinyproxy
%config(noreplace) %{_sysconfdir}/sysconfig/tinyproxy
%config(noreplace) %{_sysconfdir}/logrotate.d/tinyproxy
%dir %{_sysconfdir}/tinyproxy
%config(noreplace) %{_sysconfdir}/tinyproxy/tinyproxy.conf
%config(noreplace) %{_sysconfdir}/tinyproxy/filter
%{_logdir}/tinyproxy/
%{_var}/run/tinyproxy/
%{_mandir}/man8/tinyproxy.8*
%{_mandir}/man5/*
%{_datadir}/tinyproxy




%changelog

* Wed Oct 24 2012 luigiwalser <luigiwalser> 1.8.3-1.1.mga2
+ Revision: 309740
- add patches from debian to fix CVE-2012-3505

  + misc <misc>
    - fix initscript keyword ( rpmlint rejection)
    - upgrade to newer version 1.8.3
    - remove ndded part of the spec file
    - place each BuildRequires on a line ( easier to spot change )
    - remove provides on webproxy ( not required anywhere, and provides
      are not mean to be used for categorization )
    - remove Epoch 0 ( breaking upgrade path, but we do not plan to support
      upgrade from 2010.2 or 2011 to mageia 2 )
    - imported package tinyproxy

