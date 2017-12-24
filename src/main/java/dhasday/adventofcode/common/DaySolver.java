package dhasday.adventofcode.common;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.List;

import javafx.util.Pair;

public abstract class DaySolver<T> {
    private static final long SLOW_ELAPSED_THRESHOLD = 1500L;

    protected abstract int getYear();
    protected abstract int getDay();

    public T solvePuzzleOne() {
        throw new RuntimeException("Solving puzzle one would be easier with an implementation.");
    }

    public T solvePuzzleTwo() {
        throw new RuntimeException("Solving puzzle one would be easier with an implementation.");
    }

    public void printResults() {
        long startTime = System.currentTimeMillis();
        Pair<T, T> solutions = solvePuzzles();
        System.out.println(String.format("%4d Day %2d-1: %s", getYear(), getDay(), String.valueOf(solutions.getKey())));
        System.out.println(String.format("%4d Day %2d-2: %s", getYear(), getDay(), String.valueOf(solutions.getValue())));
        long endTime = System.currentTimeMillis();

        long elapsedTime = endTime - startTime;
        System.out.println(String.format(
                "%sElapsed Time: %d ms",
                elapsedTime >= SLOW_ELAPSED_THRESHOLD ? "*** " : "",
                elapsedTime
        ));
    }

    protected Pair<T, T> solvePuzzles() {
        return new Pair<>(solvePuzzleOne(), solvePuzzleTwo());
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
