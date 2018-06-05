# NEAM: Named-Entity Automatic Markup on Historical Texts

NEAM is a system for extracting and tagging named entities in historical texts as part of the 
[Emma B. Andrews Diary Project](http://www.emmabandrews.org/project/). One of the aims of this
project is the digitization and markup of various primary historical documents from the 'Golden
Age' of Egyptian aarchaeology (the late 19th to early 20th centuries). As it is right now, NEAM 
will work only for English-language documents.

The entities which NEAM currently extracts are people, places, and organizations. The 
found entities are tagged with XML following the 
[TEI schema](https://github.com/eba-diary/EBA-xml-TEI/blob/master/eba_tei_schema.rnc) and 
[tagging instructions](https://github.com/eba-diary/EBA-xml-TEI/wiki) of the project. In 
addition to tags for entities, structural and other contextual XML tags are also used for 
elements such as titles, dates, divs, paragraphs, and pages.

This repo is intended for people working on the various primary historical documents of the Emma
B. Andrews Diary Project. NEAM is not meant to replace human annotators altogether, but rather 
to lessen the load on them by doing a large portion of the markup process automatically. The
system is not perfect, making errors and missing entities, so human annotators are needed to
verify its output. See `Evaluation` below for information on the accuracy of NEAM.

## Using NEAM
Please refer to our 
[usage documentation](https://github.com/Linguistics575/neam/wiki/User-Guide).

## Development
There are a number of open issues in the issues section of this repo, most of which are 
new desired features of the system. Improvements in accuracy are also always welcome. See 
`Evaluation` below for information on the accuracy of NEAM.

For information on the technical aspects of NEAM, please refer to our 
[technical documentation](https://github.com/Linguistics575/neam/wiki/Technical-Documentation)

## Evaluation

MUC-Style Evaluation Results

|         | Precision | Recall | F-measure |
|   ---:  | :-------: | :----: | :-------: |
|orgname  | .3571     | .1056  | .1630     |
|persname | .8198     | .8516  | .8354     |
|placename| .8055     | .6037  | .6902     |
|Total    | .8049     | .6968  | .7470     |

CoNLL-Style Evaluation Results

|         | Precision | Recall | F-measure |
|   ---:  | :-------: | :----: | :-------: |
|orgname  | .0952     | .0282  | .0435     |
|persname | .7273     | .7555  | .7411     |
|placename| .7606     | .5701  | .6517     |
|Total    | .7274     | .6297  | .6750     |

## Forthcoming
This repository contains code for a web interface for NEAM to allow for easier usage by
participants of the Emma B. Andrews Diary Project. While the code itself is functional, 
at present there is no server available on which to run it. Plese refer to our
[technical documentation](https://github.com/Linguistics575/neam/wiki/Technical-Documentation)
for information on the web interface and needed server.

## License
NEAM is licenced under the GNU General Public License 3.0. For more information on 
this licence, please refer to `LICENSE.txt` in the NEAM root directory.
