#
# Conditional build:
%bcond_without	doc	# API documentation
%bcond_without	tests	# unit tests

%define		module	pyjwt
Summary:	JSON Web Token implementation in Python 3
Summary(pl.UTF-8):	Implementacja JSON Web Token w Pythonie 3
Name:		python3-%{module}
Version:	2.15.1
Release:	1
License:	MIT
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/pyjwt/
Source0:	https://files.pythonhosted.org/packages/source/P/PyJWT/pyjwt-%{version}.tar.gz
# Source0-md5:	c095da5019479aa8153266b1adc09d3c
URL:		http://github.com/jpadilla/pyjwt
BuildRequires:	python3-build
BuildRequires:	python3-installer
BuildRequires:	python3-modules >= 1:3.9
BuildRequires:	python3-setuptools >= 1:77.0.3
%if %{with tests}
BuildRequires:	python3-cryptography >= 3.4.0
BuildRequires:	python3-pytest >= 8.4.2
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 2.044
%if %{with doc}
BuildRequires:	python3-sphinx_rtd_theme
BuildRequires:	python3-zope.interface
BuildRequires:	sphinx-pdg-3
%endif
Requires:	python3-modules >= 1:3.9
# file and namespace conflict
Conflicts:	python3-jwt
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
A Python implementation of RFC 7519. Original implementation was
written by @progrium.

%description -l pl.UTF-8
Pythonowa implementacja RFC 7519. Oryginalna implementacja została
napisana przez @progrium.

%package apidocs
Summary:	API documentation for PyJWT
Summary(pl.UTF-8):	Dokumentacja API moduły PyJWT
Group:		Documentation

%description apidocs
API documentation for PyJWT.

%description apidocs -l pl.UTF-8
Dokumentacja API moduły PyJWT.

%prep
%setup -q -n pyjwt-%{version}

%build
%py3_build_pyproject

%if %{with tests}
# test_get_jwt_set_sslcontext_default requires network
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
%{__python3} -m pytest tests -k 'not test_get_jwt_set_sslcontext_default'
%endif

%if %{with doc}
%{__make} -C docs html \
	SPHINXBUILD=sphinx-build-3
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py3_install_pyproject

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS.rst CHANGELOG.rst LICENSE README.rst SECURITY.md
%{py3_sitescriptdir}/jwt
%{py3_sitescriptdir}/pyjwt-%{version}.dist-info

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/_build/html/{_static,*.html,*.js}
%endif
