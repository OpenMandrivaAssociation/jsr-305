Name:           jsr-305
Version:        0.4
Release:        0.6.20090319svn
Summary:        Correctness annotations for Java code

Group:          Development/Java
License:        BSD
URL:            http://jsr-305.googlecode.com/
# There has been no official release yet.  This is a snapshot of the Subversion
# repository as of 19 Mar 2009.  Use the following commands to generate the
# tarball:
#   svn export -r 49 http://jsr-305.googlecode.com/svn/trunk jsr-305
#   tar -cvf jsr-305-0.4.20090319.tar jsr-305
#   xz jsr-305-0.4.20090319.tar
Source0:        jsr-305-0.4.20090319.tar.xz

BuildRequires:  java-1.6.0-openjdk-devel
BuildRequires:  jpackage-utils, maven2
BuildRequires:  maven-compiler-plugin
BuildRequires:  maven-install-plugin
BuildRequires:  maven-jar-plugin
BuildRequires:  maven-javadoc-plugin
BuildRequires:  maven-resources-plugin
BuildRequires:  maven-site-plugin
BuildRequires:  maven-surefire-plugin
Requires:       java >= 1.5, jpackage-utils

BuildArch:      noarch

%package javadoc
Summary:        Javadoc documentation for %{name}
Group:          Development/Java
Requires:       jpackage-utils

%description
This package contains reference implementations, test cases, and other
documents for Java Specification Request 305: Annotations for Software Defect
Detection.

%description javadoc
This package contains the API documentation for %{name}.

%prep
%setup -q -n %{name}
sed -i 's/\r//' sampleUses/pom.xml

%build
export MAVEN_REPO_LOCAL=$(pwd)/.m2/repository
mkdir -p $MAVEN_REPO_LOCAL

mvn-jpp -Dmaven.repo.local=$MAVEN_REPO_LOCAL install
cd ri
mvn-jpp -Dmaven.repo.local=$MAVEN_REPO_LOCAL javadoc:javadoc

%install
rm -rf $RPM_BUILD_ROOT

# JAR files
mkdir -p $RPM_BUILD_ROOT%{_javadir}
cp -p ri/target/ri-0.1-SNAPSHOT.jar $RPM_BUILD_ROOT%{_javadir}/%{name}.jar

# Javadocs
mkdir -p $RPM_BUILD_ROOT%{_javadocdir}/%{name}
cp -rp ri/target/site/apidocs/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}/

# pom
mkdir -p $RPM_BUILD_ROOT%{_mavenpomdir}
install -pm 644 ri/pom.xml $RPM_BUILD_ROOT/%{_mavenpomdir}/JPP-%{name}.pom
%add_to_maven_depmap org.apache.maven %{name} %{version} JPP %{name}


%post
%update_maven_depmap

%postun
%update_maven_depmap

%pre javadoc
# workaround for rpm bug 646523 (can be removed in F-17)
[ $1 -gt 1 ] && [ -L %{_javadocdir}/%{name} ] && \
rm -rf $(readlink -f %{_javadocdir}/%{name}) %{_javadocdir}/%{name} || :

%files
%defattr(-,root,root,-)
%doc ri/LICENSE sampleUses
%{_mavenpomdir}/JPP-jsr-305.pom
%{_javadir}/*
%{_mavendepmapfragdir}/jsr-305

%files javadoc
%defattr(-,root,root,-)
%{_javadocdir}/*

