%global debug_package %{nil}

# Run tests in check section
%bcond_without check

# https://github.com/golang/mod
%global goipath		golang.org/x/mod
%global forgeurl	https://github.com/golang/mod
Version:		0.20.0

%gometa

%if %{with bootstrap2}
%global __requires_exclude golang\\\(golang\\.org/x/mod.*\\\)$
%endif

Summary:	Go module mechanics libraries
Name:		golang-x-mod

Release:	1
Source0:	https://github.com/golang/mod/archive/v%{version}/mod-%{version}.tar.gz
URL:		https://github.com/golang/mod
License:	BSD-3-Clause
Group:		Development/Other
BuildRequires:	compiler(go-compiler)
BuildRequires:	golang-ipath(golang.org/x/tools)

%description
This provides GO packages for writing tools that work
directly with Go module mechanics.  That is, it is for
direct manipulation of Go modules themselves.

%files
%license LICENSE PATENTS
%doc README.md
%{_bindir}/gosumcheck

#-----------------------------------------------------------------------

%package devel
Summary:	%{summary}
Group:		Development/Other
BuildArch:	noarch

%description devel
%{description}

This package contains library source intended for
building other packages which use import path with
%{goipath} prefix.

%files devel -f devel.file-list
%license LICENSE PATENTS
%doc README.md

#-----------------------------------------------------------------------

%prep
%autosetup -p1 -n mod-%{version}

%build
%gobuildroot
for cmd in gosumcheck; do
	%gobuild -o _bin/$cmd %{goipath}/$cmd
done

%install
%goinstall
for cmd in $(ls -1 _bin) ; do
	install -Dpm 0755 _bin/$cmd %{buildroot}%{_bindir}/$cmd
done

%check
%if %{with check}
# NOTE:
#   sumdb/tlog needs network
#   zip needs network
%gochecks -d sumdb/tlog -d zip
%endif

