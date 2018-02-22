#!/bin/bash

export CLANGXX_COMMAND="/usr/bin/clang++-5.0"
export CLANG_COMMAND="/usr/bin/clang-5.0"
export PS1="[clang-5.0]\u@\h:\w>"

script_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
export PATH="${script_dir}/linux_compiler_redirect:${PATH}"
exec bash --norc

