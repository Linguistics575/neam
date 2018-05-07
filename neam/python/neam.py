import argparse
from neam.python.classification import *


def main():
    args = load_args()

    pipeline = Pipeline([
        # Preprocessing
        ASCIIifier(),

        # Tagging
        load_classifier(args),
        TitleAnnotator(),
        PageReplacer(),
        SicReplacer(),

        # Tag postprocessing
        TagExpander(tags=['placeName', 'persName', 'orgName'], words=['the', 'Mr.', 'Mrs.', 'Ms.', 'Miss', 'Dr.', 'Maj.', 'Col.', 'Rev', 'SS', 'S.S.', 'Contessa', 'Judge']),
        JournalShaper('EBA', args.year),
        RefAnnotator(),
        PossessionFixer(),

        # Formatting
        SpaceNormalizer(),
        Beautifier()
    ])

    with open(args.file, encoding="utf-8") as input_file:
        text = ''.join(input_file)

    print(pipeline.run(text))


def load_classifier(args):
    props = {}
    if args.model:
        props["ner.model"] = args.model
    return Classifier(props)


def load_args():
    parser = argparse.ArgumentParser(description='Named Entity recognition and Automated Markup on historical texts')
    parser.add_argument('file', help='The file NEAM should classify')
    parser.add_argument('--model', help='A NER model to override the default')
    parser.add_argument('--gs', help='The gold standard')
    parser.add_argument('--year', help='The year of the first journal entry', type=int, default=1900)
    return parser.parse_args()


if __name__ == '__main__':
    main()

