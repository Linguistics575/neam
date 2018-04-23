#!/bin/bash

# from https://stackoverflow.com/questions/59895/getting-the-source-directory-of-a-bash-script-from-within
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

PROPERTY_FILE="$DIR/ner.prop"
TAG_FILE="$DIR/tags.prop"

"$DIR/neam/java/run" "$1" $PROPERTY_FILE $TAG_FILE "$2" | "$DIR/neam/postprocess.py" | "$DIR/neam/beautify.py"

