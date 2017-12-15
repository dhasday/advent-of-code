package dhasday.adventofcode.dec2015.solvers2x;

import dhasday.adventofcode.common.DaySolver;

public class Dec2015Day25Solver extends DaySolver<Long> {

    private static final long MULTIPLE_KEY = 252533;
    private static final long DIVIDE_KEY = 33554393;

    private static final long START_VALUE = 20151125;
    private static final int INPUT_ROW = 2981;
    private static final int INPUT_COL = 3075;

    @Override
    public int getDayNumber() {
        return 25;
    }

    @Override
    public Long solvePuzzleOne() {
        return calculateValue(START_VALUE, INPUT_ROW, INPUT_COL);
    }

    @Override
    public Long solvePuzzleTwo() {
        return null;
    }

    long calculateValue(long startValue, int row, int col) {
        int columnToReach = col + row - 2;

        long currentValue = startValue;

        for (int i = 0; i < columnToReach; i++) {
            for (int j = 0; j <= i; j++) {
                currentValue = calculateNextNumber(currentValue);
            }
        }

        for (int i = 0; i < (col - 1); i++) {
            currentValue = calculateNextNumber(currentValue);
        }

        return currentValue;
    }

    private long calculateNextNumber(long currentNumber) {
        return (currentNumber * MULTIPLE_KEY) % DIVIDE_KEY;
    }
}
