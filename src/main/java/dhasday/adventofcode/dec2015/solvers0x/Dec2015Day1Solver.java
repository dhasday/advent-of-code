package dhasday.adventofcode.dec2015.solvers0x;

import dhasday.adventofcode.DaySolver;
import dhasday.adventofcode.dec2015.domain.Day1FloorTracker;

public class Dec2015Day1Solver implements DaySolver {

    private static final String DAY_ONE_INPUT_FILE = "src/main/resources/dec2015/1-input";

    private static final int LEVEL_UP_CHAR = '(';
    private static final int LEVEL_DOWN_CHAR = ')';

    @Override
    public int getDayNumber() {
        return 1;
    }

    @Override
    public Integer solvePuzzleOne() {
        String input = getOnlyFileLine(DAY_ONE_INPUT_FILE);
        Day1FloorTracker result = processInput(input);
        return result.getCurrentFloor();
    }

    @Override
    public Integer solvePuzzleTwo() {
        String input = getOnlyFileLine(DAY_ONE_INPUT_FILE);
        Day1FloorTracker result = processInput(input);
        return result.getFirstBasementFloor();
    }

    Day1FloorTracker processInput(String input) {
        Day1FloorTracker floorResults = new Day1FloorTracker();

        for (int i = 0; i < input.length(); i++) {
            char currentChar = input.charAt(i);

            if (LEVEL_UP_CHAR == currentChar) {
                floorResults.setCurrentFloor(floorResults.getCurrentFloor() + 1);
            } else if (LEVEL_DOWN_CHAR == currentChar){
                floorResults.setCurrentFloor(floorResults.getCurrentFloor() - 1);

                if (floorResults.getCurrentFloor() < 0 && floorResults.getFirstBasementFloor() == null) {
                    floorResults.setFirstBasementFloor(i + 1);  // Advent of Code uses one based index :(
                }
            }
        }

        return floorResults;
    }
}
