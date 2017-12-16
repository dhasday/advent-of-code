package dhasday.adventofcode.common;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.List;

public abstract class DaySolver<T> {
    private static final long SLOW_ELAPSED_THRESHOLD = 1000L;

    protected abstract int getYear();
    protected abstract int getDay();

    public abstract T solvePuzzleOne();

    public abstract T solvePuzzleTwo();

    public void printResults() {
        long startTime = System.currentTimeMillis();
        System.out.println(String.format("%4d Day %2d-1: %s", getYear(), getDay(), String.valueOf(solvePuzzleOne())));
        System.out.println(String.format("%4d Day %2d-2: %s", getYear(), getDay(), String.valueOf(solvePuzzleTwo())));
        long endTime = System.currentTimeMillis();

        long elapsedTime = endTime - startTime;
        System.out.println(String.format(
                "%sElapsed Time: %d ms",
                elapsedTime >= SLOW_ELAPSED_THRESHOLD ? "*** " : "",
                elapsedTime
        ));
    }

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
}
