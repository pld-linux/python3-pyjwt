#
# Conditional build:
%bcond_with	tests	# unit tests
%bcond_without	python2 # CPython 2.x module
%bcond_without	python3 # CPython 3.x module

%define		module	pyjwt
Summary:	JSON Web Token implementation in Python 2
Summary(pl.UTF-8):	Implementacja JSON Web Token w Pythonie 2
Name:		python-%{module}
# keep 1.x here for python2 support
Version:	1.7.1
Release:	1
License:	MIT
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/pyjwt/
Source0:	https://files.pythonhosted.org/packages/source/P/PyJWT/PyJWT-%{version}.tar.gz
# Source0-md5:	a4712f980c008696e13e09504120b2a0
Patch0:		%{name}-tests.patch
URL:		http://github.com/jpadilla/pyjwt
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with python2}
BuildRequires:	python-modules >= 1:2.7
BuildRequires:	python-setuptools
%if %{with tests}
BuildRequires:	python-Crypto
BuildRequires:	python-ecdsa
BuildRequires:	python-pytest >= 4.0.1
BuildRequires:	python-pytest-cov >= 2.6.0
BuildRequires:	python-pytest-runner >= 4.2
%endif
%endif
%if %{with python3}
BuildRequires:	python3-modules >= 1:3.4
BuildRequires:	python3-setuptools
%if %{with tests}
BuildRequires:	python3-Crypto
BuildRequires:	python3-ecdsa
BuildRequires:	python3-pytest >= 4.0.1
BuildRequires:	python3-pytest-cov >= 2.6.0
BuildRequires:	python3-pytest-runner >= 4.2
%endif
%endif
# file and namespace conflict
Conflicts:	python-jwt
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
A Python implementation of RFC 7519. Original implementation was
written by @progrium.

%description -l pl.UTF-8
Pythonowa implementacja RFC 7519. Oryginalna implementacja została
napisana przez @progrium.

%package -n python3-%{module}
Summary:	JSON Web Token implementation in Python 3
Summary(pl.UTF-8):	Implementacja JSON Web Token w Pythonie 3
Group:		Libraries/Python
Requires:	python3-setuptools
# file and namespace conflict
Conflicts:	python3-jwt

%description -n python3-%{module}
A Python implementation of RFC 7519. Original implementation was
written by @progrium.

%description -n python3-%{module} -l pl.UTF-8
Pythonowa implementacja RFC 7519. Oryginalna implementacja została
napisana przez @progrium.

%prep
%setup -q -n PyJWT-%{version}
%patch0 -p1

# Remove bundled egg-info
%{__rm} -r PyJWT.egg-info

%build
%if %{with python2}
%py_build %{?with_tests:pytest}
%endif

%if %{with python3}
%py3_build %{?with_tests:pytest}
%endif

%install
rm -rf $RPM_BUILD_ROOT
%if %{with python2}
%py_install
%py_postclean
%{__mv} $RPM_BUILD_ROOT%{_bindir}/pyjwt{,-2}
%endif

%if %{with python3}
%py3_install
%{__mv} $RPM_BUILD_ROOT%{_bindir}/pyjwt{,-3}
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc AUTHORS CHANGELOG.md LICENSE README.rst
%attr(755,root,root) %{_bindir}/pyjwt-2
%{py_sitescriptdir}/jwt
%{py_sitescriptdir}/PyJWT-%{version}-py*.egg-info
%endif

%if %{with python3}
%files -n python3-%{module}
%defattr(644,root,root,755)
%doc AUTHORS CHANGELOG.md LICENSE README.rst
%attr(755,root,root) %{_bindir}/pyjwt-3
%{py3_sitescriptdir}/jwt
%{py3_sitescriptdir}/PyJWT-%{version}-py*.egg-info
%endif
