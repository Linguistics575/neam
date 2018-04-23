import java.io.*;
import java.util.Properties;

public class NEAMDict extends Properties {
    public void loadFile(String fileName) {
        try {
            BufferedReader reader = new BufferedReader(new FileReader(fileName));
            load(reader);
            reader.close();
        } catch (IOException e) {
            System.err.println("IOException: Could not open file " + fileName + ".");
        }
    }

    public String get(String key) {
        return getProperty(key);
    }
}

