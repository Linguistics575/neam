#!/bin/bash

# from https://stackoverflow.com/questions/59895/getting-the-source-directory-of-a-bash-script-from-within
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

PROPERTY_FILE="$DIR/ner.prop"
TAG_FILE="$DIR/tags.prop"
TEMP_FILE="temp.txt"

PYTHONIOENCODING=utf-8 "$DIR/neam/preprocess.py" $1 > "$TEMP_FILE"

"$DIR/neam/java/run" "$TEMP_FILE" $PROPERTY_FILE $TAG_FILE "$2" | "$DIR/neam/postprocess.py" | "$DIR/neam/beautify.py"

rm -f "$TEMP_FILE"

