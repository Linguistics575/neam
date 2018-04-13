# NEAM: Named-Entity Automatic Markup on Historical Texts

## Requirements
### Installing Python dependencies
To install NEAM's dependencies, you need to have [pip](https://pypi.python.org/pypi/pip) installed.
If you have GNU Make, dependencies can then be installed by typing `make` within the project root;
otherwise, run `pip install requirements.txt`. (If you are on Linux and get a permissions error,
try the command again, prefixed with `sudo`).

### Configuring Java dependencies
NEAM makes use of [Stanford NER](https://nlp.stanford.edu/software/CRF-NER.html), which requires
its own setup. Once you have it installed, copy or rename `config.json.example` to `config.json`
and add the path to the trained model file (a `.gz` file) and the NER jar (a `.jar` file).

