Name:           jsr-305
Version:        3.0.2
Release:        3
Summary:        Correctness annotations for Java code
Group:          Development/Java
# The majority of code is BSD-licensed, but some Java sources
# are licensed under CC-BY license, see: $ grep -r Creative .
License:        BSD and CC-BY
URL:            https://repo1.maven.org/maven2/com/google/code/findbugs/jsr305
Source0:        https://repo1.maven.org/maven2/com/google/code/findbugs/jsr305/%{version}/jsr305-%{version}-sources.jar
Source1:        jsr305-%{version}.pom
BuildRequires:	jdk-current
BuildRequires:	python
BuildRequires:	javapackages-local
BuildArch:      noarch
# javapackages-tools 6.5.1 no longer ships the maven depmap install macro.
Provides:	mvn(com.google.code.findbugs:jsr305) = %{version}
Provides:	sysjar(com.google.code.findbugs:jsr305) = %{version}

%package javadoc
Summary:        Javadoc documentation for %{name}

%description
This package contains reference implementations, test cases, and other
documents for Java Specification Request 305: Annotations for Software Defect
Detection.

%description javadoc
This package contains the API documentation for %{name}.

%prep
%setup -q -c -T
# The builders' rpmuncompress passes a sources jar to tar.
python - %{SOURCE0} <<'PY'
import sys
import zipfile
zipfile.ZipFile(sys.argv[1]).extractall(".")
PY

%build
. %{_sysconfdir}/profile.d/90java.sh
export PATH=$JAVA_HOME/bin:$PATH

echo 'module javax.annotation {' >module-info.java
find . -name "*.java" |xargs grep ^package |sed -e 's,^.*package ,,;s,\;.*,,' |sort |uniq |while read e; do
	echo "	exports $e;" >>module-info.java
done
echo '}' >>module-info.java
find . -name "*.java" |xargs javac
find . -name "*.class" -o -name "*.properties" |xargs jar cf javax.annotation-%{version}.jar
jar i javax.annotation-%{version}.jar
javadoc -d docs -sourcepath . javax.annotation
cp %{S:1} .

%install
mkdir -p %{buildroot}%{_javadir}/modules %{buildroot}%{_mavenpomdir} %{buildroot}%{_javadocdir}
cp javax.annotation-%{version}.jar %{buildroot}%{_javadir}/modules
ln -s modules/javax.annotation-%{version}.jar %{buildroot}%{_javadir}/
ln -s modules/javax.annotation-%{version}.jar %{buildroot}%{_javadir}/javax.annotation.jar
cp *.pom %{buildroot}%{_mavenpomdir}/
mkdir -p %{buildroot}%{_datadir}/sysjar/index/com.google.code.findbugs
python - %{version} <<'PY'
import json
import sys
from pathlib import Path
version = sys.argv[1]
record = {
    "aliases": [],
    "artifactId": "jsr305",
    "classifier": "",
    "dependencies": [],
    "extension": "jar",
    "groupId": "com.google.code.findbugs",
    "jar": "/usr/share/java/modules/javax.annotation-" + version + ".jar",
    "pom": "/usr/share/maven-poms/jsr305-" + version + ".pom",
    "sysjar": 1,
    "version": version,
}
Path("jsr305.sysjar").write_text(json.dumps(record, indent=2, sort_keys=True) + "\n", encoding="utf-8")
PY
install -m 644 jsr305.sysjar %{buildroot}%{_datadir}/sysjar/index/com.google.code.findbugs/jsr305.sysjar
cp -a docs %{buildroot}%{_javadocdir}/%{name}

%files
%{_javadir}/*.jar
%{_javadir}/modules/javax.annotation-%{version}.jar
%{_mavenpomdir}/jsr305-%{version}.pom
%dir %{_datadir}/sysjar/index/com.google.code.findbugs
%{_datadir}/sysjar/index/com.google.code.findbugs/jsr305.sysjar

%files javadoc
%{_datadir}/javadoc/%{name}
