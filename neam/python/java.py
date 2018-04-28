import atexit
import os
import platform
import shutil
import sys
from jpype import startJVM, shutdownJVM, JPackage, getDefaultJVMPath, java
from urllib.request import urlretrieve

# Windows separates CLASSPATH entries differently from *nix OS's
SEP = ';' if platform.system() == 'Windows' else ':'

# The version of CoreNLP to use
VERSION = '3.7.0'

# The JAR files required
JARS = ['stanford-corenlp-'+VERSION+'.jar', 'stanford-corenlp-'+VERSION+'-models.jar']

# The Maven search path
MAVEN_URL = 'http://search.maven.org/remotecontent?filepath=edu/stanford/nlp/stanford-corenlp' + VERSION + '/'

# Establish paths to the java directory
current_dir = os.path.dirname(os.path.realpath(__file__))
java_dir = os.path.join(current_dir, '..', 'java')
lib_dir = os.path.join(java_dir, 'lib')


def boot_java():
    src_path = os.path.join(java_dir, 'neam')
    jar_paths = [os.path.join(lib_dir, jar) for jar in JARS]
    load_paths = [src_path] + jar_paths

    startJVM(getDefaultJVMPath(), '-ea', '-Xmx4G', '-Djava.class.path=' + SEP.join(load_paths))
    atexit.register(shutdownJVM)


def install_corenlp():
    if not os.path.isdir(lib_dir):
        os.mkdir(lib_dir)
        print('Downloading Stanford CoreNLP for first time use...', file=sys.stderr)

        try:
            for jar in JARS:
                url = MAVEN_URL + jar
                file_path = os.path.join(lib_dir, jar)
                urlretrieve(url, file_path)
        except:
            print('Error downloading Stanford CoreNLP.', file=sys.stderr)
            shutil.rmtree(lib_dir)


install_corenlp()
boot_java()
clms = JPackage('clms')

__all__ = ['java', 'clms']

