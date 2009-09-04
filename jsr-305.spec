# Copyright (c) 2000-2008, JPackage Project
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the
#    distribution.
# 3. Neither the name of the JPackage Project nor the names of its
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

%define gcj_support 0

%define section free

Name:           jsr-305
Version:        0.1
Release:        %mkrel 1.0.2
Epoch:          0
Summary:        JSR 305: Annotations for Software Defect Detection in Java
# http://groups.google.com/group/jsr-305/browse_thread/thread/8105869a258c8c4f
License:        BSD
Group:          Development/Java
URL:            http://code.google.com/p/jsr-305/
# svn export -r20080806 http://jsr-305.googlecode.com/svn/trunk/ jsr-305-0.1
# tar cjf jsr-305-0.1.bz2 jsr-305-0.1
Source0:        http://code.google.com/p/jsr-305/jsr-305-0.1.tar.bz2
Source1:        jsr-305-ri-build.xml
Provides:       jsr305 = %{epoch}:%{version}-%{release}
Requires:       jpackage-utils
BuildRequires:  ant
BuildRequires:  java-devel
BuildRequires:  java-javadoc
BuildRequires:  jpackage-utils
BuildRequires:  java-rpmbuild
%if %{gcj_support}
BuildRequires:  java-gcj-compat-devel
%else
Buildarch:      noarch
%endif
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root

%description
This project contains reference implementations, test cases, and other
documents under source code control for Java Specification Request 305:
Annotations for Software Defect Detection. More information at the Google
group: http://groups.google.com/group/jsr-305.

%package javadoc
Summary:        Javadoc for %{name}
Group:          Development/Java

%description javadoc
Javadoc for %{name}.

%prep
%setup -q
%{__cp} -a %{SOURCE1} ri/build.xml

%build
export OPT_JAR_LIST=:
export CLASSPATH=
pushd ri
%{ant} -Dversion=%{version} -Djava.javadoc=%{_javadocdir}/java
popd

%install
%{__rm} -rf %{buildroot}

# jars
%{__mkdir_p} %{buildroot}%{_javadir}
%{__cp} -a ri/jsr-305-%{version}.jar %{buildroot}%{_javadir}/%{name}-%{version}.jar
%{__ln_s} %{name}-%{version}.jar %{buildroot}%{_javadir}/jsr305-%{version}.jar
(cd %{buildroot}%{_javadir} && for jar in *-%{version}*; do %{__ln_s} ${jar} ${jar/-%{version}/}; done)

# poms
%add_to_maven_depmap org.jsr-305 %{name} %{version} JPP %{name}

%{__mkdir_p} %{buildroot}%{_datadir}/maven2/poms
%{__cp} -a ri/pom.xml %{buildroot}%{_datadir}/maven2/poms/JPP.%{name}.pom

# javadoc
%{__mkdir_p} %{buildroot}%{_javadocdir}/%{name}-%{version}
%{__cp} -a ri/javadoc/* %{buildroot}%{_javadocdir}/%{name}-%{version}
%{__ln_s} %{name}-%{version} %{buildroot}%{_javadocdir}/%{name}

%{gcj_compile}

%clean
%{__rm} -rf %{buildroot}

%post
%update_maven_depmap
%if %{gcj_support}
%{update_gcjdb}
%endif

%postun
%update_maven_depmap
%if %{gcj_support}
%{clean_gcjdb}
%endif

%files
%defattr(0644,root,root,0755)
%{_javadir}/%{name}-%{version}.jar
%{_javadir}/%{name}.jar
%{_javadir}/jsr305-%{version}.jar
%{_javadir}/jsr305.jar
%{_datadir}/maven2/poms/*
%{_mavendepmapfragdir}/*
%{gcj_files}

%files javadoc
%defattr(0644,root,root,0755)
%{_javadocdir}/%{name}-%{version}
%{_javadocdir}/%{name}

