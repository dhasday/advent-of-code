package dhasday.adventofcode.dec2017.solvers1x;

import dhasday.adventofcode.dec2017.Dec2017DaySolver;

public class Dec2017Day15Solver extends Dec2017DaySolver<Integer> {

    private static final long INPUT_GEN_A_START = 783L;
    private static final long INPUT_GEN_B_START = 325L;

    private static final int GEN_A_FACTOR = 16807;
    private static final int GEN_B_FACTOR = 48271;
    private static final int DIVIDEND = 2147483647;
    private static final long BITMASK = 0x0000ffffL;

    public static void main(String[] args) {
        new Dec2017Day15Solver().printResults();
    }

    @Override
    public int getDay() {
        return 15;
    }

    @Override
    public Integer solvePuzzleOne() {
        long valueGenA = INPUT_GEN_A_START;
        long valueGenB = INPUT_GEN_B_START;

        int matchCount = 0;
        for (int i = 0; i < 40000000; i++) {
            valueGenA = computeNextValue(valueGenA, GEN_A_FACTOR, 1);
            valueGenB = computeNextValue(valueGenB, GEN_B_FACTOR, 1);

            if (areLastSixteenBitsEqual(valueGenA, valueGenB)) {
                matchCount++;
            }
        }

        return matchCount;
    }

    @Override
    public Integer solvePuzzleTwo() {
        long valueGenA = INPUT_GEN_A_START;
        long valueGenB = INPUT_GEN_B_START;

        int matchCount = 0;
        for (int i = 0; i < 5000000; i++) {
            valueGenA = computeNextValue(valueGenA, GEN_A_FACTOR, 4);
            valueGenB = computeNextValue(valueGenB, GEN_B_FACTOR, 8);

            if (areLastSixteenBitsEqual(valueGenA, valueGenB)) {
                matchCount++;
            }
        }

        return matchCount;
    }

    private long computeNextValue(long currentValue, int factor, int requiredMultiple) {
        long nextValue = currentValue;

        do {
            nextValue = (nextValue * factor) % DIVIDEND;
        } while (nextValue % requiredMultiple != 0);

        return nextValue;
    }

    private boolean areLastSixteenBitsEqual(long valueOne, long valueTwo) {
        return (valueOne & BITMASK) == (valueTwo & BITMASK);
    }
}