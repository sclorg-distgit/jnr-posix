%{?scl:%scl_package jnr-posix}
%{!?scl:%global pkg_name %{name}}
%{?java_common_find_provides_and_requires}

Name:           %{?scl_prefix}jnr-posix
Version:        3.0.14
Release:        2.2%{?dist}
Summary:        Java Posix layer
License:        CPL or GPLv2+ or LGPLv2+
URL:            http://github.com/jnr/jnr-posix
Source0:        https://github.com/jnr/%{name}/archive/%{version}.tar.gz
Patch0:		fix-manifest.patch

BuildRequires:  %{?scl_prefix_java_common}maven-local
BuildRequires:  %{?scl_prefix}mvn(com.github.jnr:jnr-constants) >= 0.8.8
BuildRequires:  %{?scl_prefix}mvn(com.github.jnr:jnr-ffi)
BuildRequires:  %{?scl_prefix_java_common}mvn(junit:junit)
BuildRequires:  %{?scl_prefix_maven}mvn(org.sonatype.oss:oss-parent:pom:)

BuildArch:      noarch

%description
jnr-posix is a lightweight cross-platform POSIX emulation layer for Java, 
written in Java and is part of the JNR project 

%package        javadoc
Summary:        Javadoc for %{pkg_name}

%description    javadoc
Javadoc for %{pkg_name}.

%prep
%{?scl:scl enable %{scl_maven} %{scl} - << "EOF"}
%setup -q -n %{pkg_name}-%{version}
%patch0

# fix test which assumes that there is a group named "nogroup"
sed -i 's|"nogroup"|"root"|' src/test/java/jnr/posix/GroupTest.java

# Remove useless wagon extension.
%pom_xpath_remove "pom:build/pom:extensions"

%mvn_file : %{pkg_name}/%{pkg_name} %{pkg_name}

%{?scl:EOF}

%build
%{?scl:scl enable %{scl_maven} %{scl} - << "EOF"}
%mvn_build -f
%{?scl:EOF}

%install
%{?scl:scl enable %{scl_maven} %{scl} - << "EOF"}
%mvn_install
%{?scl:EOF}

%files -f .mfiles
%doc LICENSE.txt README.txt
%dir %{_javadir}/%{pkg_name}
%dir %{_mavenpomdir}/%{pkg_name}

%files javadoc -f .mfiles-javadoc

%changelog
* Sat Aug 22 2015 Mat Booth <mat.booth@redhat.com> - 3.0.14-2.2
- Fix unowned directories

* Wed Jul 1 2015 akurtakov <akurtakov@localhost.localdomain> 3.0.14-2.1
- Fix maven scl prefix.

* Tue Jun 30 2015 Jeff Johnston <jjohnstn@redhat.com> 3.0.14-2
- SCL-ize package.

* Tue Jun 30 2015 Jeff Johnston <jjohnstn@redhat.com> 3.0.14-1
- Initial import from rawhide.
