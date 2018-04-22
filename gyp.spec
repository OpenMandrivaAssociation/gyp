%global		revision	920ee58
%{expand:	%%global	archivename	gyp-%{version}%{?revision:-git%{revision}}}
%{!?python2_sitelib: %global python2_sitelib %(%{__python2} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%{!?python2_sitearch: %global python2_sitearch %(%{__python2} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")}

Name:		gyp
Version:	0.1
Release:	0.25%{?revision:.%{revision}git}%{?dist}
Summary:	Generate Your Projects

Group:		Development/Tools
License:	BSD
URL:		http://code.google.com/p/gyp/
# No released tarball avaiable. so the tarball was generated
# from svn as following:
#
# 1. svn co http://gyp.googlecode.com/svn/trunk gyp
# 2. cd gyp
# 3. version=$(grep version= setup.py|cut -d\' -f2)
# 4. revision=$(git log --oneline|head -1|cut -d' ' -f1)
# 5. tar -a --exclude-vcs -cf /tmp/gyp-$version-git$revision.tar.bz2 *
Source0:	%{archivename}.tar.bz2
Patch0:		gyp-rpmoptflags.patch
Patch1:		gyp-ninja-build.patch

BuildRequires:	python2-devel
BuildRequires:	python2-setuptools
Requires:	python2-setuptools
BuildArch:	noarch

%description
GYP is a tool to generates native Visual Studio, Xcode and SCons
and/or make build files from a platform-independent input format.

Its syntax is a universal cross-platform build representation
that still allows sufficient per-platform flexibility to accommodate
irreconcilable differences.


%prep
%setup -q -c -n %{archivename}
%patch0 -p1 -b .0-rpmoptflags
%patch1 -p1  -b .1-ninja-build
for i in $(find pylib -name '*.py'); do
	sed -e '\,#![ \t]*/.*python,{d}' $i > $i.new && touch -r $i $i.new && mv $i.new $i
done

%build
%{__python2} setup.py build


%install
%{__python2} setup.py install --root $RPM_BUILD_ROOT --skip-build

%files
%doc AUTHORS LICENSE
%{_bindir}/gyp
%{python2_sitelib}/*
