#!/bin/bash

# from https://stackoverflow.com/questions/59895/getting-the-source-directory-of-a-bash-script-from-within
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

"$DIR/neam/java/run" "$1" "$2" | "$DIR/neam/beautify.py"

