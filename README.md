# NEAM: Named-Entity Automatic Markup on Historical Texts

## Requirements
### Installing Python dependencies
To install NEAM's dependencies, you need to have [pip](https://pypi.python.org/pypi/pip) installed.
If you have GNU Make, dependencies can then be installed by typing `make` within the project root;
otherwise, run `pip install requirements.txt`. (If you are on Linux and get a permissions error,
try the command again, prefixed with `sudo`).

### Configuring Java dependencies
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

## Usage
The full NEAM pipeline can be run by calling `pipeline.sh file`, where `file` is a text document to
be tagged.
