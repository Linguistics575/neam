# NEAM: Named-Entity Automatic Markup on Historical Texts

## Requirements
NEAM is written in Python and Java, and requires both to be installed. (For Python, it requires
Python 3, and the Java version must be 1.8.) There are also language-specific dependencies,
which are given below:

### Python dependencies
To install NEAM's Python dependencies, you need to have [pip](https://pypi.python.org/pypi/pip)
installed. If you have GNU Make, dependencies can then be installed by typing `make` within the
project root; otherwise, run `pip install requirements.txt`. (If you are on Linux and get a
permissions error, try the command again, prefixed with `sudo`).

### Java dependencies
NEAM makes use of [Stanford CoreNLP](https://stanfordnlp.github.io/CoreNLP/download.html), which
requires its own setup. Specifically, it tested on version `3.7.0`, available
[here](https://stanfordnlp.github.io/CoreNLP/history.html). You're welcome to try using a newer
version, but results are not guaranteed. Once you have CoreNLP downloaded, you can add it to your
`CLASSPATH` on Linux like so:

`export CLASSPATH="/Path/To/CoreNLP/*:$CLASSPATH"`

CoreNLP requires Java 8, so your `JAVA_HOME` and `PATH` need to reflect that. On Linux, these can
be set like so:

`export JAVA_HOME="/path/to/java/bin/java"`

`export PATH="/path/to/java/bin:$PATH"`

If you're going to be running NEAM a lot, it is recommended to put all of these commands inside
your `.bashrc` file (or the comparable file if you're using a shell other than Bash).

## Usage
The full NEAM pipeline can be run by calling `pipeline.sh file`, where `file` is a text document to
be tagged.
