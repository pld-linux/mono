#
# Conditional build:
%bcond_with	nptl		# enable support for NPTL
#
Summary:	Common Language Infrastructure implementation
Summary(pl):	Implementacja Common Language Infrastructure
Name:		mono
Version:	1.0.2
Release:	1
License:	LGPL
Group:		Development/Languages
Source0:	http://www.go-mono.com/archive/%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	4490424a30ce40d1d7534cc681f6c14c
Source1:	http://www.go-mono.com/archive/%{version}/mcs-%{version}.tar.gz
# Source1-md5:	8052bfcb065d8c81e413b22fee549640
Patch0:		%{name}-nolibs.patch
Patch1:		%{name}-runtime-install-path.patch
URL:		http://www.mono-project.org/
ExcludeArch:	alpha
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	bison
BuildRequires:	glib2-devel >= 2.0.0
BuildRequires:	libtool
BuildRequires:	pkgconfig
BuildRequires:	icu
BuildRequires:	libicu-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# workaround for buggy gcc 3.3.1
%define         specflags_alpha  -mno-explicit-relocs 

%description
The Common Language Infrastructure platform. Microsoft has created a
new development platform. The highlights of this new development
platform are:
- A runtime environment that provides garbage collection, threading
  and a virtual machine specification (The Virtual Execution System,
  VES),
- A comprehensive class library,
- A new language, C#. Very similar to Java, C# allows programmers to
  use all the features available on the .NET runtime,
- A language specification that compilers can follow if they want to
  generate classes and code that can interoperate with other programming
  languages (The Common Language Specification: CLS).

%description -l pl
Platforma CLI (Common Language Infrastructure). Microsoft stworzy³
now± platformê developersk±. Zalety tej platformy to:
- ¶rodowisko, które dostarcza garbage collector, w±tki oraz
  specyfikacjê maszyny wirtualnej (The Virtual Execution System, VES),
- bibliotekê klas,
- nowy jêzyk, C#. Bardzo podobny do Javy, C# pozwala programistom na
  u¿ywanie wszystkich mo¿liwo¶ci dostarczanych przez platformê .NET,
- specyfikacja dla kompilatorów, które chc± generowaæ kod
  wspó³pracuj±cy z innymi jêzykami programowania (The Common Language
  Specification: CLS).

%package devel
Summary:	Development resources for mono
Summary(pl):	Zasoby programisty do mono
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Development resources for mono.

%description devel -l pl
Zasoby programisty dla mono.

%package basic
Summary:	MonoBASIC compiler for mono
Summary(pl):	Kompilator MonoBASIC dla mono
Group:		Development/Languages
Requires:	%{name}-devel = %{version}-%{release}

%description basic
MonoBASIC compiler for mono.

%description basic -l pl
Kompilator MonoBASIC dla mono.

%package csharp
Summary:	C# compiler for mono
Summary(pl):	Kompilator C# dla mono
Group:		Development/Languages
Requires:	%{name}-devel = %{version}-%{release}

%description csharp
C# compiler for mono.

%description csharp -l pl
Kompilator C# dla mono.

%package ilasm
Summary:	ILasm compiler for mono
Summary(pl):	Kompilator ILasm dla mono
Group:		Development/Languages
Requires:	%{name}-devel = %{version}-%{release}
Provides:	ilasm
Obsoletes:	pnet-compiler-ilasm

%description ilasm
ILasm compiler for mono.

%description ilasm -l pl
Kompilator ILasm dla mono.

%package static
Summary:	Static mono library
Summary(pl):	Statyczna biblioteka mono
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static mono library.

%description static -l pl
Statyczna biblioteka mono.

%package jay
Summary:	Yacc-like parser generator for Java and C#
Summary(pl):	Podobny do Yacca generator parserów dla Javy i C#
Group:		Development/Tools

%description jay
Yacc-like parser generator for Java and C#.

%description jay -l pl
Podobny do Yacca generator parserów dla Javy i C#.

%package compat-links
Summary:	Mono compatibility links
Summary(pl):	Dowi±zania dla kompatybilno¶ci
Group:		Development/Languages
Requires:	%{name}-devel = %{version}-%{release}

%description compat-links
This package contains links to binaries with names used in .NET and
dotGNU.

%description compat-links -l pl
Pakiet ten zawiera dowi±zania do programów o nazwach u¿ywanych w .NET
oraz dotGNU.

%prep
%setup -q -a1
%patch0 -p1
%patch1 -p1

# quick hack for sparc
perl -p -i -e 's/LIBC="libc.so"//' configure.in

%build
cp -f /usr/share/automake/config.sub .
cp -f /usr/share/automake/config.sub libgc
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__automake}
%configure \
	%{?with_nptl:--with-nptl} \
	%{!?with_nptl:--without-nptl} \
	--with-preview=yes \
%ifarch amd64
	--with-sigaltstack=yes \
	--with-gc=none
%else
	--with-gc=included
%endif

%{__make}

# for now we only build jay, and don't rebuild runtime and mcs
%{__make} -C mcs-*/jay \
	CC="%{__cc}" \
	CFLAGS="%{rpmcflags} -DSKEL_DIRECTORY=\\\"%{_datadir}/jay\\\""

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__make} -C mcs-*/jay install \
	prefix=%{_prefix} \
	DESTDIR=$RPM_BUILD_ROOT
mv -f $RPM_BUILD_ROOT%{_prefix}/man/man1/* $RPM_BUILD_ROOT%{_mandir}/man1
rm -f $RPM_BUILD_ROOT%{_datadir}/jay/[A-Z]*

# Make links to all binaries. In fact we could move *.exe to
# %{_libdir}, but probably something relays on it.
old="$(pwd)"
cd $RPM_BUILD_ROOT%{_bindir}
for f in *.exe ; do
	bn=$(basename $f .exe)
	rm -f $bn
	echo "#!/bin/sh" > $bn
%ifarch %{ix86} ppc sparc
	echo "%{_bindir}/mono %{_bindir}/$f" '"$@"' >> $bn
%else
	echo "%{_bindir}/mint %{_bindir}/$f" '"$@"' >> $bn
%endif
done
cd "$old"

# this way we can run rpmbuild -bi several times, and directories
# have more meaningful name.
rm -rf pld-doc
mkdir -p pld-doc/{webpage,notes}
cp -a web/* pld-doc/webpage
cp -a docs/* pld-doc/notes
rm -f pld-doc/*/Makefile*

%clean
rm -rf $RPM_BUILD_ROOT

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/mint
%ifarch %{ix86} ppc sparc
%attr(755,root,root) %{_bindir}/mono
%endif
%attr(755,root,root) %{_bindir}/secutil*
%attr(755,root,root) %{_bindir}/chktrust*
%attr(755,root,root) %{_bindir}/signcode*
%attr(755,root,root) %{_bindir}/sn*
%attr(755,root,root) %{_bindir}/MakeCert*
%attr(755,root,root) %{_bindir}/makecert*
%attr(755,root,root) %{_bindir}/cert*
%attr(755,root,root) %{_bindir}/setreg*
%attr(755,root,root) %{_bindir}/gacutil*
%attr(755,root,root) %{_libdir}/lib*.so.*.*
%attr(755,root,root) %{_libdir}/*.dll
%attr(755,root,root) %{_libdir}/mono/*.*/*.dll
%{_mandir}/man5/mono-config.5*
%{_mandir}/man1/mint.1*
%{_mandir}/man1/mono.1*
%{_mandir}/man1/sn.1*
%{_mandir}/man1/cert*.1*
%{_mandir}/man1/makecert.1*
%{_mandir}/man1/secutil.1*
%{_mandir}/man1/signcode.1*
%{_mandir}/man1/setreg.1*
%{_mandir}/man1/chktrust.1*
%{_mandir}/man1/gacutil.1*
#%{_mandir}/man1/oldmono.1*
%dir %{_libdir}/mono
%dir %{_libdir}/mono/1.0
%dir %{_libdir}/mono/2.0
%{_libdir}/mono/gac
%dir %{_sysconfdir}/mono
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/mono/config
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/mono/machine.config
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/mono/browscap.ini
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/mono/DefaultWsdlHelpGenerator.aspx

%files jay
%defattr(644,root,root,755)
%doc mcs-*/jay/{ACKNOWLEDGEMENTS,ChangeLog,NEW_FEATURES,NOTES,README,README.jay}
%attr(755,root,root) %{_bindir}/jay
%dir %{_datadir}/jay
%{_datadir}/jay/skeleton*
%{_mandir}/man1/jay.1*

%files compat-links
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/resgen

%files devel
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README pld-doc/*
%attr(755,root,root) %{_bindir}/monodis
%attr(755,root,root) %{_bindir}/mono-find*
%attr(755,root,root) %{_bindir}/xsd*
%attr(755,root,root) %{_bindir}/monograph
%attr(755,root,root) %{_bindir}/monoresgen*
%attr(755,root,root) %{_bindir}/pedump
%attr(755,root,root) %{_bindir}/wsdl*
%attr(755,root,root) %{_bindir}/genxs*
%attr(755,root,root) %{_bindir}/sqlsharp*
%attr(755,root,root) %{_bindir}/disco*
%attr(755,root,root) %{_bindir}/cilc*
%attr(755,root,root) %{_bindir}/al*
%attr(755,root,root) %{_bindir}/soapsuds*
%attr(755,root,root) %{_bindir}/monop*
%attr(755,root,root) %{_libdir}/lib*.so
%{_libdir}/lib*.la
%{_datadir}/%{name}
%{_pkgconfigdir}/*.pc
%{_includedir}/%{name}
%{_mandir}/man1/cilc.1*
%{_mandir}/man1/genxs.1*
%{_mandir}/man1/monoburg.1*
%{_mandir}/man1/monodis.1*
%{_mandir}/man1/monostyle.1*
%{_mandir}/man1/sqlsharp.1*
%{_mandir}/man1/wsdl.1*
%{_mandir}/man1/soapsuds.1*
%{_mandir}/man1/disco.1*
%{_mandir}/man1/monop.1*
%{_mandir}/man1/xsd.1*

%files csharp
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/mcs
%attr(755,root,root) %{_bindir}/gmcs
%attr(755,root,root) %{_libdir}/mono/1.0/mcs.exe
%attr(755,root,root) %{_libdir}/mono/2.0/gmcs.exe
%{_mandir}/man1/mcs.1*

%files basic
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/mbas
%attr(755,root,root) %{_libdir}/mono/1.0/mbas.exe

%files ilasm
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/ilasm*
%{_mandir}/man1/ilasm.1*

%files static
%defattr(644,root,root,755)
%{_libdir}/lib*.a
