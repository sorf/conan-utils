#!/bin/bash

export GXX_COMMAND="/usr/bin/g++-7"
export GCC_COMMAND="/usr/bin/gcc-7"
export PS1="[gcc-7]\u@\h:\w>"

script_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
export PATH="${script_dir}/linux_compiler_redirect:${PATH}"
exec bash --norc

