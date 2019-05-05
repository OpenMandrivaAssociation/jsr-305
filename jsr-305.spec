Name:           jsr-305
Version:        3.0.2
Release:        1
Summary:        Correctness annotations for Java code
# The majority of code is BSD-licensed, but some Java sources
# are licensed under CC-BY license, see: $ grep -r Creative .
License:        BSD and CC-BY
URL:            https://repo1.maven.org/maven2/com/google/code/findbugs/jsr305
Source0:        https://repo1.maven.org/maven2/com/google/code/findbugs/jsr305/%{version}/jsr305-%{version}-sources.jar
Source1:        https://repo1.maven.org/maven2/com/google/code/findbugs/jsr305/%{version}/jsr305-%{version}.pom
BuildRequires:	jdk-current
BuildRequires:	javapackages-local
BuildArch:      noarch

%package javadoc
Summary:        Javadoc documentation for %{name}

%description
This package contains reference implementations, test cases, and other
documents for Java Specification Request 305: Annotations for Software Defect
Detection.

%description javadoc
This package contains the API documentation for %{name}.

%prep
%autosetup -p1 -c %{name}-%{version}

%build
. %{_sysconfdir}/profile.d/90java.sh
export PATH=$JAVA_HOME/bin:$PATH

cat >module-info.java <<'EOF'
module javax.annotation {
        exports javax.annotation;
}
EOF
find . -name "*.java" |xargs javac
find . -name "*.class" -o -name "*.properties" |xargs jar cf javax.annotation-%{version}.jar
javadoc -d docs -sourcepath . javax.annotation
cp %{S:1} .

%install
mkdir -p %{buildroot}%{_javadir} %{buildroot}%{_mavenpomdir} %{buildroot}%{_javadocdir}
cp javax.annotation-%{version}.jar %{buildroot}%{_javadir}
cp *.pom %{buildroot}%{_mavenpomdir}/
%add_maven_depmap jsr305-%{version}.pom javax.annotation-%{version}.jar
cp -a docs %{buildroot}%{_javadocdir}/%{name}

%files -f .mfiles
%{_javadir}/javax.annotation-%{version}.jar

%files javadoc
%{_datadir}/javadoc/%{name}
