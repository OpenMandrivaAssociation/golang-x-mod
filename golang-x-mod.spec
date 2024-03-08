%global debug_package %{nil}

%bcond_without bootstrap2

# Run tests in check section
%bcond_without check

# https://github.com/golang/mod
%global goipath		golang.org/x/mod
%global forgeurl	https://github.com/golang/mod
Version:		0.16.0

%gometa

%if %{with bootstrap2}
%global __requires_exclude golang\\\(golang\\.org/x/mod.*\\\)$
%endif

Summary:	Go module mechanics libraries
Name:		golang-x-mod

Release:	1
Source0:	https://github.com/golang/mod/archive/v%{version}/mod-%{version}.tar.gz
%if %{with bootstrap2}
# Generated from Source100
Source3:	vendor.tar.zst
Source100:	golang-package-dependencies.sh
%endif
URL:		https://github.com/golang/mod
License:	BSD-3-Clause
Group:		Development/Other
BuildRequires:	compiler(go-compiler)
%if ! %{with bootstrap2}
BuildRequires:	golang-ipath(golang.org/x/tools)
BuildRequires:	golang(github.com/google/go-cmp/cmp)
BuildRequires:	golang(github.com/jba/printsrc)
BuildRequires:	golang(github.com/yuin/goldmark)
BuildRequires:	golang(github.com/yuin/goldmark/ast)
BuildRequires:	golang(github.com/yuin/goldmark/parser)
BuildRequires:	golang(github.com/yuin/goldmark/renderer/html)
BuildRequires:	golang(github.com/yuin/goldmark/text)
BuildRequires:	golang(golang.org/x/mod/modfile)
BuildRequires:	golang(golang.org/x/mod/module)
BuildRequires:	golang(golang.org/x/mod/semver)
BuildRequires:	golang(golang.org/x/net/html)
BuildRequires:	golang(golang.org/x/net/html/atom)
BuildRequires:	golang(golang.org/x/net/websocket)
BuildRequires:	golang(golang.org/x/sync/errgroup)
BuildRequires:	golang(golang.org/x/text/unicode/runenames)
BuildRequires:	golang(golang.org/x/vuln/scan)
BuildRequires:	golang(honnef.co/go/tools/analysis/lint)
BuildRequires:	golang(honnef.co/go/tools/quickfix)
BuildRequires:	golang(honnef.co/go/tools/simple)
BuildRequires:	golang(honnef.co/go/tools/staticcheck)
BuildRequires:	golang(honnef.co/go/tools/stylecheck)
BuildRequires:	golang(mvdan.cc/gofumpt/format)
BuildRequires:	golang(mvdan.cc/xurls/v2)
%endif

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

rm -rf vendor

%if %{with bootstrap2}
tar xf %{S:3}
%endif

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

