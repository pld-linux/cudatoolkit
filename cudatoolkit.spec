Summary:	NVIDIA CUDA Toolkit
Summary(pl.UTF-8):	Zestaw narzędzi NVIDIA CUDA
Name:		cudatoolkit
Version:	2.3
Release:	1
License:	nVidia Binary
Group:		Applications
Source0:	http://developer.download.nvidia.com/compute/cuda/2_3/toolkit/%{name}_%{version}_linux_32_fedora10.run
# Source0-md5:	4c7d5002aeff376f826e9744d8322dbe
Source1:	http://developer.download.nvidia.com/compute/cuda/2_3/toolkit/%{name}_%{version}_linux_64_fedora10.run
# Source1-md5:	9da21f449005be25d0fc928c914562ba
URL:		http://www.nvidia.com/object/cuda_home.html
Requires:	%{name}-libs = %{version}-%{release}
Requires:	qt4-assistant
Requires:	xorg-driver-video-nvidia-libs >= 1:190.53-4
ExclusiveArch:	%{ix86} %{x8664}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The CUDA™ architecture enables developers to leverage the massively
parallel processing power of NVIDIA GPUs, delivering the performance
of NVIDIA’s world-renowned graphics processor technology to general
purpose GPU Computing.

With the CUDA architecture and tools, developers are achieving
dramatic speedups in fields such as medical imaging and natural
resource exploration, and creating breakthrough applications in areas
such as image recognition and real-time HD video playback and
encoding.

CUDA enables this unprecedented performance via standard APIs such
OpenCL and DirectCompute, and high level programming languages such as
C/C++, Fortran, Java, Python, and the Microsoft .NET Framework.

##description -l pl.UTF-8

%package libs
Summary:	NVIDIA CUDA libraries
Summary(pl.UTF-8):	Biblioteki NVIDIA CUDA
Group:		Libraries

%description libs
NVIDIA CUDA libraries.

%description libs -l pl.UTF-8
Biblioteki NVIDIA CUDA.

%prep
%setup -qcT
%ifarch %{ix86}
/bin/sh %{SOURCE0} --noexec --keep
%else
/bin/sh %{SOURCE1} --noexec --keep
%endif

cp -a pkg/cudaprof/doc pkg/cudaprof/cudaprof

%build

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_libdir}/cudaprof/{doc,bin}} \
	$RPM_BUILD_ROOT{%{_mandir}/man{1,3},%{_includedir}/cuda}

install pkg/bin/* $RPM_BUILD_ROOT%{_bindir}
cp -a pkg/%{_lib}/* $RPM_BUILD_ROOT%{_libdir}
install pkg/man/man1/* $RPM_BUILD_ROOT%{_mandir}/man1
install pkg/man/man3/* $RPM_BUILD_ROOT%{_mandir}/man3
cp -a pkg/include/* $RPM_BUILD_ROOT%{_includedir}/cuda

cp -a pkg/cudaprof/doc/cudaprof.{html,q*} $RPM_BUILD_ROOT%{_libdir}/cudaprof/doc
cp -a pkg/cudaprof/doc/help.png $RPM_BUILD_ROOT%{_libdir}/cudaprof/doc

install pkg/cudaprof/bin/cudaprof $RPM_BUILD_ROOT%{_libdir}/cudaprof/bin
ln -s %{_libdir}/qt4/bin/assistant $RPM_BUILD_ROOT%{_libdir}/cudaprof/bin
ln -s %{_libdir}/cudaprof/bin/cudaprof $RPM_BUILD_ROOT%{_bindir}/cudaprof

%clean
rm -rf $RPM_BUILD_ROOT

%post libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc pkg/doc/* pkg/bin/nvcc.profile
%doc pkg/cudaprof/CUDA_Visual_Profiler_Release_Notes.txt pkg/cudaprof/cudaprof
%attr(755,root,root) %{_bindir}/bin2c
%attr(755,root,root) %{_bindir}/cuda-gdb
%attr(755,root,root) %{_bindir}/cudafe*
%attr(755,root,root) %{_bindir}/cudaprof
%attr(755,root,root) %{_bindir}/fatbin
%attr(755,root,root) %{_bindir}/filehash
%attr(755,root,root) %{_bindir}/nvcc
%attr(755,root,root) %{_bindir}/ptxas
%{_includedir}/cuda
%dir %{_libdir}/cudaprof
%dir %{_libdir}/cudaprof/bin
%attr(755,root,root) %{_libdir}/cudaprof/bin/*
%{_libdir}/cudaprof/doc
%attr(755,root,root) %{_libdir}/lib*.so
%{_mandir}/man1/*
%{_mandir}/man3/*

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %ghost %{_libdir}/lib*.so.2
%attr(755,root,root) %{_libdir}/lib*.so.*.*
