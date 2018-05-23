# NEAM: Named-Entity Automatic Markup on Historical Texts

## Downloading NEAM
For instructions on how to download NEAM, please refer to 
[this page](https://help.github.com/articles/cloning-a-repository/) for instructions for your
particular OS. Instructions are available both for Github Desktop and through Terminal.

## Requirements
NEAM is written in Python and Java, and requires both to be installed. (For Python, it requires
Python 3, and the Java version must be 1.8.) There are also language-specific dependencies,
which are given below. NEAM can run on Windows, however instructions cannot be provided for 
this operating system as they vary too much depending on the particular version and setup.

### Java dependencies
NEAM is built on [Stanford CoreNLP](https://stanfordnlp.github.io/CoreNLP/download.html), which
in turn requires Java 1.8 installed and `JAVA_HOME` properly configured. Navigate to 
[this page](http://www.oracle.com/technetwork/java/javase/downloads/index.html) and scroll to 
`Java SE 8u171/ 8u172`. Click the download link below "JDK" and download Java SE Development Kit
8u171. Next, follow the `Installation Instructions` link from the previous page in
the `Java SE 8u171/ 8u172` section to find specific installation instructions for your operating 
system.

Your `JAVA_HOME` environment variable should point to the folder that contains `bin/java`. You 
can follow the appropriate platform-specific instructions below to set this up. You do not need 
to install Stanford CoreNLP yourself; NEAM will do this for you the first time you call it.

#### Linux
Start Terminal by typing `Ctrl + Alt + T` and run the following command:

`export JAVA_HOME="/path/to/java"`

If you're going to be running NEAM a lot, it is recommended to put this command inside your
`.bashrc` file (or the comparable file if you're using a shell other than Bash).

#### Mac OS X
Your configuration should work without any changes, but if it does not work you can follow the
instructions in the Linux section above. To access Terminal on Mac, type `CMD + Space` to open 
Spotlight, then type "terminal" and hit Enter.

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

`pip install -r requirements.txt`

in Terminal from the NEAM root directory. Note: if you have multiple versions of pip installed 
(e.g., one for Python 2.7 and one for Python 3), you will need to use the command `pip3` instead
of `pip`. Root/administrative privileges are required to install dependencies through this 
method. If you do not have root privileges, see "Usage" below for running NEAM in a virtual 
environment.

## Usage

### Tagging
If you were able to install NEAM's Python dependencies, NEAM can be run by calling
`./neam.py <file>` in Terminal, where `<file>` is a text document to be tagged. 

If you were not able to install its dependencies, running `./neam.sh <file>` will initialize a 
virtual environment and install the dependencies before running NEAM. The virtual environment 
will be left in place, so this install will only need to be done once, even though you will need
to continue to call `neam.sh` instead of `neam.py`.

### Evaluation

Evaluation of the system against a gold standard is a development-related task. Users wishing 
only to tag named entities in texts need not carry out evaluation.

Nevertheless, valuation of the system's output against a gold standard can be carried out by 
executing

`./evaluate.sh <output> <gold> [eval_tag ...]`

where `<output>` is the XML file you are evaluating, and `<gold>` is the gold standard XML file.
You can optionally include a sequence of tags you want evaluated after this. If no tags are 
included, persname, placename, and orgname are evaluated by default. The evaluation script will 
dump all incorrect taggings to stderr. This can be redirected to a file using `2>` at the end of
the call followed by the desired filename when executing the script.
