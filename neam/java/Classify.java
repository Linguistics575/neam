import edu.stanford.nlp.pipeline.*;
import edu.stanford.nlp.ling.*;
import edu.stanford.nlp.ling.CoreAnnotations.*;
import edu.stanford.nlp.util.*;
import java.util.*;
import java.io.*;

public class Classify {

    public static String OUTSIDE_TAG = "O";

    public static void main(String[] args) {
        String fileName = args[0];
        String model = args.length > 1 ? args[1] : null;

        StanfordCoreNLP pipeline = initPipeline(model);
        Annotation document = initDocument(fileName);

        pipeline.annotate(document);
        tagDocument(document);
    }

    public static StanfordCoreNLP initPipeline(String model) {
        Properties props = new Properties();
        props.setProperty("annotators", "tokenize, ssplit, pos, lemma, ner");

        if (model != null) {
            props.setProperty("ner.model", model);
        }

        return new StanfordCoreNLP(props);
    }

    public static Annotation initDocument(String fileName) {
        StringBuilder builder = new StringBuilder();
        String line;
        BufferedReader reader;

        try {
            reader = new BufferedReader(new FileReader(fileName));

            while ((line = reader.readLine()) != null) {
                builder.append(line).append(' ');
            }
        } catch (IOException e) {
            System.err.println("Could not open " + fileName);
        }


        return new Annotation(builder.toString());
    }

    public static void tagDocument(Annotation document) {
        List<CoreMap> sentences = document.get(SentencesAnnotation.class);
        String prevTag = OUTSIDE_TAG;
        String word;
        String currentTag;

        for (CoreMap sentence : sentences) {
            for (CoreLabel token : sentence.get(TokensAnnotation.class)) {
                word = token.get(TextAnnotation.class);
                currentTag = token.get(NamedEntityTagAnnotation.class);

                if (!currentTag.equals(prevTag) && !prevTag.equals(OUTSIDE_TAG)) {
                    System.out.println(closeTag(prevTag));
                }

                if (!currentTag.equals(prevTag) && !currentTag.equals(OUTSIDE_TAG)) {
                    System.out.println(openTag(currentTag));
                }

                System.out.println(word);

                prevTag = currentTag;
            }
        }
    }

    public static String openTag(String name) {
        return '<' + name + '>';
    }

    public static String closeTag(String name) {
        return "</" + name + '>';
    }
}

