# NEAM: Named-Entity Automatic Markup on Historical Texts

## Requirements
NEAM is written in Python and Java, and requires both to be installed. (For Python, it requires
Python 3, and the Java version must be 1.8.) There are also language-specific dependencies,
which are given below.

### Java dependencies
NEAM is built on [Stanford CoreNLP](https://stanfordnlp.github.io/CoreNLP/download.html), which
in turn requires Java 1.8 installed and `JAVA_HOME` properly configured. It should point to the
folder that contains `bin/java`. On Linux, this can be set with the following command:

`export JAVA_HOME="/path/to/java"`

If you're going to be running NEAM a lot, it is recommended to put all of this commands inside
your `.bashrc` file (or the comparable file if you're using a shell other than Bash). You do
not need to explicitly install Stanford CoreNLP yourself; NEAM will do this for you the first
time you call it.

### Python dependencies
NEAM uses [pip](https://pypi.python.org/pypi/pip) to manage its Python dependencies. If it is
not already installed, please do so. If you have root privileges, you can install all of NEAM's
Python dependencies with

`pip3 install -r requirements.txt`

from the NEAM root directory. If you do not have root privileges, see "Usage" below for
running NEAM in a virtual environment.

## Usage
If you were able to install NEAM's Python dependencies, NEAM can be run by calling
`./neam.py file`, where `file` is a text document to be tagged. If you were not able to install
its dependencies, running `./neam.sh file` will initialize a virtual environment and install the
dependencies before running NEAM. The virtual environment will be left in place, so this install
will only need to be done once, even though you will need to continue to call `neam.sh` instead
of `neam.py`.
