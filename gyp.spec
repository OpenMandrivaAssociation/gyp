# from https://chromium.googlesource.com/external/gyp/
%define date		20190716
%define commit		fcd686f1880fa52a1ee78d3e98af1b88cb334528

Name:		gyp
Version:	0.1
Release:	0.26%{?revision:.%{revision}git}%{?dist}
Summary:	Generate Your Projects

Group:		Development/Tools
License:	BSD
URL:		http://code.google.com/p/gyp/

# No released tarball avaiable. so the tarball was generated
# from git as following:
#
# 1. git clone https://chromium.googlesource.com/external/gyp.git
# 2. cd gyp
# 3. version=$(grep version= setup.py|cut -d\' -f2)
# 4. revision=$(svn info|grep -E "^Revision:"|cut -d' ' -f2)
# 5. tar -a --exclude-vcs -cf /tmp/gyp-$version-svn$revision.tar.bz2 *
Source0:	https://chromium.googlesource.com/external/gyp/+archive/%{commit}.tar.gz
Patch0:         gyp-rpmoptflags.patch
Patch1:         gyp-ninja-build.patch
Patch2:         gyp-python3.patch
Patch3:         gyp-python38.patch
Patch4:         gyp-fix-cmake.patch

BuildArch:	noarch
BuildRequires:	pkgconfig(python3)
BuildRequires:	python3dist(setuptools)
Requires:	python3dist(setuptools)

%description
GYP is a tool to generates native Visual Studio, Xcode and SCons
and/or make build files from a platform-independent input format.

Its syntax is a universal cross-platform build representation
that still allows sufficient per-platform flexibility to accommodate
irreconcilable differences.


%prep
%autosetup -p1 -c -n %{commit}

for i in $(find pylib -name '*.py'); do
	sed -e '\,#![ \t]*/.*python,{d}' $i > $i.new && touch -r $i $i.new && mv $i.new $i
done

%build
%py3_build

%install
%py3_install

%files
%doc AUTHORS LICENSE
%{_bindir}/gyp
%{python3_sitelib}/*
