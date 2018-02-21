""" Functions to retrieve compiler versions.
"""
import os
import subprocess
import sys
import tempfile
from enum import Enum

if (sys.version_info.major, sys.version_info.minor) < (3, 5):
    raise RuntimeError('Python 3.5 is required')

class _LanguageType(Enum):
    C = 'c'
    CPP = 'c++'

class CompilationError(Exception):
    """ Compilation error of the version printing test program. """

def _check_compilation_result(result):
    if result.returncode != 0:
        raise CompilationError(result.stdout)

def _get_gcc_version_implementation(language_type):
    with tempfile.TemporaryDirectory() as tmpdirname:
        print_version_exe = os.path.join(tmpdirname, 'print_version')
        print_version_code = """
            #include <stdio.h>
            int main(void)
            {
                printf("%d.%d.%d", __GNUC__, __GNUC_MINOR__, __GNUC_PATCHLEVEL__);
                return 0;
            }
        """
        _check_compilation_result(subprocess.run(
            ['g++' if language_type == _LanguageType.CPP else 'gcc',
             '-x', language_type.value,
             '-o', print_version_exe, '-'],
            input=print_version_code,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True,
            check=False))
        result = subprocess.run(
            [print_version_exe],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True,
            check=True)
        return result.stdout

def get_gcc_version():
    """ Returns the current `gcc` version as a string formated as major.minor.patch-level.
    """
    return _get_gcc_version_implementation(_LanguageType.C)

def get_gpp_version():
    """ Returns the current `g++` version as a string formated as major.minor.patch-level.
    """
    return _get_gcc_version_implementation(_LanguageType.CPP)


def check_gcc_version(version):
    """ Checks that the current `gcc` version is the one provided.
        The version to check should be of the format:
        major[.minor[.patch-level]]
    """
    return get_gcc_version().startswith(version)

def check_gpp_version(version):
    """ Checks that the current `g++` version is the one provided.
        The version to check should be of the format:
        major[.minor[.patch-level]]
    """
    return get_gpp_version().startswith(version)

def _get_clang_version_implementation(language_type):
    with tempfile.TemporaryDirectory() as tmpdirname:
        print_version_exe = os.path.join(tmpdirname, 'print_version')
        print_version_code = """
            #include <stdio.h>
            int main(void)
            {
                printf("%d.%d.%d", __clang_major__, __clang_minor__, __clang_patchlevel__);
                return 0;
            }
        """
        _check_compilation_result(subprocess.run(
            ['clang++' if language_type == _LanguageType.CPP else 'clang',
             '-x', language_type.value,
             '-o', print_version_exe, '-'],
            input=print_version_code,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True,
            check=False))

        result = subprocess.run(
            [print_version_exe],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True,
            check=True)
        return result.stdout

def get_clang_version():
    """ Returns the current `clang` version as a string formated as major.minor.patch-level.
    """
    return _get_clang_version_implementation(_LanguageType.C)

def get_clangpp_version():
    """ Returns the current `clang++` version as a string formated as major.minor.patch-level.
    """
    return _get_clang_version_implementation(_LanguageType.CPP)

def check_clang_version(version):
    """ Checks that the current `clang` version is the one provided.
        The version to check should be of the format:
        major[.minor[.patch-level]]
    """
    return get_clang_version().startswith(version)

def check_clangpp_version(version):
    """ Checks that the current `clang++` version is the one provided.
        The version to check should be of the format:
        major[.minor[.patch-level]]
    """
    return get_clangpp_version().startswith(version)


def _print_compiler_version(compiler):
    status = 0
    if compiler == 'gcc':
        print(get_gcc_version())
    elif compiler == 'g++':
        print(get_gcc_version())
    elif compiler == 'clang':
        print(get_clang_version())
    elif compiler == 'clang++':
        print(get_clangpp_version())
    else:
        status = 1
    return status

def _print_check_compiler_version(compiler, version):
    status = 0
    check = False
    if compiler == 'gcc':
        check = check_gcc_version(version)
    elif compiler == 'g++':
        check = check_gcc_version(version)
    elif compiler == 'clang':
        check = check_clang_version(version)
    elif compiler == 'clang++':
        check = check_clangpp_version(version)
    else:
        status = 1
    if status == 0:
        print('%s version %s %s' % (
            compiler,
            'is' if check else 'is NOT',
            version))
        if not check:
            status = 1

    return status

def _main():
    status = 0
    try:
        if len(sys.argv) == 2:
            status = _print_compiler_version(sys.argv[1])
        elif len(sys.argv) == 3:
            status = _print_check_compiler_version(sys.argv[1], sys.argv[2])
        else:
            status = 2
    except OSError as error:
        print(sys.argv[1] + ':', error, file=sys.stderr)
        status = 3
    except CompilationError as error:
        print(sys.argv[1] + ':', error, file=sys.stderr)
        status = 4

    sys.exit(status)

if __name__ == '__main__':
    _main()
