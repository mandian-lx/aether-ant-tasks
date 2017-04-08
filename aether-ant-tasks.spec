%{?_javapackages_macros:%_javapackages_macros}
%global vertag v20141111

Name:           aether-ant-tasks
Epoch:          1
Version:        1.0.1
Release:        6%{?dist}
Summary:        Ant tasks using Aether to resolve, install and deploy artifacts
Group:          Development/Java
BuildArch:      noarch

License:        EPL
URL:            http://www.eclipse.org/aether
Source0:        http://git.eclipse.org/c/aether/aether-ant.git/snapshot/%{name}-%{version}.%{vertag}.tar.bz2
Source5:        ant-classpath

# Partially forwarded upstream: http://bugs.eclipse.org/470696
Patch0001:      0001-Compatibility-with-Maven-3.4.0.patch
Patch0002:      0002-Add-support-for-XMvn-workspace-reader.patch

BuildRequires:  maven-local
BuildRequires:  mvn(junit:junit)
BuildRequires:  mvn(org.apache.ant:ant)
BuildRequires:  mvn(org.apache.ant:ant-launcher)
BuildRequires:  mvn(org.apache.ant:ant-testutil)
BuildRequires:  mvn(org.apache.maven:maven-aether-provider) >= 3.1.0
BuildRequires:  mvn(org.apache.maven:maven-settings-builder)
BuildRequires:  mvn(org.codehaus.plexus:plexus-component-annotations)
BuildRequires:  mvn(org.codehaus.plexus:plexus-interpolation)
BuildRequires:  mvn(org.eclipse.aether:aether-api)
BuildRequires:  mvn(org.eclipse.aether:aether-connector-basic)
BuildRequires:  mvn(org.eclipse.aether:aether-impl)
BuildRequires:  mvn(org.eclipse.aether:aether-test-util)
BuildRequires:  mvn(org.eclipse.aether:aether-transport-classpath)
BuildRequires:  mvn(org.eclipse.aether:aether-transport-file)
BuildRequires:  mvn(org.eclipse.aether:aether-transport-http)
BuildRequires:  mvn(org.eclipse.aether:aether-util)
BuildRequires:  mvn(org.eclipse.sisu:org.eclipse.sisu.plexus)
BuildRequires:  mvn(org.hamcrest:hamcrest-core)
BuildRequires:  mvn(org.hamcrest:hamcrest-library)
BuildRequires:  mvn(org.fedoraproject.xmvn:xmvn-api)
BuildRequires:  mvn(org.fedoraproject.xmvn:xmvn-launcher)
BuildRequires:  mvn(org.fedoraproject.xmvn:xmvn-connector-aether)

Requires:       ant
Requires:       xmvn-api
Requires:       xmvn-core
Requires:       xmvn-launcher
Requires:       xmvn-connector-aether

%description
The Aether Ant Tasks enable build scripts for Apache Ant 1.7+ to use Eclipse
Aether to resolve dependencies and install and deploy locally built artifacts.

%package javadoc
Summary:        Javadocs for %{name}
Group:          Documentation

%description javadoc
This package contains the API documentation for %{name}.

%prep
%setup -q -n %{name}-%{version}.%{vertag}
%patch0001 -p1
#patch0002 -p1

# Use junit since junit-dep is obselete and equivilent to junit since 4.11
sed -i -e 's@junit-dep@junit@g' pom.xml

%pom_remove_plugin ":maven-shade-plugin"
%pom_remove_plugin ":maven-enforcer-plugin"

%build
# Some tests require internet connectivity, so ignore failures
%mvn_build -- -Dmaven.test.failure.ignore=true

%install
%mvn_install

install -d -m 755 %{buildroot}/%{_sysconfdir}/ant.d
install -p -m 644 %{SOURCE5} %{buildroot}/%{_sysconfdir}/ant.d/%{name}

%files -f .mfiles
%config(noreplace) %{_sysconfdir}/ant.d/%{name}
%doc README.md
%doc epl-v10.html notice.html

%files javadoc -f .mfiles-javadoc
%doc epl-v10.html notice.html

%changelog
* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.0.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Oct 10 2016 Mikolaj Izdebski <mizdebsk@redhat.com> - 1:1.0.1-5
- Fix integration with XMvn

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.0.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Jul 14 2015 Mat Booth <mat.booth@redhat.com> - 1:1.0.1-3
- Fix broken localrepo task due to missing builder-support from ant classpath

* Tue Jun 16 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Feb  4 2015 Mikolaj Izdebski <mizdebsk@redhat.com> - 1:1.0.1-1
- Update to upstream version 1.0.1

* Fri Nov  7 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 1:1.0.0-3
- Update to Maven 3.2.3

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue May 20 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 1:1.0.0-1
- Update to upstream version 1.0.0

* Thu Feb 27 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 1:0.9.0-1
- Update to upstream version 0.9.0

* Tue Jan  7 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 1:0.9.0-0.4.M4
- Update to upstream version 0.9.0.M4
- Remove workaround for rhbz#996062

* Wed Sep 11 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 1:0.9.0-0.3.M3
- Add support for resulving artifacts using XMvn
- Resolves: rhbz#1005971

* Mon Aug 12 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 1:0.9.0-0.2.M3
- Update to upstream version 0.9.0.M3

* Mon Jul 29 2013 Mat Booth <fedora@matbooth.co.uk> - 1:0.9-0.1.SNAPSHOT
- Upstream has moved to Eclipse, update to upstream 0.9-SNAPSHOT
- Run tests now all deps are in Fedora
- Migrate to Eclipse Aether, fixes rhbz #985700

* Tue May 14 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.0-0.8.SNAPSHOT
- Add missing BR: maven-shade-plugin

* Tue May  7 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.0-0.7.SNAPSHOT
- Replace BR with mvn-style virtual packages
- Resolves: rhbz#958156

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-0.6.SNAPSHOT
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Feb 06 2013 Java SIG <java-devel@lists.fedoraproject.org> - 1.0-0.5.SNAPSHOT
- Update for https://fedoraproject.org/wiki/Fedora_19_Maven_Rebuild
- Replace maven BuildRequires with maven-local

* Wed Jan  9 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.0-0.4.SNAPSHOT
- Bump release tag

* Tue Jan  8 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.0-0.3.SNAPSHOT
- Build with xmvn

* Mon Sep 17 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.0-0.2.SNAPSHOT
- Install LICENSE files

* Mon Apr 30 2012 Mikolaj Izdebski <mizdebsk@redhat.com> 1.0-0.1.SNAPSHOT
- Initial packaging.
