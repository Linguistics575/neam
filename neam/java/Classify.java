import edu.stanford.nlp.pipeline.*;
import edu.stanford.nlp.ling.*;
import edu.stanford.nlp.ling.CoreAnnotations.*;
import edu.stanford.nlp.util.*;
import java.util.*;
import java.io.*;

public class Classify {

    /**
     * Maps Stanford tags to TEI tags
     */
    public static final Map<String, String> tagMap;

    /**
     * The file where the Stanford CoreNLP properties are located
     */
    public static final String PROPERTY_FILE = "ner.prop";

    // Initialize the tag map. Why doesn't Java have hash literals? Who knows.
    static {
        tagMap = new HashMap<String, String>();
        String[][] pairs = {
            { "PERSON", "persName" },
            { "LOCATION", "placeName" },
            { "ORGANIZATION", "orgName" }
        };

        for (String[] pair : pairs) {
            tagMap.put(pair[0], pair[1]);
        }
    }

    public static void main(String[] args) {
        String fileName = args[0];
        String model = args.length > 1 ? args[1] : null;

        StanfordCoreNLP pipeline = initPipeline(model);
        Annotation document = initDocument(fileName);

        pipeline.annotate(document);
        String tagged = tagDocument(document);

        System.out.println(tagged);
    }

    /**
     * Sets up the StanfordCoreNLP pipeline.
     *
     * Any changes to CoreNLP should be effected here.
     *
     * @param model A file name for a NER model to use, or null to use the default one
     * @return A StanfordCoreNLP pipeline
     */
    public static StanfordCoreNLP initPipeline(String model) {
        Properties props = new Properties();

        loadProperties(props, PROPERTY_FILE);

        if (model != null && model.length() > 0) {
            props.setProperty("ner.model", model);
        }

        return new StanfordCoreNLP(props);
    }

    /**
     * Loads properties from a file into a CoreNLP Properties object.
     *
     * @param props    The properties object to populate
     * @param fileName The name of the file to load from
     */
    private static void loadProperties(Properties props, String fileName) {
        try {
            BufferedReader propertyFile = new BufferedReader(new FileReader(fileName));

            props.load(propertyFile);

            propertyFile.close();
        } catch (IOException e) {
            System.err.println("Could not open properties file.");
        }
    }

    /**
     * Loads in a document to annotate.
     *
     * @param fileName The name of the file to load in
     * @return A CoreNLP Annotation, ready to be run through a pipeline
     */
    public static Annotation initDocument(String fileName) {
        StringBuilder builder = new StringBuilder();
        String line;
        BufferedReader reader;

        try {
            reader = new BufferedReader(new FileReader(fileName));

            while ((line = reader.readLine()) != null) {
                builder.append(line).append('\n');
            }

            reader.close();
        } catch (IOException e) {
            System.err.println("Could not open " + fileName);
        }


        return new Annotation(builder.toString());
    }

    /**
     * Applies the annotations made to a document to the document itself.
     *
     * The document needs to have been already run through a pipeline.
     *
     * @param document The annotated document
     * @return The text of the document, with the named entites tagged in XML
     */
    public static String tagDocument(Annotation document) {
        List<CoreMap> namedEntities = document.get(MentionsAnnotation.class);
        int lastPos = -1;
        int nextPos;
        String text = document.toString();
        String tag, phrase;
        StringBuilder builder = new StringBuilder();

        for (CoreMap namedEntity : namedEntities) {
            tag = namedEntity.get(NamedEntityTagAnnotation.class);
            phrase = namedEntity.toString();

            if (tagMap.containsKey(tag)) {
                tag = tagMap.get(tag);
            }

            // Find the location of the current phrase in the document
            nextPos = text.indexOf(phrase, lastPos);

            // For some reason, the annotator will tag things that aren't in the text
            // sometimes. This check makes sure that it really is tagging something
            // in the text.
            if (nextPos > 0) {
                // Append the text between the previous entity and the current entity
                builder.append(text.substring(lastPos + 1, nextPos));

                // Append the new named entity
                builder.append(wrap(phrase, tag));

                lastPos = nextPos + phrase.length() - 1;
            }
        }

        // Add the stuff between the last NE and the end of the document
        builder.append(text.substring(lastPos + 1));

        return builder.toString();
    }

    /**
     * Wraps a string inside a set of tags.
     *
     * @param content The string to wrap
     * @param tag     The tag to wrap the content in
     * @return The content wrapped inside the tag
     */
    public static String wrap(String content, String tag) {
        return String.format("<%s>%s</%s>", tag, content, tag);
    }
}

