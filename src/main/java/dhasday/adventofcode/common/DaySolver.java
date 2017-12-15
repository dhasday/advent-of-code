package dhasday.adventofcode.common;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.List;

public abstract class DaySolver<T> implements Runnable {

    public abstract int getDayNumber();

    public abstract T solvePuzzleOne();

    public abstract T solvePuzzleTwo();

    protected List<String> getAllFileLines(String filename) {
        try {
            return Files.readAllLines(Paths.get(filename));
        } catch (IOException e) {
            throw new RuntimeException("Failed to read contents of file: " + filename, e);
        }
    }

    protected String getOnlyFileLine(String filename) {
        List<String> allLines = getAllFileLines(filename);

        if (allLines.size() != 1) {
            throw new RuntimeException(String.format("Expected all contents on a single line, but found %s lines", allLines.size()));
        }

        return allLines.get(0);
    }

    @Override
    public void run() {
        long startMillis = System.currentTimeMillis();
        System.out.println(String.format("%2d-1: %s", getDayNumber(), String.valueOf(solvePuzzleOne())));
        System.out.println(String.format("%2d-2: %s", getDayNumber(), String.valueOf(solvePuzzleTwo())));
        long endMillis = System.currentTimeMillis();

        System.out.println(String.format("%2d Elapsed: %d", getDayNumber(), endMillis - startMillis));
    }
}
