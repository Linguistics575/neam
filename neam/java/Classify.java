import java.io.*;
import java.util.*;

/**
 * Classifies a document using a NEAMClassifier
 */
public class Classify {
    /**
     * The file where the Stanford CoreNLP properties are located
     */
    public static final String PROPERTY_FILE = "ner.prop";

    public static final String TAG_FILE = "tags.prop";

    public static void main(String[] args) {
        // The name of the file to classify
        String fileName = args[0];

        // The NER model to use - default to null
        String model = args.length > 1 ? args[1] : null;

        // Generate the properties
        NEAMDict props = new NEAMDict();
        props.loadFile(PROPERTY_FILE);
        if (model != null && model.length() > 0) {
            props.setProperty("ner.model", model);
        }

        // Generate the classifier
        NEAMClassifier classifier = new NEAMClassifier(props);
        classifier.tags.loadFile(TAG_FILE);

        // Classify the document
        String tagged = classifier.classify(fileName);

        // Dump the output
        System.out.println(tagged);
    }
}

