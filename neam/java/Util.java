import java.io.*;

/**
 * Contains static NEAM utility methods
 */
public final class Util {

    private Util() {
        throw new RuntimeException("Util is a static class and cannot be instantiated.");
    }

    /**
     * Loads an entire file into a String.
     *
     * @param fileName The name of the file to load
     * @return The contents of the file
     */
    public static String loadFile(String fileName) {
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
            System.err.println("IOException: Could not open " + fileName + ".");
        }

        return builder.toString();
    }
}

