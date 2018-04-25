#!/bin/sh
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PYTHONIOENCODING=utf-8 python3 "$DIR/neam/evaluate.py" $1 $2
