import argparse
from neam.python.classification import *


def main(input_file, model=None, year=1900):
    pipeline = Pipeline([
        #################
        # Preprocessing #
        #################

        # Get rid of any weird characters from the input
        ASCIIifier(),

        ###########
        # Tagging #
        ###########
        
        # Run Stanford CoreNLP to tag named entities and dates
        load_classifier(model),
        # Tag all of the titles using a custom trained MaxEnt classifier
        TitleAnnotator(),
        # Replace page numbers with <pb> tags
        PageReplacer(),
        # Replace sic marks with <sic> tags
        SicReplacer(),

        ######################
        # Tag postprocessing #
        ######################

        # Clean up Stanford's tagging of dates
        DateProcessor(),
        # Move any of the following titles inside tags that occur directly to their right
        TagExpander(tags=['persName'], words=['the', 'Mr.', 'Mrs.', 'Ms.', 'Miss', 'Lady', 'Dr.', 'Maj.', 'Col.', 'Capt.', 'Rev', 'SS', 'S.S.', 'Contessa', 'Judge']),
        # Add in the <p> and <div> tags
        JournalShaper('EBA', year),
        # Check tags against Wikipedia
        WikiRetagger(tags=['placeName', 'orgName']),
        # Set the ref attribute of named entity tags
        RefAnnotator(),

        ##############
        # Formatting #
        ##############

        # Adjust the spacing to get rid of weird newlines and repeated spaces
        SpaceNormalizer(),
        # Format the XML into a standardized layout
        Beautifier()
    ])

    text = ''.join(input_file)
    return pipeline.run(text)


def load_classifier(model):
    props = {}
    if model:
        props["ner.model"] = model
    return Classifier(props)


def load_args():
    parser = argparse.ArgumentParser(description='Named Entity recognition and Automated Markup on historical texts')
    parser.add_argument('file', help='The file NEAM should classify')
    parser.add_argument('--model', help='A NER model to override the default')
    parser.add_argument('--gs', help='The gold standard')
    parser.add_argument('--year', help='The year of the first journal entry', type=int, default=1900)
    return parser.parse_args()


if __name__ == '__main__':
    args = load_args()
    with open(args.file, encoding="utf-8") as input_file:
        print(main(input_file, args.model))

