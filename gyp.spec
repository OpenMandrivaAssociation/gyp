%global		revision	1617

Name:		gyp
Version:	0.1
Release:	0.1%{?revision:.%{revision}svn}
Summary:	Generate Your Projects

Group:		Development/Python
License:	BSD
URL:		http://code.google.com/p/gyp/
# No released tarball avaiable. so the tarball was generated
# from svn as following:
#
# 1. svn co http://gyp.googlecode.com/svn/trunk gyp
# 2. cd gyp
# 3. version=$(grep version= setup.py|cut -d\' -f2)
# 4. revision=$(svn info|grep -E "^Revision:"|cut -d' ' -f2)
# 5. tar -a --exclude-vcs -cf /tmp/gyp-$version-svn$revision.tar.bz2 *
Source0:	%{name}-%{version}-svn%{revision}.tar.bz2
Patch0:		gyp-rpmoptflags.patch

BuildRequires:	python-devel
BuildArch:	noarch

%description
GYP is a tool to generates native Visual Studio, Xcode and SCons
and/or make build files from a platform-independent input format.

Its syntax is a universal cross-platform build representation
that still allows sufficient per-platform flexibility to accommodate
irreconcilable differences.


%prep
%setup -q -c -n %{name}-%{version}-svn%{revision}
%patch0 -p1 -b .0-rpmoptflags
for i in $(find pylib -name '*.py'); do
	sed -e '\,#![ \t]*/.*python,{d}' $i > $i.new && touch -r $i $i.new && mv $i.new $i
done

%build
%{__python} setup.py build


%install
%{__python} setup.py install --root $RPM_BUILD_ROOT --skip-build


%files
%doc AUTHORS LICENSE
%{_bindir}/gyp
%{python_sitelib}/*
