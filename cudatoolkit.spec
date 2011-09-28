#
# Conditional build:
%bcond_with	prof		# package computeprof (requires Qt < 4.7)

Summary:	NVIDIA CUDA Toolkit
Summary(pl.UTF-8):	Zestaw narzędzi NVIDIA CUDA
Name:		cudatoolkit
Version:	4.0.17
Release:	0.1
License:	nVidia Binary
Group:		Development/Tools
Source0:	http://developer.download.nvidia.com/compute/cuda/4_0/toolkit/%{name}_%{version}_linux_32_ubuntu10.10.run
# Source0-md5:	8d025093ac6713eaa7dbffc8f3493606
Source1:	http://developer.download.nvidia.com/compute/cuda/4_0/toolkit/%{name}_%{version}_linux_64_ubuntu10.10.run
# Source1-md5:	fb1f87e7a112545f6f07bc30e646bdf4
Source2:	http://developer.download.nvidia.com/compute/cuda/4_0/sdk/gpucomputingsdk_%{version}_linux.run
# Source2-md5:	07393c5eb702485deaa06a37747391ea
Source3:	http://developer.download.nvidia.com/compute/cuda/4_0/ToolsSDK/cudatools_%{version}_linux_32.run
# Source3-md5:	6426892e521b931a18b57e3680b1cc4e
Source4:	http://developer.download.nvidia.com/compute/cuda/4_0/ToolsSDK/cudatools_%{version}_linux_64.run
# Source4-md5:	1fc9673eccb604ed6e386397b995ec25
URL:		http://www.nvidia.com/object/cuda_home.html
Requires:	%{name}-libs = %{version}-%{release}
%{?with_prof:Requires:	qt4-assistant}
Requires:	xorg-driver-video-nvidia-libs >= 1:190.53-4
ExclusiveArch:	%{ix86} %{x8664}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The CUDA(tm) architecture enables developers to leverage the massively
parallel processing power of NVIDIA GPUs, delivering the performance
of NVIDIA's world-renowned graphics processor technology to general
purpose GPU Computing.

With the CUDA architecture and tools, developers are achieving
dramatic speedups in fields such as medical imaging and natural
resource exploration, and creating breakthrough applications in areas
such as image recognition and real-time HD video playback and
encoding.

CUDA enables this unprecedented performance via standard APIs such
OpenCL and DirectCompute, and high level programming languages such as
C/C++, Fortran, Java, Python, and the Microsoft .NET Framework.

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
/bin/sh %{SOURCE3} --noexec --keep
%else
/bin/sh %{SOURCE1} --noexec --keep
/bin/sh %{SOURCE4} --noexec --keep
%endif
/bin/sh %{SOURCE2} --noexec --keep
cp -a pkg/computeprof/doc pkg/computeprof/computeprof

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_libdir}/cuda/prof/{doc,bin}} \
	$RPM_BUILD_ROOT{%{_mandir}/man{1,3},%{_includedir}/cuda} \
	$RPM_BUILD_ROOT%{_sysconfdir}

install -p pkg/bin/* $RPM_BUILD_ROOT%{_bindir}
cp -a pkg/%{_lib}/* $RPM_BUILD_ROOT%{_libdir}
cp -p pkg/man/man1/* $RPM_BUILD_ROOT%{_mandir}/man1
cp -p pkg/man/man3/* $RPM_BUILD_ROOT%{_mandir}/man3
cp -a pkg/include/* $RPM_BUILD_ROOT%{_includedir}/cuda

cp -a pkg/open64 $RPM_BUILD_ROOT%{_libdir}/cuda

mv $RPM_BUILD_ROOT%{_bindir}/nvcc{,.bin}
cat <<'EOF' >$RPM_BUILD_ROOT%{_sysconfdir}/nvcc.conf
INCLUDES="-I/usr/include/cuda"
LIBRARIES="-lcudart"

CUDAFE_FLAGS=
OPENCC_FLAGS=
PTXAS_FLAGS=
EOF

cat <<'EOF' >$RPM_BUILD_ROOT%{_bindir}/nvcc
#!/bin/sh
. %{_sysconfdir}/nvcc.conf

export INCLUDES LIBRARIES CUDAFE_FLAGS OPENCC_FLAGS PTXAS_FLAG

exec %{_bindir}/nvcc.bin "$@"
EOF

%if %{with prof}
cp -a pkg/computeprof/doc/computeprof.{html,q*} $RPM_BUILD_ROOT%{_libdir}/cuda/prof/doc
cp -a pkg/computeprof/doc/help.png $RPM_BUILD_ROOT%{_libdir}/cuda/prof/doc
install -p pkg/computeprof/bin/computeprof $RPM_BUILD_ROOT%{_libdir}/cuda/prof/bin

ln -s %{_libdir}/qt4/bin/assistant $RPM_BUILD_ROOT%{_libdir}/cuda/prof/bin/assistant
ln -s %{_libdir}/cuda/prof/bin/computeprof $RPM_BUILD_ROOT%{_bindir}/computeprof
%endif

ln -s %{_libdir}/cuda/open64/bin/nvopencc $RPM_BUILD_ROOT%{_bindir}/nvopencc

%clean
rm -rf $RPM_BUILD_ROOT

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc pkg/doc/* pkg/bin/nvcc.profile
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/nvcc.conf
%attr(755,root,root) %{_bindir}/bin2c
%attr(755,root,root) %{_bindir}/cuda-gdb
%attr(755,root,root) %{_bindir}/cuda-memcheck
%attr(755,root,root) %{_bindir}/cudafe*
%attr(755,root,root) %{_bindir}/fatbin
%attr(755,root,root) %{_bindir}/filehash
%attr(755,root,root) %{_bindir}/nvcc
%attr(755,root,root) %{_bindir}/nvcc.bin
%attr(755,root,root) %{_bindir}/nvopencc
%attr(755,root,root) %{_bindir}/ptxas
%{_includedir}/cuda
%dir %{_libdir}/cuda
%if %{with prof}
%doc pkg/computeprof/CUDA_Visual_Profiler_Release_Notes.txt pkg/computeprof/computeprof
%dir %{_libdir}/cuda/prof
%dir %{_libdir}/cuda/prof/bin
%attr(755,root,root) %{_bindir}/computeprof
%attr(755,root,root) %{_libdir}/cuda/prof/bin/*
%{_libdir}/cuda/prof/doc
%endif
%dir %{_libdir}/cuda/open64
%dir %{_libdir}/cuda/open64/bin
%dir %{_libdir}/cuda/open64/lib
%attr(755,root,root) %{_libdir}/cuda/open64/bin/*
%attr(755,root,root) %{_libdir}/cuda/open64/lib/*
%{_libdir}/libcublas.so
%{_libdir}/libcudart.so
%{_libdir}/libcufft.so
%{_mandir}/man1/*
%{_mandir}/man3/*

%files libs
%defattr(644,root,root,755)
%ghost %{_libdir}/libcublas.so.3
%attr(755,root,root) %{_libdir}/libcublas.so.*.*.*
%ghost %{_libdir}/libcudart.so.3
%attr(755,root,root) %{_libdir}/libcudart.so.*.*.*
%ghost %{_libdir}/libcufft.so.3
%attr(755,root,root) %{_libdir}/libcufft.so.*.*.*
