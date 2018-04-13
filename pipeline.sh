#!/bin/sh
src/ner.py $1 | src/beautify.py
