import java.io.*;
import java.util.*;

/**
 * Classifies a document using a NEAMClassifier
 */
public class Classify {
    public static void main(String[] args) {
        // The name of the file to classify
        String fileName = args[0];
        // The properties to load into the classifier
        String properties = args[1];
        // The tags to look for
        String tags = args[2];
        // The NER model to use - default to null
        String model = args.length > 3 ? args[3] : null;

        // Generate the properties
        NEAMDict props = new NEAMDict();
        props.loadFile(properties);
        if (model != null && model.length() > 0) {
            props.setProperty("ner.model", model);
        }

        // Generate the classifier
        NEAMClassifier classifier = new NEAMClassifier(props);
        classifier.tags.loadFile(tags);

        // Classify the document
        String tagged = classifier.classify(fileName);

        // Dump the output
        System.out.println(tagged);
    }
}

