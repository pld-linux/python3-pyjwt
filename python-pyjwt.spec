#
# Conditional build:
%bcond_with	doc	# don't build doc
%bcond_with	tests	# do not perform "make test"
%bcond_without	python2 # CPython 2.x module
%bcond_without	python3 # CPython 3.x module

%define		module	pyjwt
Summary:	JSON Web Token implementation in Python
Name:		python-%{module}
Version:	1.4.0
Release:	1
License:	MIT
Group:		Libraries/Python
Source0:	https://files.pythonhosted.org/packages/source/P/PyJWT/PyJWT-%{version}.tar.gz
# Source0-md5:	2f9bd9226d72b13d19d2c557114d03dc
URL:		http://github.com/jpadilla/pyjwt
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with python2}
BuildRequires:	python-modules
BuildRequires:	python-setuptools
%if %{with tests}
BuildRequires:	python-pytest
BuildRequires:	python-pytest-cov
BuildRequires:	python-pytest-runner
%endif
%endif
%if %{with python3}
BuildRequires:	python3-modules
BuildRequires:	python3-setuptools
%if %{with tests}
BuildRequires:	python3-pytest
BuildRequires:	python3-pytest-cov
BuildRequires:	python3-pytest-runner
%endif
%endif
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
A Python implementation of RFC 7519. Original implementation was
written by @progrium.

%package -n python3-%{module}
Summary:	JSON Web Token implementation in Python
Requires:	python3-setuptools

%description -n python3-%{module}
A Python implementation of RFC 7519. Original implementation was
written by @progrium.

%prep
%setup -q -n PyJWT-%{version}

# Remove bundled egg-info
%{__rm} -r PyJWT.egg-info

%build
%if %{with python2}
%py_build %{?with_tests:test}
%endif

%if %{with python3}
%py3_build %{?with_tests:test}
%endif

%install
rm -rf $RPM_BUILD_ROOT
%if %{with python2}
%py_install
%py_postclean
mv $RPM_BUILD_ROOT%{_bindir}/jwt{,-2}
%endif

%if %{with python3}
%py3_install
mv $RPM_BUILD_ROOT%{_bindir}/jwt{,-3}
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc README.md LICENSE
%attr(755,root,root) %{_bindir}/jwt-2
%{py_sitescriptdir}/jwt
%{py_sitescriptdir}/PyJWT-%{version}-py*.egg-info
%endif

%if %{with python3}
%files -n python3-%{module}
%defattr(644,root,root,755)
%doc README.md LICENSE
%attr(755,root,root) %{_bindir}/jwt-3
%{py3_sitescriptdir}/jwt
%{py3_sitescriptdir}/PyJWT-%{version}-py*.egg-info
%endif
