package dhasday.adventofcode.dec2015.solvers0x;

import dhasday.adventofcode.DaySolver;
import org.apache.commons.lang3.builder.EqualsBuilder;
import org.apache.commons.lang3.builder.HashCodeBuilder;
import org.apache.commons.lang3.builder.ToStringBuilder;
import org.apache.commons.lang3.builder.ToStringStyle;

public class Dec2015Day1Solver implements DaySolver<Integer> {

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
        FloorTracker result = processInput(input);
        return result.currentFloor;
    }

    @Override
    public Integer solvePuzzleTwo() {
        String input = getOnlyFileLine(DAY_ONE_INPUT_FILE);
        FloorTracker result = processInput(input);
        return result.firstBasementFloor;
    }

    FloorTracker processInput(String input) {
        FloorTracker floorResults = new FloorTracker();

        for (int i = 0; i < input.length(); i++) {
            char currentChar = input.charAt(i);

            if (LEVEL_UP_CHAR == currentChar) {
                floorResults.currentFloor++;
            } else if (LEVEL_DOWN_CHAR == currentChar){
                floorResults.currentFloor--;

                if (floorResults.currentFloor < 0 && floorResults.firstBasementFloor == null) {
                    floorResults.firstBasementFloor = i + 1;  // Advent of Code uses one based index :(
                }
            }
        }

        return floorResults;
    }

    class FloorTracker {
        int currentFloor = 0;
        Integer firstBasementFloor = null;

        @Override
        public boolean equals(Object o) {
            return EqualsBuilder.reflectionEquals(this, o);
        }

        @Override
        public int hashCode() {
            return HashCodeBuilder.reflectionHashCode(this);
        }

        @Override
        public String toString() {
            return ToStringBuilder.reflectionToString(this, ToStringStyle.SHORT_PREFIX_STYLE);
        }
    }
}
