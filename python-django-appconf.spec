#
# Conditional build:
%bcond_with	doc	# don't build doc
%bcond_with	tests	# do not perform "make test"
%bcond_without	python2 # CPython 2.x module
%bcond_without	python3 # CPython 3.x module

%define	module		appconf
%define	egg_name	django_appconf
%define	pypi_name	django-appconf
Summary:	A helper class for handling configuration defaults of packaged apps gracefully
Name:		python-%{pypi_name}
Version:	1.0.1
Release:	1
License:	BSD
Source0:	https://pypi.python.org/packages/source/d/%{pypi_name}/%{pypi_name}-%{version}.tar.gz
# Source0-md5:	29c87a00f0d098b90f3ac6113ae6e52d
Group:		Libraries/Python
URL:		http://pypi.python.org/pypi/django-appconf/
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with python2}
BuildRequires:	python-modules
BuildRequires:	python-setuptools
%if %{with tests}
BuildRequires:	python-coverage
BuildRequires:	python-django
BuildRequires:	python-django-discover-runner
BuildRequires:	python-flake8
%endif
%endif
%if %{with doc}
BuildRequires:	sphinx-pdg-2
%endif
%if %{with python3}
BuildRequires:	python3-modules
BuildRequires:	python3-setuptools
%if %{with tests}
BuildRequires:	python3-coverage
BuildRequires:	python3-django
BuildRequires:	python3-django-discover-runner
BuildRequires:	python3-flake8
%endif
%endif
Requires:	python-django
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
A helper class for handling configuration defaults of packaged Django
apps gracefully.

%package -n python3-%{pypi_name}
Summary:	A helper class for handling configuration defaults of packaged apps gracefully
Group:		Libraries/Python
Requires:	python3-django

%description -n python3-%{pypi_name}
A helper class for handling configuration defaults of packaged Django
apps gracefully.

%package apidocs
Summary:	%{pypi_name} API documentation
Summary(pl.UTF-8):	Dokumentacja API %{pypi_name}
Group:		Documentation

%description apidocs
API documentation for %{pypi_name}.

%description apidocs -l pl.UTF-8
Dokumentacja API %{pypi_name}.

%prep
%setup -q -n %{pypi_name}-%{version}

%build
%if %{with python2}
%py_build %{?with_tests:test}

%if %{with tests}
export PYTHONPATH=.:$PYTHONPATH
export DJANGO_SETTINGS_MODULE=tests.test_settings
coverage run %{_bindir}/django-admin test -v2 test
%endif

%endif

%if %{with python3}
%py3_build %{?with_tests:test}
%endif

%if %{with doc}
# generate html docs
sphinx-build-2 docs html
# remove the sphinx-build leftovers
rm -r html/.{doctrees,buildinfo}
%endif

%install
%if %{with python2}
%py_install
%py_postclean
%endif

%if %{with python3}
%py3_install
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc README.rst LICENSE
%{py_sitescriptdir}/%{module}
%{py_sitescriptdir}/%{egg_name}-%{version}-py%{py_ver}.egg-info
%endif

%if %{with python3}
%files -n python3-%{pypi_name}
%defattr(644,root,root,755)
%doc README.rst LICENSE
%{py3_sitescriptdir}/%{module}
%{py3_sitescriptdir}/%{egg_name}-%{version}-py%{py3_ver}.egg-info
%endif

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc html/*
%endif
