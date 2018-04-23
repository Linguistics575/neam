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

    public static void main(String[] args) {
        // The name of the file to classify
        String fileName = args[0];

        // The NER model to use - default to null
        String model = args.length > 1 ? args[1] : null;

        // Generate the properties
        Properties props = initProperties(PROPERTY_FILE);
        if (model != null && model.length() > 0) {
            props.setProperty("ner.model", model);
        }

        // Classify the document
        NEAMClassifier classifier = new NEAMClassifier(props);
        String tagged = classifier.classify(fileName);

        // Dump the output
        System.out.println(tagged);
    }

    /**
     * Loads properties from a file into a Properties object.
     *
     * @param props    The properties object to populate
     * @param fileName The name of the file to load from
     */
    private static Properties initProperties(String fileName) {
        Properties props = new Properties();

        try {
            BufferedReader propertyFile = new BufferedReader(new FileReader(fileName));

            props.load(propertyFile);

            propertyFile.close();
        } catch (IOException e) {
            System.err.println("Could not open properties file.");
        }

        return props;
    }
}

