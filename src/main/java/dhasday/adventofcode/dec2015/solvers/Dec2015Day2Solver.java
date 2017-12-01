package dhasday.adventofcode.dec2015.solvers;

import java.util.ArrayList;
import java.util.Comparator;
import java.util.List;

import dhasday.adventofcode.DaySolver;

public class Dec2015Day2Solver implements DaySolver {

    private static final String INPUT_FILE = "src/main/resources/dec2015/2-input";

    @Override
    public int getDayNumber() {
        return 2;
    }

    @Override
    public Integer solvePuzzleOne() {
        List<String> allDimensions = fileUtils.loadFileLines(INPUT_FILE);

        return allDimensions.stream()
                .mapToInt(this::calculateNeededWrappingPaper)
                .sum();
    }

    @Override
    public Integer solvePuzzleTwo() {
        List<String> allDimensions = fileUtils.loadFileLines(INPUT_FILE);

        return allDimensions.stream()
                .mapToInt(this::calculateNeededRibbon)
                .sum();
    }

    int calculateNeededWrappingPaper(String input) {
        Dimensions dimensions = parseDimensions(input);

        int sideOne = dimensions.length * dimensions.width;
        int sideTwo = dimensions.length * dimensions.depth;
        int sideThree = dimensions.width * dimensions.depth;

        int smallestSide = Math.min(sideOne, Math.min(sideTwo, sideThree));

        return (sideOne * 2) + (sideTwo * 2) + (sideThree * 2) + smallestSide;
    }
    
    int calculateNeededRibbon(String input) {
        Dimensions dimensions = parseDimensions(input);

        int perimeter = determineMinimumPerimeter(dimensions);
        int volume = dimensions.length * dimensions.width * dimensions.depth;

        return perimeter + volume;
    }

    private Dimensions parseDimensions(String input) {
        String[] rawDimensions = input.split("x");
        if (rawDimensions.length != 3) {
            throw new RuntimeException("'" + input + "' does not have 3 parts separated with 'x'");
        }

        return new Dimensions(
                Integer.valueOf(rawDimensions[0]),
                Integer.valueOf(rawDimensions[1]),
                Integer.valueOf(rawDimensions[2])
        );
    }

    private int determineMinimumPerimeter(Dimensions dimensions) {
        List<Integer> sides = new ArrayList<>();
        sides.add(dimensions.length);
        sides.add(dimensions.width);
        sides.add(dimensions.depth);

        sides.sort(Comparator.naturalOrder());

        return (sides.get(0) + sides.get(1)) * 2;
    }

    private class Dimensions {
        private final int length;
        private final int width;
        private final int depth;

        public Dimensions(int length, int width, int depth) {
            this.length = length;
            this.width = width;
            this.depth = depth;
        }
    }
}
