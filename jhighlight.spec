%{?_javapackages_macros:%_javapackages_macros}
Name:           jhighlight
Version:        1.0
Release:        11.3
Summary:        An embeddable pure Java syntax highlighting library

Group:          Development/Java
License:        LGPLv2+
URL:            http://svn.rifers.org/jhighlight

# svn export http://svn.rifers.org/jhighlight/tags/release-1.0/ jhighlight-1.0
# find jhighlight-1.0/ -name *.jar
# tar cJf jhighlight-1.0.tar.xz jhighlight-1.0/
Source0:        %{name}-%{version}.tar.xz
Source1:        http://central.maven.org/maven2/com/uwyn/%{name}/%{version}/%{name}-%{version}.pom

BuildArch:      noarch

BuildRequires:  ant
BuildRequires:  java-devel
BuildRequires:  jflex
BuildRequires:  jpackage-utils
BuildRequires:  javapackages-local
BuildRequires:  tomcat-servlet-3.0-api

Requires:       java-headless
Requires:       jflex
Requires:       jpackage-utils
Requires:       tomcat-servlet-3.0-api

%description
JHighlight is an embeddable pure Java syntax highlighting library that supports
Java, Groovy, C++, HTML, XHTML, XML and LZX languages and outputs to XHTML. It
also supports RIFE (http://rifers.org) templates tags and highlights them
clearly so that you can easily identify the difference between your RIFE markup
and the actual marked up source.

%package javadoc
Summary:        Javadocs for %{name}
Group:          Documentation
Requires:       jpackage-utils

%description javadoc
This package contains the API documentation for %{name}.

%prep
%setup -q

find -name '*.class' -delete
find -name '*.jar' -delete

pushd lib/
ln -s %{_javadir}/jflex.jar
ln -s %{_javadir}/tomcat-servlet-3.0-api.jar
popd

sed -i -e "s/JFlex.anttask.JFlexTask/jflex.anttask.JFlexTask/" build.xml

cp %{SOURCE1} %{name}.pom
%pom_change_dep javax.servlet:servlet-api org.apache.tomcat:tomcat-servlet-api %{name}.pom
%mvn_file com.uwyn:jhighlight %{name}

%build
ant

%mvn_artifact %{name}.pom build/dist/%{name}-%{version}.jar

%install
mkdir javadoc
unzip build/dist/%{name}-javadocs-%{version}.zip -d javadoc

%mvn_install -J javadoc/docs/api

%files -f .mfiles
%doc README
%doc COPYING
%doc LICENSE_LGPL.txt

%files javadoc -f .mfiles-javadoc
%doc LICENSE_LGPL.txt
%doc COPYING


%changelog
* Wed Jul 02 2014 Gerard Ryan <galileo@fedoraproject.org> - 1.0-11
- Pull content up from nested dirs in javadoc pkg

* Tue Jul 01 2014 Gerard Ryan <galileo@fedoraproject.org> - 1.0-10
- Use new mvn_* macros to generate metadata
- Change broken servlet-api dependency in POM

* Mon Jun 09 2014 Gerard Ryan <galileo@fedoraproject.org> - 1.0-8
- RHBZ-1106948: FTBFS in rawhide (mass rebuild)

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Mar 23 2014 Gerard Ryan <galileo@fedoraproject.org> - 1.0-6
- RHBZ-1068284: Switch to java-headless Requires

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Jul 24 2012 Gerard Ryan <galileo@fedoraproject.org> - 1.0-3
- Remove jars from source tarball before inclusion in srpm.

* Tue Jul 24 2012 Gerard Ryan <galileo@fedoraproject.org> - 1.0-2
- Remove lgpl text added from external source.

* Tue Jul 24 2012 Gerard Ryan <galileo@fedoraproject.org> - 1.0-1
- Initial package.
