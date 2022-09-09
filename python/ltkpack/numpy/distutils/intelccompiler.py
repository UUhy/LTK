from __future__ import division, absolute_import, print_function
import re
import platform

from distutils.unixccompiler import UnixCCompiler
if platform.system() == 'Windows':
    from numpy.distutils.msvc9compiler import MSVCCompiler
from numpy.distutils.exec_command import find_executable, exec_command
from numpy.distutils.ccompiler import simple_version_match
from os import environ

class IntelCCompiler(UnixCCompiler):
    """A modified Intel compiler compatible with a GCC-built Python."""
    compiler_type = 'intel'
    cc_exe = 'icc'
    cc_args = 'fPIC'

    def __init__(self, verbose=0, dry_run=0, force=0):
        UnixCCompiler.__init__(self, verbose, dry_run, force)

        v = self.get_version()
        self.cc_exe = ('icc -fPIC -fp-model strict -O3 -fomit-frame-pointer ' +
                        environ.get('CFLAGS', '').strip())
        compiler = self.cc_exe

        if platform.system() == 'Darwin':
            shared_flag = '-Wl,-undefined,dynamic_lookup'
        else:
            shared_flag = '-shared'
        self.set_executables(compiler=compiler,
                             compiler_so=compiler,
                             compiler_cxx=compiler,
                             archiver='xiar' + ' cru',
                             linker_exe=compiler + ' -shared-intel',
                             linker_so=compiler + ' ' + shared_flag +
                             ' -shared-intel ' + environ.get('LDFLAGS', '').strip())


class IntelItaniumCCompiler(IntelCCompiler):
    compiler_type = 'intele'

    # On Itanium, the Intel Compiler used to be called ecc, let's search for
    # it (now it's also icc, so ecc is last in the search).
    for cc_exe in map(find_executable, ['icc', 'ecc']):
        if cc_exe:
            break

    def get_version(self):
        if platform.system() == 'Windows':
            version_cmd = "icl -dummy"
            status, output = exec_command(version_cmd, use_tee=0)
            version = re.search(r'Version\s*([\d.]+)', output).group(1)
        else:
            version_cmd = "icc -dumpversion"
            status, version = exec_command(version_cmd, use_tee=0)
        return version


class IntelEM64TCCompiler(UnixCCompiler):
    """
    A modified Intel x86_64 compiler compatible with a 64bit GCC-built Python.
    """
    compiler_type = 'intelem'
    cc_exe = 'icc -m64'
    cc_args = "-fPIC"

    def __init__(self, verbose=0, dry_run=0, force=0):
        UnixCCompiler.__init__(self, verbose, dry_run, force)

        v = self.get_version()
        self.cc_exe = ('icc -m64 -fPIC -fp-model strict -O3 -fomit-frame-pointer {} {}'.format(
                            environ.get('ARCH_FLAGS', '-xSSE4.2 -axCORE-AVX2,COMMON-AVX512'),
                            environ.get('CFLAGS', '').strip()))
        compiler = self.cc_exe

        if platform.system() == 'Darwin':
            shared_flag = '-Wl,-undefined,dynamic_lookup'
        else:
            shared_flag = '-shared'
        self.set_executables(compiler=compiler,
                             compiler_so=compiler,
                             compiler_cxx=compiler,
                             archiver='xiar' + ' cru',
                             linker_exe=compiler + ' -shared-intel',
                             linker_so=compiler + ' ' + shared_flag +
                             ' -shared-intel ' + environ.get('LDFLAGS', '').strip())

    def get_version(self):
        if platform.system() == 'Windows':
            # Intel compiler on Windows does not have way of getting version. Need to parse string using regex to
            # extract version string. Regex from here: https://stackoverflow.com/a/26480961/5140953
            version_cmd = "icl -dummy"
            status, output = exec_command(version_cmd, use_tee=0)
            version = re.search(r'Version\s*([\d.]+)', output).group(1)
        else:
            version_cmd = "icc -dumpversion"
            status, version = exec_command(version_cmd, use_tee=0)
        return version


if platform.system() == 'Windows':
    class IntelCCompilerW(MSVCCompiler):
        """
        A modified Intel compiler compatible with an MSVC-built Python.
        """
        compiler_type = 'intelw'
        compiler_cxx = 'icl'

        def __init__(self, verbose=0, dry_run=0, force=0):
            MSVCCompiler.__init__(self, verbose, dry_run, force)
            version_match = simple_version_match(start=r'Intel\(R\).*?32,')
            self.__version = version_match

        def initialize(self, plat_name=None):
            MSVCCompiler.initialize(self, plat_name)
            self.cc = self.find_exe("icl.exe")
            self.lib = self.find_exe('xilib')
            self.linker = self.find_exe("xilink")
            self.compile_options = ['/nologo', '/O3', '/MD', '/W3',
                                    '/Qstd=c99', '/fp:strict'] + environ.get('ARCH_FLAGS', '/QxSSE4.2 /QaxCORE-AVX2,COMMON-AVX512').strip().split()
            self.compile_options_debug = ['/nologo', '/Od', '/MDd', '/W3',
                                          '/Qstd=c99', '/Z7', '/D_DEBUG']
            self.compile_options.extend(environ.get('CFLAGS', '').strip().split())
            self.compile_options_debug.extend(environ.get('CFLAGS', '').strip().split())

    class IntelEM64TCCompilerW(IntelCCompilerW):
        """
        A modified Intel x86_64 compiler compatible with
        a 64bit MSVC-built Python.
        """
        compiler_type = 'intelemw'

        def __init__(self, verbose=0, dry_run=0, force=0):
            MSVCCompiler.__init__(self, verbose, dry_run, force)
            version_match = simple_version_match(start=r'Intel\(R\).*?64,')
            self.__version = version_match
