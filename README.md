# NEAM: Named-Entity Automatic Markup on Historical Texts

## Requirements
NEAM is written in Python and Java, and requires both to be installed. (For Python, it requires
Python 3, and the Java version must be 1.8.) There are also language-specific dependencies,
which are given below.

### Java dependencies
NEAM is built on [Stanford CoreNLP](https://stanfordnlp.github.io/CoreNLP/download.html), which
in turn requires Java 1.8 installed and `JAVA_HOME` properly configured. Navigate to 
[this page](http://www.oracle.com/technetwork/java/javase/downloads/index.html) and scroll to 
`Java SE 8u171/ 8u172`. Download the JDK and then follow the `Installation Instructions` link in
that section to find specific installation instructions for your operating system.

Your `JAVA_HOME` environment variable should point to the folder that contains `bin/java`. You 
can follow the appropriate platform-specific instructions below to set this up. You do not need 
to install Stanford CoreNLP yourself; NEAM will do this for you the first time you call it.

#### Windows
Right click on `My Computer`, and navigate to `Properties -> Advanced System Settings ->
Environment Variables`. Click on `New...`, and type `JAVA_HOME` as the `Variable name`, and the
path to your java installation directory (e.g. `C:\Program Files\Java\jdk1.8.0_141`) as the
`Variable value`.

#### Linux
Run the following command from the terminal:

`export JAVA_HOME="/path/to/java"`

If you're going to be running NEAM a lot, it is recommended to put this command inside your
`.bashrc` file (or the comparable file if you're using a shell other than Bash).

### Python dependencies
Navigate to [this page](https://www.python.org/downloads/) and download and install Python 3. 
NEAM uses [pip](https://pypi.python.org/pypi/pip) to manage its Python dependencies. If it is
not already installed, please do so by navigating to 
[this page](https://pip.pypa.io/en/stable/installing/) and following the instructions there. If
you have more than one version of Python installed on your system, you will need to install it 
using the Python command for Python 3. You may be able to do this by typing `python3` instead 
of `python` in the pip installation instructions. If not, you will need to find the path to the
Python 3 binary on your system and use that. 

Once pip is installed, if you have root privileges, you can install all of NEAM's Python 
dependencies by typing

`pip3 install -r requirements.txt`

on the command line / Powershell (on Windows) or Terminal (on Linux / OS X) from the NEAM root 
directory. If you are on Windows, be sure to run the command line / Powershell as an 
administrator. If you do not have root privileges, see "Usage" below for running NEAM in a 
virtual environment.

## Usage

### Tagging
If you were able to install NEAM's Python dependencies, NEAM can be run by calling
`./neam.py file`, where `file` is a text document to be tagged. If you were not able to install
its dependencies, running `./neam.sh file` will initialize a virtual environment and install the
dependencies before running NEAM. The virtual environment will be left in place, so this install
will only need to be done once, even though you will need to continue to call `neam.sh` instead
of `neam.py`.

### Evaluation

Evaluation of the system against a gold standard is a development-related task. Users wishing 
only to tag named entities in texts need not carry out evaluation.

Nevertheless, valuation of the system's output against a gold standard can be carried out by 
executing

`./evaluate.sh <output> <gold> [eval_tag ...]`

where `output` is the XML file you are evaluating, and `gold` is the gold standard XML file. You
can optionally include a sequence of tags you want evaluated after this. If no tags are 
included, persname, placename, and orgname are evaluated by default. The evaluation script will 
dump all incorrect taggings to stderr. This can be redirected to a file using `2>` followed by 
the desired filename when executing the script.
