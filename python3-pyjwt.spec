#
# Conditional build:
%bcond_without	doc	# API documentation
%bcond_with	tests	# unit tests

%define		module	pyjwt
Summary:	JSON Web Token implementation in Python 3
Summary(pl.UTF-8):	Implementacja JSON Web Token w Pythonie 3
Name:		python3-%{module}
Version:	2.0.1
Release:	5
License:	MIT
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/pyjwt/
Source0:	https://files.pythonhosted.org/packages/source/P/PyJWT/PyJWT-%{version}.tar.gz
# Source0-md5:	93b74f59d08be8c852a3c259da2ea121
URL:		http://github.com/jpadilla/pyjwt
BuildRequires:	python3-modules >= 1:3.6
BuildRequires:	python3-setuptools
%if %{with tests}
BuildRequires:	python3-cryptography >= 3.3.1
BuildRequires:	python3-pytest >= 5.0.0
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with doc}
BuildRequires:	python3-sphinx_rtd_theme
BuildRequires:	sphinx-pdg-3
%endif
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
%setup -q -n PyJWT-%{version}

# Remove bundled egg-info
%{__rm} -r PyJWT.egg-info

%build
%py3_build

%if %{with tests}
%{__python3} -m pytest tests
%endif

%if %{with doc}
%{__make} -C docs html \
	SPHINXBUILD=sphinx-build-3
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py3_install

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS.rst CHANGELOG.rst LICENSE README.rst
%{py3_sitescriptdir}/jwt
%{py3_sitescriptdir}/PyJWT-%{version}-py*.egg-info

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/_build/html/{_static,*.html,*.js}
%endif
