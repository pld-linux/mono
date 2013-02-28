#
# NOTE: Makefiles are broken, build could stop long time after first fatal error
# TODO:
#   - cleanup %%doc ./notes from dll/zip/sh/etc.
#
# Conditional build:
%bcond_without	tls		# don't use TLS (which requires recent 2.4.x or 2.6 kernel)
%bcond_without	static_libs	# don't build static libraries
%bcond_with	bootstrap	# don't require mono-devel to find req/prov
%bcond_with	mint		# build mint instead of mono VM (JIT) [broken]
%bcond_with	llvm		# LLVM backend [unfinished, needs unreleased mono-llvm version]

%ifnarch %{ix86} %{x8664} alpha arm ia64 ppc s390 s390x sparc sparcv9 sparc64
# JIT not supported on hppa
%define		with_mint	1
%endif

Summary:	Common Language Infrastructure implementation
Summary(pl.UTF-8):	Implementacja Common Language Infrastructure
Name:		mono
Version:	3.0.5
Release:	1
License:	LGPL v2 (VM), MIT X11/GPL v2 (C# compilers), MIT X11 (classes, tools), GPL v2 (tools)
Group:		Development/Languages
# latest downloads summary at http://download.mono-project.com/sources-stable/
Source0:	http://download.mono-project.com/sources/mono/%{name}-%{version}.tar.bz2
# Source0-md5:	6016eb76f5b7661df53201d016acf977
Patch0:		%{name}-alpha-float.patch
Patch1:		%{name}-mint.patch
Patch2:		%{name}-sonames.patch
Patch3:		%{name}-awk.patch
Patch4:		%{name}-console-no-utf8-bom.patch
Patch5:		%{name}-pc.patch
Patch6:		%{name}-ARG_MAX.patch
Patch7:		%{name}-fix-null-requirement.patch
Patch8:		%{name}-docs-build.patch
Patch9:		%{name}-format-security.patch
URL:		http://www.mono-project.com/
%if %(test -r /dev/random; echo $?)
BuildRequires:	ACCESSIBLE_/dev/random
%endif
BuildRequires:	autoconf
BuildRequires:	automake >= 1:1.9
BuildRequires:	bison
BuildRequires:	gettext-devel
BuildRequires:	libtool
%{!?with_bootstrap:BuildRequires:	mono-csharp}
%{!?with_bootstrap:BuildRequires:	mono-devel >= 1.1.8.3-2}
%{?with_llvm:BuildRequires:	mono-llvm >= 2.11}
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 1.213
BuildRequires:	rpmbuild(monoautodeps)
BuildRequires:	zlib-devel >= 1.2.3
BuildConflicts:	mono-csharp < 2.4
Requires:	zlib >= 1.2.3
Suggests:	binfmt-detector
# for System.Drawing
Suggests:	libgdiplus >= 2.6
Obsoletes:	mono-jscript
ExclusiveArch:	%{ix86} %{x8664} alpha arm hppa ia64 mips ppc s390 s390x sparc sparcv9
# plain i386 is not supported; mono uses cmpxchg/xadd which require i486
ExcludeArch:	i386
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_rpmlibdir	/usr/lib/rpm

# debugger doesn't work with stripped mono
%define         _noautostrip    .*/mono

%define		skip_post_check_so	'.+(libmonosgen|libmono-profiler).+\.so.+'

%if %{with bootstrap}
%define	__mono_provides /bin/true
%define	__mono_requires /bin/true
%else
%define	__mono_provides	%{_rpmlibdir}/mono-find-provides
%define	__mono_requires	%{_rpmlibdir}/mono-find-requires
%endif

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

%{?with_tls:This version was built with TLS __thread.}

%description -l pl.UTF-8
Platforma CLI (Common Language Infrastructure). Microsoft stworzył
nową platformę developerską. Zalety tej platformy to:
- środowisko, które dostarcza garbage collector, wątki oraz
  specyfikację maszyny wirtualnej (The Virtual Execution System, VES),
- bibliotekę klas,
- nowy język, C#. Bardzo podobny do Javy, C# pozwala programistom na
  używanie wszystkich możliwości dostarczanych przez platformę .NET,
- specyfikacja dla kompilatorów, które chcą generować kod
  współpracujący z innymi językami programowania (The Common Language
  Specification: CLS).

%{?with_tls:Ta wersja została zbudowana z TLS __thread.}

%package devel
Summary:	Development resources for mono
Summary(pl.UTF-8):	Zasoby programisty do mono
License:	LGPL (VM), MIT X11 with GPL additions (classes, tools)
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Development resources for mono.

%description devel -l pl.UTF-8
Zasoby programisty dla mono.

%package debug
Summary:	Mono libraries debugging resources
Summary(pl.UTF-8):	Pliki umożliwiające debugowanie bibliotek mono
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description debug
Mono libraries debugging resources.

%description debug -l pl.UTF-8
Pliki umożliwiające debugowanie bibliotek mono.

%package csharp
Summary:	C# compiler for mono
Summary(pl.UTF-8):	Kompilator C# dla mono
License:	MIT or GPL v2
Group:		Development/Languages
Requires:	%{name}-devel = %{version}-%{release}

%description csharp
C# compiler for mono.

%description csharp -l pl.UTF-8
Kompilator C# dla mono.

%package ilasm
Summary:	ILasm compiler for mono
Summary(pl.UTF-8):	Kompilator ILasm dla mono
# implied
License:	MIT X11
Group:		Development/Languages
Requires:	%{name}-devel = %{version}-%{release}
Provides:	ilasm
Obsoletes:	pnet-compiler-ilasm

%description ilasm
ILasm compiler for mono.

%description ilasm -l pl.UTF-8
Kompilator ILasm dla mono.

%package monodoc
Summary:	Documentation for Mono class libraries and tools to produce and edit the documentation
Summary(pl.UTF-8):	Dokumentacja klas Mono wraz z narzędziami do jej generowania i przeglądania
License:	LGPL v2
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}
Provides:	monodoc = %{version}-%{release}
Obsoletes:	monodoc

%description monodoc
This package contains the documentation for the Mono class libraries,
tools to produce and edit the documentation, and a documentation
browser.

%description monodoc -l pl.UTF-8
Ten pakiet zawiera dokumentację klas Mono wraz z narzędziami do jej
generowania i przeglądania.

%package static
Summary:	Static mono library
Summary(pl.UTF-8):	Statyczna biblioteka mono
License:	LGPL v2
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static mono library.

%description static -l pl.UTF-8
Statyczna biblioteka mono.

%package jay
Summary:	Yacc-like parser generator for Java and C#
Summary(pl.UTF-8):	Podobny do Yacca generator parserów dla Javy i C#
License:	BSD
Group:		Development/Tools

%description jay
Yacc-like parser generator for Java and C#.

%description jay -l pl.UTF-8
Podobny do Yacca generator parserów dla Javy i C#.

%package compat-links
Summary:	Mono compatibility links
Summary(pl.UTF-8):	Dowiązania dla kompatybilności
# resgen license
License:	MIT X11
Group:		Development/Languages
Requires:	%{name}-devel = %{version}-%{release}

%description compat-links
This package contains links to binaries with names used in .NET and
dotGNU.

%description compat-links -l pl.UTF-8
Pakiet ten zawiera dowiązania do programów o nazwach używanych w .NET
oraz dotGNU.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1

# for jay
cat >> mcs/build/config-default.make <<'EOF'
CC = %{__cc}
CFLAGS = %{rpmcflags}
EOF

# spurious-executable-perm on source files
find -name '*.[ch]' | xargs chmod a-x

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoheader}
%{__autoconf}
%{__automake}
cd libgc
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__automake}
cd ../eglib
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
cd ..

%{?with_llvm:PATH=%{_libdir}/mono-llvm/bin:$PATH}
# -DUSE_COMPILER_TLS is passed to libgc by main configure, but our
# CPPFLAGS override that CPPFLAGS
CPPFLAGS="-DUSE_LIBC_PRIVATE_SYMBOLS -DUSE_COMPILER_TLS"
# note: don't enable moonlight here (yet) - it doesn't add anything to package
# but disables some utils (it's meant for stripped mono build for moonlight)
%configure \
	%{!?with_static_libs:--disable-static} \
	--enable-fast-install \
%if %{with llvm}
	--enable-llvm \
	--enable-loadedllvm \
%endif
	--enable-parallel-mark \
%ifarch %{x8664} ppc64 s390x sparc64
	--enable-big-arrays \
	--with-large-heap \
%endif
	--with-gc=included \
	--without-icu \
	--with-interp%{!?with_mint:=no} \
	--with-jit%{?with_mint:=no} \
	--without-monotouch \
	--with-profile4 \
	--with-sgen \
	--with-tls=%{?with_tls:__thread}%{!?with_tls:pthread}

# mint uses heap to make trampolines, which need to be executable
# there is mprotect(...,PROT_EXEC) for ppc/s390, but not used
# (ifdef NEED_MPROTECT, which is never defined)
# in fact the flag should be "-Wl,-z,execheap" for libmint, but:
# -z execheap doesn't seem to do anything currently;
# -z execstack for library makes only stack executable, but not heap.
# V=1 because --disable-silent-rules doesn't work.
%{__make} -j1 \
	V=1 \
	mint_LDFLAGS="-Wl,-z,execheap -Wl,-z,execstack"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_rpmlibdir},%{_datadir}/.mono/keypairs}

%{__make} -j 1 install \
	DESTDIR=$RPM_BUILD_ROOT

strip --strip-debug $RPM_BUILD_ROOT%{_bindir}/mono

%{__make} -C mcs/jay -j 1 install \
	DESTDIR=$RPM_BUILD_ROOT
# leave only skeleton
%{__rm} $RPM_BUILD_ROOT%{_datadir}/jay/[ANR]*

# this way we can run rpmbuild -bi several times, and directories
# have more meaningful name.
%{__rm} -rf pld-doc
#install -d pld-doc/{webpage,notes}
install -d pld-doc/notes
#cp -a web/* pld-doc/webpage
cp -a docs/* pld-doc/notes
%{__rm} pld-doc/*/Makefile*

%{__rm} -r $RPM_BUILD_ROOT%{_datadir}/libgc-mono

mv -f $RPM_BUILD_ROOT%{_bindir}/mono-find-* $RPM_BUILD_ROOT%{_rpmlibdir}

# loadable modules
%{__rm} $RPM_BUILD_ROOT%{_libdir}/lib{MonoPosixHelper,MonoSupportW,ikvm-native}.la
%if %{with static_libs}
%{__rm} $RPM_BUILD_ROOT%{_libdir}/lib{MonoPosixHelper,MonoSupportW,ikvm-native}.a
%endif

%find_lang mcs

%clean
rm -rf $RPM_BUILD_ROOT

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog LICENSE NEWS README pld-doc/*
%if %{with mint}
%attr(755,root,root) %{_bindir}/mint
%else
%attr(755,root,root) %{_bindir}/mono
%endif
%attr(755,root,root) %{_bindir}/caspol
%attr(755,root,root) %{_bindir}/cert2spc
%attr(755,root,root) %{_bindir}/certmgr
%attr(755,root,root) %{_bindir}/chktrust
%attr(755,root,root) %{_bindir}/crlupdate
%attr(755,root,root) %{_bindir}/dtd2rng
%attr(755,root,root) %{_bindir}/gacutil
%attr(755,root,root) %{_bindir}/gacutil2
%attr(755,root,root) %{_bindir}/httpcfg
%attr(755,root,root) %{_bindir}/installvst
%attr(755,root,root) %{_bindir}/makecert
%attr(755,root,root) %{_bindir}/mconfig
%attr(755,root,root) %{_bindir}/mdbrebase
%attr(755,root,root) %{_bindir}/mkbundle
%attr(755,root,root) %{_bindir}/mono-configuration-crypto
%attr(755,root,root) %{_bindir}/mono-service
%attr(755,root,root) %{_bindir}/mono-service2
%attr(755,root,root) %{_bindir}/mono-test-install
%attr(755,root,root) %{_bindir}/mono-xmltool
%attr(755,root,root) %{_bindir}/mozroots
%attr(755,root,root) %{_bindir}/mprof-report
%attr(755,root,root) %{_bindir}/pdb2mdb
%attr(755,root,root) %{_bindir}/secutil
%attr(755,root,root) %{_bindir}/setreg
%attr(755,root,root) %{_bindir}/sgen
%attr(755,root,root) %{_bindir}/signcode
%attr(755,root,root) %{_bindir}/sn
%attr(755,root,root) %{_bindir}/sqlmetal
%attr(755,root,root) %{_bindir}/svcutil
%if %{with mint}
%attr(755,root,root) %{_libdir}/libmint.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libmint.so.0
%else
%attr(755,root,root) %{_libdir}/libmono-2.0.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libmono-2.0.so.1
%attr(755,root,root) %{_libdir}/libmonosgen-2.0.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libmonosgen-2.0.so.0
%endif
%attr(755,root,root) %{_libdir}/libmono-profiler-aot.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libmono-profiler-aot.so.0
%attr(755,root,root) %{_libdir}/libmono-profiler-cov.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libmono-profiler-cov.so.0
%attr(755,root,root) %{_libdir}/libmono-profiler-iomap.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libmono-profiler-iomap.so.0
%attr(755,root,root) %{_libdir}/libmono-profiler-log.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libmono-profiler-log.so.0
%attr(755,root,root) %{_libdir}/libMonoPosixHelper.so
%attr(755,root,root) %{_libdir}/libMonoSupportW.so
%attr(755,root,root) %{_libdir}/libikvm-native.so
%dir %{_prefix}/lib/mono
%dir %{_prefix}/lib/mono/2.0
%attr(755,root,root) %{_prefix}/lib/mono/2.0/RabbitMQ.Client.Apigen.exe
%attr(755,root,root) %{_prefix}/lib/mono/2.0/gacutil.exe
%attr(755,root,root) %{_prefix}/lib/mono/2.0/mkbundle.exe
%attr(755,root,root) %{_prefix}/lib/mono/2.0/mono-service.exe
%attr(755,root,root) %{_prefix}/lib/mono/2.0/xsd.exe
%{_prefix}/lib/mono/2.0/*.dll
%attr(755,root,root) %{_prefix}/lib/mono/2.0/mscorlib.dll.so
%dir %{_prefix}/lib/mono/3.5
%{_prefix}/lib/mono/3.5/*.dll
%dir %{_prefix}/lib/mono/4.0
%attr(755,root,root) %{_prefix}/lib/mono/4.0/RabbitMQ.Client.Apigen.exe
%{_prefix}/lib/mono/4.0/*.dll
%dir %{_prefix}/lib/mono/4.5
%attr(755,root,root) %{_prefix}/lib/mono/4.5/RabbitMQ.Client.Apigen.exe
%attr(755,root,root) %{_prefix}/lib/mono/4.5/browsercaps-updater.exe
%attr(755,root,root) %{_prefix}/lib/mono/4.5/caspol.exe
%attr(755,root,root) %{_prefix}/lib/mono/4.5/cert2spc.exe
%attr(755,root,root) %{_prefix}/lib/mono/4.5/certmgr.exe
%attr(755,root,root) %{_prefix}/lib/mono/4.5/chktrust.exe
%attr(755,root,root) %{_prefix}/lib/mono/4.5/crlupdate.exe
%attr(755,root,root) %{_prefix}/lib/mono/4.5/dtd2rng.exe
%attr(755,root,root) %{_prefix}/lib/mono/4.5/gacutil.exe
%attr(755,root,root) %{_prefix}/lib/mono/4.5/httpcfg.exe
%attr(755,root,root) %{_prefix}/lib/mono/4.5/installutil.exe
%attr(755,root,root) %{_prefix}/lib/mono/4.5/makecert.exe
%attr(755,root,root) %{_prefix}/lib/mono/4.5/mconfig.exe
%attr(755,root,root) %{_prefix}/lib/mono/4.5/mdbrebase.exe
%attr(755,root,root) %{_prefix}/lib/mono/4.5/mkbundle.exe
%attr(755,root,root) %{_prefix}/lib/mono/4.5/mono-service.exe
%attr(755,root,root) %{_prefix}/lib/mono/4.5/mozroots.exe
%attr(755,root,root) %{_prefix}/lib/mono/4.5/pdb2mdb.exe
%attr(755,root,root) %{_prefix}/lib/mono/4.5/secutil.exe
%attr(755,root,root) %{_prefix}/lib/mono/4.5/setreg.exe
%attr(755,root,root) %{_prefix}/lib/mono/4.5/sgen.exe
%attr(755,root,root) %{_prefix}/lib/mono/4.5/signcode.exe
%attr(755,root,root) %{_prefix}/lib/mono/4.5/sn.exe
%attr(755,root,root) %{_prefix}/lib/mono/4.5/sqlmetal.exe
%{_prefix}/lib/mono/4.5/sqlmetal.exe.config
%attr(755,root,root) %{_prefix}/lib/mono/4.5/svcutil.exe
%attr(755,root,root) %{_prefix}/lib/mono/4.5/xsd.exe
%{_prefix}/lib/mono/4.5/*.dll
%attr(755,root,root) %{_prefix}/lib/mono/4.5/mscorlib.dll.so
%dir %{_prefix}/lib/mono/compat-2.0
%{_prefix}/lib/mono/compat-2.0/*.dll
%dir %{_prefix}/lib/mono/mono-configuration-crypto
%dir %{_prefix}/lib/mono/mono-configuration-crypto/4.5
%{_prefix}/lib/mono/mono-configuration-crypto/4.5/Mono.Configuration.Crypto.dll
%attr(755,root,root) %{_prefix}/lib/mono/mono-configuration-crypto/4.5/mono-configuration-crypto.exe
%exclude %{_prefix}/lib/mono/gac/monodoc
%{_prefix}/lib/mono/gac
%exclude %{_prefix}/lib/mono/gac/*/*/*.mdb
%{_prefix}/lib/mono-source-libs
%dir %{_datadir}/.mono
%dir %{_datadir}/.mono/keypairs
%{_mandir}/man1/cert2spc.1*
%{_mandir}/man1/certmgr.1*
%{_mandir}/man1/chktrust.1*
%{_mandir}/man1/crlupdate.1*
%{_mandir}/man1/gacutil.1*
%{_mandir}/man1/httpcfg.1*
%{_mandir}/man1/makecert.1*
%{_mandir}/man1/mconfig.1*
%{_mandir}/man1/mkbundle.1*
%{_mandir}/man1/mono.1*
%{_mandir}/man1/mono-configuration-crypto.1*
%{_mandir}/man1/mono-service.1*
%{_mandir}/man1/mozroots.1*
%{_mandir}/man1/mprof-report.1*
%{_mandir}/man1/pdb2mdb.1*
%{_mandir}/man1/secutil.1*
%{_mandir}/man1/setreg.1*
%{_mandir}/man1/sgen.1*
%{_mandir}/man1/signcode.1*
%{_mandir}/man1/sn.1*
%{_mandir}/man5/mono-config.5*
%dir %{_sysconfdir}/mono
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/mono/browscap.ini
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/mono/config
%dir %{_sysconfdir}/mono/mconfig
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/mono/mconfig/config.xml
%dir %{_sysconfdir}/mono/2.0
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/mono/2.0/DefaultWsdlHelpGenerator.aspx
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/mono/2.0/machine.config
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/mono/2.0/settings.map
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/mono/2.0/web.config
%dir %{_sysconfdir}/mono/2.0/Browsers
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/mono/2.0/Browsers/Compat.browser
%dir %{_sysconfdir}/mono/4.0
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/mono/4.0/DefaultWsdlHelpGenerator.aspx
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/mono/4.0/machine.config
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/mono/4.0/settings.map
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/mono/4.0/web.config
%dir %{_sysconfdir}/mono/4.5
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/mono/4.5/DefaultWsdlHelpGenerator.aspx
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/mono/4.5/machine.config
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/mono/4.5/settings.map
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/mono/4.5/web.config

%files jay
%defattr(644,root,root,755)
%doc mcs/jay/{ACKNOWLEDGEMENTS,ChangeLog,NEW_FEATURES,NOTES,README,README.jay}
%attr(755,root,root) %{_bindir}/jay
%dir %{_datadir}/jay
%{_datadir}/jay/skeleton*
%{_mandir}/man1/jay.1*

%files compat-links
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/resgen
%attr(755,root,root) %{_bindir}/resgen2

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/al
%attr(755,root,root) %{_bindir}/al2
%attr(755,root,root) %{_bindir}/cccheck
%attr(755,root,root) %{_bindir}/ccrewrite
%attr(755,root,root) %{_bindir}/disco
%attr(755,root,root) %{_bindir}/dtd2xsd
%attr(755,root,root) %{_bindir}/genxs
%attr(755,root,root) %{_bindir}/macpack
%attr(755,root,root) %{_bindir}/mono-api-info
%attr(755,root,root) %{_bindir}/mono-cil-strip
%attr(755,root,root) %{_bindir}/mono-heapviz
%attr(755,root,root) %{_bindir}/mono-sgen
%attr(755,root,root) %{_bindir}/monodis
%attr(755,root,root) %{_bindir}/monograph
%attr(755,root,root) %{_bindir}/monolinker
%attr(755,root,root) %{_bindir}/monop
%attr(755,root,root) %{_bindir}/monop2
%attr(755,root,root) %{_bindir}/mono-shlib-cop
%attr(755,root,root) %{_bindir}/mono-gdb.py
%attr(755,root,root) %{_bindir}/mono-sgen-gdb.py
%attr(755,root,root) %{_bindir}/lc
%attr(755,root,root) %{_bindir}/nunit-console
%attr(755,root,root) %{_bindir}/nunit-console2
%attr(755,root,root) %{_bindir}/nunit-console4
%attr(755,root,root) %{_bindir}/pedump
%attr(755,root,root) %{_bindir}/peverify
%attr(755,root,root) %{_bindir}/permview
%attr(755,root,root) %{_bindir}/prj2make
%attr(755,root,root) %{_bindir}/soapsuds
%attr(755,root,root) %{_bindir}/sqlsharp
%attr(755,root,root) %{_bindir}/wsdl
%attr(755,root,root) %{_bindir}/wsdl2
%attr(755,root,root) %{_bindir}/xbuild
%attr(755,root,root) %{_bindir}/xsd
%if %{with mint}
%attr(755,root,root) %{_libdir}/libmint.so
%{_libdir}/libmint.la
%else
%attr(755,root,root) %{_libdir}/libmono-2.0.so
%attr(755,root,root) %{_libdir}/libmonosgen-2.0.so
%{_libdir}/libmono-2.0.la
%{_libdir}/libmonosgen-2.0.la
%endif
%attr(755,root,root) %{_libdir}/libmono-profiler-aot.so
%attr(755,root,root) %{_libdir}/libmono-profiler-cov.so
%attr(755,root,root) %{_libdir}/libmono-profiler-iomap.so
%attr(755,root,root) %{_libdir}/libmono-profiler-log.so
%{_libdir}/libmono-profiler-aot.la
%{_libdir}/libmono-profiler-cov.la
%{_libdir}/libmono-profiler-iomap.la
%{_libdir}/libmono-profiler-log.la
%attr(755,root,root) %{_prefix}/lib/mono/2.0/al.exe
%attr(755,root,root) %{_prefix}/lib/mono/2.0/culevel.exe
%attr(755,root,root) %{_prefix}/lib/mono/2.0/genxs.exe
%attr(755,root,root) %{_prefix}/lib/mono/2.0/monolinker.exe
%attr(755,root,root) %{_prefix}/lib/mono/2.0/monop.exe
%attr(755,root,root) %{_prefix}/lib/mono/2.0/nunit-console.exe
%{_prefix}/lib/mono/2.0/nunit-console.exe.config
%attr(755,root,root) %{_prefix}/lib/mono/2.0/resgen.exe
%attr(755,root,root) %{_prefix}/lib/mono/2.0/wsdl.exe
%attr(755,root,root) %{_prefix}/lib/mono/2.0/xbuild.exe
%{_prefix}/lib/mono/2.0/xbuild.rsp
%{_prefix}/lib/mono/2.0/MSBuild
%{_prefix}/lib/mono/2.0/Microsoft.Build.xsd
%{_prefix}/lib/mono/2.0/Microsoft.CSharp.targets
%{_prefix}/lib/mono/2.0/Microsoft.Common.targets
%{_prefix}/lib/mono/2.0/Microsoft.Common.tasks
%{_prefix}/lib/mono/2.0/Microsoft.VisualBasic.targets
%attr(755,root,root) %{_prefix}/lib/mono/3.5/xbuild.exe
%{_prefix}/lib/mono/3.5/xbuild.rsp
%{_prefix}/lib/mono/3.5/MSBuild
%{_prefix}/lib/mono/3.5/Microsoft.Build.xsd
%{_prefix}/lib/mono/3.5/Microsoft.CSharp.targets
%{_prefix}/lib/mono/3.5/Microsoft.Common.targets
%{_prefix}/lib/mono/3.5/Microsoft.Common.tasks
%{_prefix}/lib/mono/3.5/Microsoft.VisualBasic.targets
%{_prefix}/lib/mono/4.0/MSBuild
%{_prefix}/lib/mono/4.0/Microsoft.Build.xsd
%{_prefix}/lib/mono/4.0/Microsoft.CSharp.targets
%{_prefix}/lib/mono/4.0/Microsoft.Common.targets
%{_prefix}/lib/mono/4.0/Microsoft.Common.tasks
%{_prefix}/lib/mono/4.0/Microsoft.VisualBasic.targets
%attr(755,root,root) %{_prefix}/lib/mono/4.5/al.exe
%attr(755,root,root) %{_prefix}/lib/mono/4.5/cccheck.exe
%attr(755,root,root) %{_prefix}/lib/mono/4.5/ccrewrite.exe
%attr(755,root,root) %{_prefix}/lib/mono/4.5/culevel.exe
%attr(755,root,root) %{_prefix}/lib/mono/4.5/disco.exe
%attr(755,root,root) %{_prefix}/lib/mono/4.5/dtd2xsd.exe
%attr(755,root,root) %{_prefix}/lib/mono/4.5/genxs.exe
%attr(755,root,root) %{_prefix}/lib/mono/4.5/ictool.exe
%attr(755,root,root) %{_prefix}/lib/mono/4.5/installvst.exe
%attr(755,root,root) %{_prefix}/lib/mono/4.5/lc.exe
%attr(755,root,root) %{_prefix}/lib/mono/4.5/macpack.exe
%attr(755,root,root) %{_prefix}/lib/mono/4.5/mcs.exe
%attr(755,root,root) %{_prefix}/lib/mono/4.5/mcs.exe.so
%attr(755,root,root) %{_prefix}/lib/mono/4.5/mono-api-info.exe
%attr(755,root,root) %{_prefix}/lib/mono/4.5/mono-cil-strip.exe
%attr(755,root,root) %{_prefix}/lib/mono/4.5/mono-shlib-cop.exe
%{_prefix}/lib/mono/4.5/mono-shlib-cop.exe.config
%attr(755,root,root) %{_prefix}/lib/mono/4.5/mono-xmltool.exe
%attr(755,root,root) %{_prefix}/lib/mono/4.5/monolinker.exe
%attr(755,root,root) %{_prefix}/lib/mono/4.5/monop.exe
%attr(755,root,root) %{_prefix}/lib/mono/4.5/nunit-console.exe
%{_prefix}/lib/mono/4.5/nunit-console.exe.config
%attr(755,root,root) %{_prefix}/lib/mono/4.5/permview.exe
%attr(755,root,root) %{_prefix}/lib/mono/4.5/resgen.exe
%attr(755,root,root) %{_prefix}/lib/mono/4.5/soapsuds.exe
%attr(755,root,root) %{_prefix}/lib/mono/4.5/sqlsharp.exe
%attr(755,root,root) %{_prefix}/lib/mono/4.5/wsdl.exe
%attr(755,root,root) %{_prefix}/lib/mono/4.5/xbuild.exe
%{_prefix}/lib/mono/4.5/xbuild.rsp
%{_prefix}/lib/mono/xbuild
%{_prefix}/lib/mono/xbuild-frameworks
%{_datadir}/mono-2.0
%attr(755,root,root) %{_rpmlibdir}/mono-find-provides
%attr(755,root,root) %{_rpmlibdir}/mono-find-requires
%{_pkgconfigdir}/aspnetwebstack.pc
%{_pkgconfigdir}/cecil.pc
%{_pkgconfigdir}/dotnet.pc
%{_pkgconfigdir}/dotnet35.pc
%if %{with mint}
%{_pkgconfigdir}/mint.pc
%else
%{_pkgconfigdir}/mono.pc
%endif
%{_pkgconfigdir}/mono-2.pc
%{_pkgconfigdir}/mono-cairo.pc
%{_pkgconfigdir}/mono-nunit.pc
%{_pkgconfigdir}/mono-lineeditor.pc
%{_pkgconfigdir}/mono-options.pc
%{_pkgconfigdir}/mono.web.pc
%{_pkgconfigdir}/monosgen-2.pc
%{_pkgconfigdir}/reactive.pc
%{_pkgconfigdir}/system.web.extensions.design_1.0.pc
%{_pkgconfigdir}/system.web.extensions_1.0.pc
%{_pkgconfigdir}/system.web.mvc.pc
%{_pkgconfigdir}/system.web.mvc2.pc
%{_pkgconfigdir}/system.web.mvc3.pc
%{_pkgconfigdir}/wcf.pc
%{_includedir}/%{name}-2.0
%{_mandir}/man1/al.1*
%{_mandir}/man1/cccheck.1*
%{_mandir}/man1/ccrewrite.1*
%{_mandir}/man1/cilc.1*
%{_mandir}/man1/disco.1*
%{_mandir}/man1/dtd2xsd.1*
%{_mandir}/man1/genxs.1*
%{_mandir}/man1/lc.1*
%{_mandir}/man1/macpack.1*
%{_mandir}/man1/mono-api-info.1*
%{_mandir}/man1/mono-cil-strip.1*
%{_mandir}/man1/mono-shlib-cop.1*
%{_mandir}/man1/mono-xmltool.1*
%{_mandir}/man1/monodis.1*
%{_mandir}/man1/monolinker.1*
%{_mandir}/man1/monop.1*
%{_mandir}/man1/permview.1*
%{_mandir}/man1/prj2make.1*
%{_mandir}/man1/resgen.1*
%{_mandir}/man1/soapsuds.1*
%{_mandir}/man1/sqlsharp.1*
%{_mandir}/man1/wsdl.1*
%{_mandir}/man1/xbuild.1*
%{_mandir}/man1/xsd.1*

%files debug
%defattr(644,root,root,755)
%{_prefix}/lib/mono/2.0/*.mdb
%{_prefix}/lib/mono/3.5/*.mdb
%{_prefix}/lib/mono/4.5/*.mdb
%{_prefix}/lib/mono/gac/*/*/*.mdb
%{_prefix}/lib/mono/mono-configuration-crypto/4.5/*.mdb

%files csharp -f mcs.lang
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/csharp
%attr(755,root,root) %{_bindir}/dmcs
%attr(755,root,root) %{_bindir}/gmcs
%attr(755,root,root) %{_bindir}/mcs
%attr(755,root,root) %{_prefix}/lib/mono/4.5/csharp.exe
%{_mandir}/man1/mcs.1*
%{_mandir}/man1/csharp.1*

%files ilasm
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/ilasm
%attr(755,root,root) %{_prefix}/lib/mono/2.0/ilasm.exe
%attr(755,root,root) %{_prefix}/lib/mono/4.5/ilasm.exe
%{_mandir}/man1/ilasm.1*

%files monodoc
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/mdassembler
%attr(755,root,root) %{_bindir}/mdoc*
%attr(755,root,root) %{_bindir}/mod
%attr(755,root,root) %{_bindir}/monodocer
%attr(755,root,root) %{_bindir}/monodocs2html
%attr(755,root,root) %{_bindir}/monodocs2slashdoc
%attr(755,root,root) %{_bindir}/mdvalidater
%attr(755,root,root) %{_prefix}/lib/mono/4.5/mdoc.exe
%attr(755,root,root) %{_prefix}/lib/mono/4.5/mod.exe
%attr(755,root,root) %{_prefix}/lib/mono/monodoc/monodoc.dll
%exclude %{_prefix}/lib/mono/gac/monodoc/*/*.mdb
%{_prefix}/lib/mono/gac/monodoc
%dir %{_prefix}/lib/mono/monodoc
%dir %{_prefix}/lib/monodoc
%{_prefix}/lib/monodoc/sources
%{_prefix}/lib/monodoc/monodoc.xml
%{_pkgconfigdir}/monodoc.pc
%{_mandir}/man1/mdassembler.1*
%{_mandir}/man1/mdoc*.1*
%{_mandir}/man1/monodocer.1*
%{_mandir}/man1/monodocs2html.1*
%{_mandir}/man1/mdvalidater.1*
%{_mandir}/man5/mdoc.5*

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%if %{with mint}
%{_libdir}/libmint.a
%else
%{_libdir}/libmono-2.0.a
%{_libdir}/libmonosgen-2.0.a
%endif
%{_libdir}/libmono-profiler-aot.a
%{_libdir}/libmono-profiler-cov.a
%{_libdir}/libmono-profiler-iomap.a
%{_libdir}/libmono-profiler-log.a
%endif
