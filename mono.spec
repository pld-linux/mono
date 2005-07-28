#
# Conditional build:
%bcond_without	nptl		# don't use TLS (which effectively requires NPTL libs)
%bcond_without	static_libs	# don't build static libraries
#
%define		_glibver	2.4
Summary:	Common Language Infrastructure implementation
Summary(pl):	Implementacja Common Language Infrastructure
Name:		mono
Version:	1.1.8.3
Release:	1
License:	GPL/LGPL/MIT
Group:		Development/Languages
#Source0Download: http://www.mono-project.com/Downloads
Source0:	http://www.go-mono.com/sources/mono-1.1/%{name}-%{version}.tar.gz
# Source0-md5:	5aefdc915cbd6ed84834692f59b92080
Patch0:		%{name}-nolibs.patch
Patch1:		%{name}-alpha-float.patch
Patch2:		%{name}-mint.patch
Patch3:		%{name}-sonames.patch
URL:		http://www.mono-project.com/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	bison
BuildRequires:	glib2-devel >= %{_glibver}
BuildRequires:	libtool
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 1.213
ExclusiveArch:	%{ix86} %{x8664} arm hppa ppc s390 s390x sparc sparcv9 sparc64
# alpha still broken, mips/ia64/m68k disabled in configure
# note: plain i386 is not supported; mono uses cmpxchg/xadd which require i486
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

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

%{?with_nptl:This version was build with TLS __thread.}

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

%{?with_nptl:Ta wersja zosta³a zbudowana z TLS __thread.}

%package devel
Summary:	Development resources for mono
Summary(pl):	Zasoby programisty do mono
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	glib2-devel >= %{_glibver}

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

%package jscript
Summary:	jscript compiler for mono
Summary(pl):	Kompilator jscript dla mono
Group:		Development/Languages
Requires:	%{name}-devel = %{version}-%{release}

%description jscript
jscript compiler for mono.

%description jscript -l pl
Kompilator jscript dla mono.

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
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1

# workaround for variable name disallowed by new pkgconfig
echo 'm4_pattern_allow(PKG_PATH)' > acinclude.m4

%build
cp -f /usr/share/automake/config.sub .
cp -f /usr/share/automake/config.sub libgc
%{__libtoolize}
%{__aclocal}
%{__autoheader}
%{__autoconf}
%{__automake}
cd libgc
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__automake}
cd ..

%configure \
	--enable-fast-install \
	%{?with_nptl:--with-tls=__thread} \
	%{!?with_nptl:--with-tls=pthread} \
	%{!?with_static_libs:--enable-static=no} \
	--with-preview=yes \
	--with-icu=no \
	--with-jit=yes \
	--with-gc=included

# mint uses heap to make trampolines, which need to be executable
# there is mprotect(...,PROT_EXEC) for ppc/s390, but not used
# (ifdef NEED_MPROTECT, which is never defined)
# in fact the flag should be "-Wl,-z,execheap" for libmint, but:
# -z execheap doesn't seem to do anything currently
# -z execstack for library makes only stack executable, but not heap
%{__make} \
	mint_LDFLAGS="-Wl,-z,execheap -Wl,-z,execstack"

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

mv -f $RPM_BUILD_ROOT%{_prefix}/man/man1/* $RPM_BUILD_ROOT%{_mandir}/man1
rm -f $RPM_BUILD_ROOT%{_datadir}/jay/[A-Z]*

# this way we can run rpmbuild -bi several times, and directories
# have more meaningful name.
rm -rf pld-doc
mkdir -p pld-doc/{webpage,notes}
cp -a web/* pld-doc/webpage
cp -a docs/* pld-doc/notes
rm -f pld-doc/*/Makefile*

rm -rf $RPM_BUILD_ROOT%{_datadir}/libgc-mono

%clean
rm -rf $RPM_BUILD_ROOT

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%ifarch %{ix86} ppc sparc %{x8664}
%attr(755,root,root) %{_bindir}/mono
%else
%attr(755,root,root) %{_bindir}/mint
%endif
%attr(755,root,root) %{_bindir}/cert*
%attr(755,root,root) %{_bindir}/chktrust*
%attr(755,root,root) %{_bindir}/gacutil*
%attr(755,root,root) %{_bindir}/makecert*
%attr(755,root,root) %{_bindir}/mkbundle*
%attr(755,root,root) %{_bindir}/secutil*
%attr(755,root,root) %{_bindir}/setreg*
%attr(755,root,root) %{_bindir}/signcode*
%attr(755,root,root) %{_bindir}/sn*
%attr(755,root,root) %{_bindir}/mono-service
%attr(755,root,root) %{_bindir}/caspol
%attr(755,root,root) %{_libdir}/lib*.so.*.*
%attr(755,root,root) %{_libdir}/libMonoPosixHelper.so
%attr(755,root,root) %{_libdir}/libikvm-native.so
%dir /usr/lib/mono
%dir /usr/lib/mono/1.0
%dir /usr/lib/mono/2.0
%attr(755,root,root) /usr/lib/mono/*.*/*.dll
%attr(755,root,root) /usr/lib/mono/1.0/cert*
%attr(755,root,root) /usr/lib/mono/1.0/chktrust*
%attr(755,root,root) /usr/lib/mono/1.0/gacutil*
%attr(755,root,root) /usr/lib/mono/1.0/MakeCert*
%attr(755,root,root) /usr/lib/mono/1.0/mkbundle*
%attr(755,root,root) /usr/lib/mono/1.0/secutil*
%attr(755,root,root) /usr/lib/mono/1.0/setreg*
%attr(755,root,root) /usr/lib/mono/1.0/signcode*
%attr(755,root,root) /usr/lib/mono/1.0/sn*
%attr(755,root,root) /usr/lib/mono/1.0/caspol*
%attr(755,root,root) /usr/lib/mono/1.0/mono-service*
%{_mandir}/man1/cert*.1*
%{_mandir}/man1/chktrust.1*
%{_mandir}/man1/gacutil.1*
%{_mandir}/man1/makecert.1*
%{_mandir}/man1/mkbundle.1*
%{_mandir}/man1/mint.1*
%{_mandir}/man1/mono.1*
%{_mandir}/man1/mono-service.1*
%{_mandir}/man1/secutil.1*
%{_mandir}/man1/setreg.1*
%{_mandir}/man1/signcode.1*
%{_mandir}/man1/sn.1*
%{_mandir}/man1/permview.1*
%{_mandir}/man5/mono-config.5*
/usr/lib/mono/gac
%dir %{_sysconfdir}/mono
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/mono/config
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/mono/browscap.ini
%dir %{_sysconfdir}/mono/1.0
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/mono/1.0/machine.config
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/mono/1.0/DefaultWsdlHelpGenerator.aspx
%dir %{_sysconfdir}/mono/2.0
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/mono/2.0/machine.config
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/mono/2.0/DefaultWsdlHelpGenerator.aspx

%files jay
%defattr(644,root,root,755)
%doc mcs/jay/{ACKNOWLEDGEMENTS,ChangeLog,NEW_FEATURES,NOTES,README,README.jay}
%attr(755,root,root) %{_bindir}/jay
%dir %{_datadir}/jay
%{_datadir}/jay/skeleton*
%{_mandir}/man1/jay.1*

# TODO: probably Microsoft.JScript.dll & Co. should be here
%files jscript
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/mjs
%attr(755,root,root) /usr/lib/mono/1.0/mjs*

%files compat-links
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/resgen

%files devel
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README pld-doc/*
%attr(755,root,root) %{_bindir}/al*
%attr(755,root,root) %{_bindir}/cilc*
%attr(755,root,root) %{_bindir}/disco*
%attr(755,root,root) %{_bindir}/dtd2xsd
%attr(755,root,root) %{_bindir}/genxs*
%attr(755,root,root) %{_bindir}/macpack
%attr(755,root,root) %{_bindir}/monodiet
%attr(755,root,root) %{_bindir}/monodis
%attr(755,root,root) %{_bindir}/mono-find*
%attr(755,root,root) %{_bindir}/monograph
%attr(755,root,root) %{_bindir}/monop*
%attr(755,root,root) %{_bindir}/mono-shlib-cop*
%attr(755,root,root) %{_bindir}/pedump
%attr(755,root,root) %{_bindir}/permview
%attr(755,root,root) %{_bindir}/prj2make
%attr(755,root,root) %{_bindir}/soapsuds*
%attr(755,root,root) %{_bindir}/sqlsharp*
%attr(755,root,root) %{_bindir}/wsdl*
%attr(755,root,root) %{_bindir}/xsd*
%attr(755,root,root) %{_libdir}/libmono.so
%attr(755,root,root) %{_libdir}/libmono-profiler-cov.so
%attr(755,root,root) /usr/lib/mono/1.0/al*
%attr(755,root,root) /usr/lib/mono/1.0/browsercaps-updater*
%attr(755,root,root) /usr/lib/mono/1.0/cilc*
%attr(755,root,root) /usr/lib/mono/1.0/CorCompare*
%attr(755,root,root) /usr/lib/mono/1.0/disco*
%attr(755,root,root) /usr/lib/mono/1.0/dtd2xsd*
%attr(755,root,root) /usr/lib/mono/1.0/genxs*
%attr(755,root,root) /usr/lib/mono/1.0/ictool*
%attr(755,root,root) /usr/lib/mono/1.0/macpack*
%attr(755,root,root) /usr/lib/mono/1.0/mono-api-*
%attr(755,root,root) /usr/lib/mono/1.0/monop*
%attr(755,root,root) /usr/lib/mono/1.0/mono-shlib-cop*
%attr(755,root,root) /usr/lib/mono/1.0/permview*
%attr(755,root,root) /usr/lib/mono/1.0/prj2make*
%attr(755,root,root) /usr/lib/mono/1.0/resgen*
%attr(755,root,root) /usr/lib/mono/1.0/soapsuds*
%attr(755,root,root) /usr/lib/mono/1.0/sqlsharp*
%attr(755,root,root) /usr/lib/mono/1.0/wsdl*
%attr(755,root,root) /usr/lib/mono/1.0/xsd*
%attr(755,root,root) /usr/lib/mono/2.0/mono-api-info*
%attr(755,root,root) /usr/lib/mono/2.0/wsdl*
/usr/lib/mono/*.*/*.dll.mdb
%{_libdir}/lib*.la
%{_datadir}/%{name}
%{_pkgconfigdir}/*.pc
%{_includedir}/%{name}
%{_mandir}/man1/cilc.1*
%{_mandir}/man1/disco.1*
%{_mandir}/man1/dtd2xsd.1*
%{_mandir}/man1/genxs.1*
%{_mandir}/man1/macpack.1*
%{_mandir}/man1/monoburg.1*
%{_mandir}/man1/monodis.1*
%{_mandir}/man1/monop.1*
%{_mandir}/man1/mono-shlib-cop.1*
%{_mandir}/man1/monostyle.1*
%{_mandir}/man1/oldmono.1*
%{_mandir}/man1/prj2make.1*
%{_mandir}/man1/soapsuds.1*
%{_mandir}/man1/sqlsharp.1*
%{_mandir}/man1/wsdl.1*
%{_mandir}/man1/xsd.1*

%files csharp
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/mcs
%attr(755,root,root) %{_bindir}/gmcs
%attr(755,root,root) /usr/lib/mono/1.0/mcs.exe*
%attr(755,root,root) /usr/lib/mono/2.0/gmcs.exe*
%{_mandir}/man1/mcs.1*

%files basic
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/mbas
%attr(755,root,root) /usr/lib/mono/1.0/mbas.exe*

%files ilasm
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/ilasm*
%attr(755,root,root) /usr/lib/mono/1.0/ilasm*
%{_mandir}/man1/ilasm.1*

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/lib*.a
%endif
