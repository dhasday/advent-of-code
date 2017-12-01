package dhasday.adventofcode;

import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.util.List;
import java.util.stream.Collectors;

public class FileUtils {

    public String loadFileContents(String filename) {
        List<String> allLines = loadFileLines(filename);

        if (allLines.size() != 1) {
            throw new RuntimeException(String.format("Expected all contents on a single line, but found %s lines", allLines.size()));
        }

        return allLines.get(0);
    }

    public List<String> loadFileLines(String filename) {
        try {
            FileReader fileReader = new FileReader(filename);

            BufferedReader bufferedReader = new BufferedReader(fileReader);
            return bufferedReader.lines().collect(Collectors.toList());
        } catch (IOException e) {
            throw new RuntimeException("Failed to read contents of file: " + filename, e);
        }
    }
}
