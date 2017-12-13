package dhasday.adventofcode.common;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.List;

public interface DaySolver<T> {

    int getDayNumber();

    T solvePuzzleOne();

    T solvePuzzleTwo();

    default List<String> getAllFileLines(String filename) {
        try {
            return Files.readAllLines(Paths.get(filename));
        } catch (IOException e) {
            throw new RuntimeException("Failed to read contents of file: " + filename, e);
        }
    }

    default String getOnlyFileLine(String filename) {
        List<String> allLines = getAllFileLines(filename);

        if (allLines.size() != 1) {
            throw new RuntimeException(String.format("Expected all contents on a single line, but found %s lines", allLines.size()));
        }

        return allLines.get(0);
    }

}
