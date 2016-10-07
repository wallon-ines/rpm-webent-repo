Summary: Security module for the Apache HTTP Server
Name: mod_security 
Version: 2.9.1
Release: 1%{?dist}
License: GPLv2
URL: http://www.modsecurity.org/
Group: System Environment/Daemons
Source: http://www.modsecurity.org/download/modsecurity-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires: libxml2 pcre httpd httpd-mmn = %([ -a %{_includedir}/httpd/.mmn ] && cat %{_includedir}/httpd/.mmn || echo missing)
BuildRequires: httpd-devel libxml2-devel pcre-devel

%description
ModSecurity is an open source intrusion detection and prevention engine
for web applications. It operates embedded into the web server, acting
as a powerful umbrella - shielding web applications from attacks.

%prep

%setup -n modsecurity-%{version}

%configure

#make -C apache2 CFLAGS="%{optflags}" top_dir="%{_libdir}/httpd"
make CFLAGS="%{optflags}" top_dir="%{_libdir}/httpd"
#perl -pi.orig -e 's|LIBDIR|%{_libdir}|;' %{SOURCE1}


%install
rm -rf %{buildroot}
install -D -m755 apache2/.libs/mod_security2.so %{buildroot}/%{_libdir}/httpd/modules/mod_security2.so
install -D -m644 modsecurity.conf-recommended %{buildroot}/%{_sysconfdir}/httpd/conf.d/mod_security.conf
install -d %{buildroot}/%{_sysconfdir}/httpd/modsecurity.d/

sed -i '1s;^;LoadModule %{_libdir}/httpd/modules/mod_security2.so\n;' %{buildroot}/%{_sysconfdir}/httpd/conf.d/mod_security.conf

echo -e "#Include modsecurity.d directory 
IncludeOptional %{_sysconfdir}/httpd/modsecurity.d/*.conf" >> %{buildroot}/%{_sysconfdir}/httpd/conf.d/mod_security.conf

#install -d %{buildroot}/%{_sysconfdir}/httpd/modsecurity.d/optional_rules/
#cp -r rules/*.conf %{buildroot}/%{_sysconfdir}/httpd/modsecurity.d/
#cp -r rules/optional_rules/*.conf %{buildroot}/%{_sysconfdir}/httpd/modsecurity.d/optional_rules/
#install -D -m644 %{SOURCE2} %{buildroot}/%{_sysconfdir}/httpd/modsecurity.d/modsecurity_localrules.conf

%clean
rm -rf %{buildroot}

%files
%defattr (-,root,root)
%doc CHANGES LICENSE README.* modsecurity* doc
%{_libdir}/httpd/modules/mod_security2.so
%config(noreplace) %{_sysconfdir}/httpd/conf.d/mod_security.conf
%dir %{_sysconfdir}/httpd/modsecurity.d
