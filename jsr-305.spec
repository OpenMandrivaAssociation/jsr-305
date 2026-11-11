Name:           jsr-305
Version:        3.0.2
Release:        4
Summary:        Correctness annotations for Java code
Group:          Development/Java
# The majority of code is BSD-licensed, but some Java sources
# are licensed under CC-BY license, see: $ grep -r Creative .
License:        BSD and CC-BY
URL:            https://repo1.maven.org/maven2/com/google/code/findbugs/jsr305
# Unpacked from the 3.0.2 sources jar. No class files.
Source0:        jsr305-%{version}-sources.tar.gz
Source1:        jsr305-%{version}.pom
BuildRequires:	jdk-current
BuildRequires:	python
BuildRequires:	java-current-devel
# %{_javadir} and %{_mavenpomdir} come from this package. Without it the
# file list is rejected as "File must begin with /".
BuildRequires:	javapackages-filesystem
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
%autosetup -n jsr305-%{version}

%build
. %{_sysconfdir}/profile.d/90java.sh
export PATH=$JAVA_HOME/bin:$PATH

# Class files stay at Java 8. A module-info compiled by the builder JDK
# made the previous jar unreadable on JDK 25.
find . -name '*.java' > sources.list
test "$(wc -l < sources.list)" -eq 31
mkdir -p classes
javac --release 8 -encoding UTF-8 -Xlint:-options -d classes @sources.list
jar cf javax.annotation-%{version}.jar -C classes .
jar i javax.annotation-%{version}.jar
javap -verbose -cp javax.annotation-%{version}.jar javax.annotation.Nullable | grep -F 'major version: 52'
javadoc -d docs -sourcepath . javax.annotation
cp %{S:1} .

%check
. %{_sysconfdir}/profile.d/90java.sh
export PATH=$JAVA_HOME/bin:$PATH
mkdir -p check
cat > check/Smoke.java << 'EOF'
import javax.annotation.Nullable;
import java.lang.annotation.Retention;
public class Smoke {
	public static void main(String[] args) {
		Retention retention = Nullable.class.getAnnotation(Retention.class);
		if (retention == null) {
			throw new RuntimeException("no retention");
		}
		System.out.println("jsr305_ok " + retention.value());
	}
}
EOF
JAR=%{buildroot}%{_javadir}/javax.annotation.jar
test -f "$JAR"
javac --release 8 -encoding UTF-8 -Xlint:-options -cp "$JAR" -d check check/Smoke.java
java -cp "check:$JAR" Smoke > check/out.txt
cat check/out.txt
grep -F -q 'jsr305_ok RUNTIME' check/out.txt

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
