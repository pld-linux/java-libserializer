#
# Conditional build:
%bcond_without	javadoc		# don't build javadoc

%define		srcname		libserializer
%include	/usr/lib/rpm/macros.java
Summary:	JFreeReport General Serialization Framework
Name:		java-%{srcname}
Version:	1.1.2
Release:	1
License:	LGPL v2+
Group:		Libraries/Java
Obsoletes:	libserializer
Source0:	http://downloads.sourceforge.net/jfreereport/libserializer-%{version}.zip
# Source0-md5:	61b41eb7423a6aba3bf1138089ff6213
Patch0:		build.patch
URL:		http://reporting.pentaho.org
BuildRequires:	ant
BuildRequires:	ant-contrib
BuildRequires:	ant-nodeps
BuildRequires:	java-libbase >= 1.1.2
BuildRequires:	jdk
BuildRequires:	jpackage-utils
BuildRequires:	jpackage-utils
BuildRequires:	rpm-javaprov
BuildRequires:	rpmbuild(macros) >= 1.300
Requires:	java-libbase >= 1.1.2
Requires:	jpackage-utils
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Libserializer contains a general serialization framework that
simplifies the task of writing custom java serialization handlers.

%package javadoc
Summary:	Javadoc for Libserializer
Group:		Documentation
Requires:	jpackage-utils

%description javadoc
Javadoc for Libserializer.

%prep
%setup -qc
%patch0 -p1
find -name "*.jar" | xargs rm -v

install -d lib
ln -s %{_javadir}/ant lib/ant-contrib

%build
build-jar-repository -s -p lib libbase commons-logging-api

%ant jar %{?with_javadoc:javadoc}

%install
rm -rf $RPM_BUILD_ROOT

# jars
install -d $RPM_BUILD_ROOT%{_javadir}
cp -p dist/%{srcname}-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{srcname}-%{version}.jar
ln -s %{srcname}-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{srcname}.jar

# javadoc
%if %{with javadoc}
install -d $RPM_BUILD_ROOT%{_javadocdir}/%{srcname}-%{version}
cp -a bin/javadoc/docs/api/* $RPM_BUILD_ROOT%{_javadocdir}/%{srcname}-%{version}
ln -s %{srcname}-%{version} $RPM_BUILD_ROOT%{_javadocdir}/%{srcname} # ghost symlink
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post javadoc
ln -nfs %{srcname}-%{version} %{_javadocdir}/%{srcname}

%files
%defattr(644,root,root,755)
%doc ChangeLog.txt licence-LGPL.txt README.txt
%{_javadir}/%{srcname}-%{version}.jar
%{_javadir}/%{srcname}.jar

%if %{with javadoc}
%files javadoc
%defattr(644,root,root,755)
%{_javadocdir}/%{srcname}-%{version}
%ghost %{_javadocdir}/%{srcname}
%endif
