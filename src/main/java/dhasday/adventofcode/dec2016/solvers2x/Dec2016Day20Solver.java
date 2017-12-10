package dhasday.adventofcode.dec2016.solvers2x;

import dhasday.adventofcode.DaySolver;

public class Dec2016Day20Solver implements DaySolver<Long> {

    private static final String INPUT_FILE = "src/main/resources/dec2016/20-input-sorted";

    @Override
    public int getDayNumber() {
        return 20;
    }

    @Override
    public Long solvePuzzleOne() {
        long currentMin = 0;

        for (String range : getAllFileLines(INPUT_FILE)) {
            String[] splitRange = range.split("-");

            Long start = Long.valueOf(splitRange[0]);
            Long end = Long.valueOf(splitRange[1]);

            if (start > (currentMin + 1)) {
                return currentMin + 1;
            }

            currentMin = Math.max(currentMin, end);
        }

        return currentMin;
    }

    @Override
    public Long solvePuzzleTwo() {
        long currentMin = 0;
        long numUnblocked = 0;

        for (String range : getAllFileLines(INPUT_FILE)) {
            String[] splitRange = range.split("-");

            Long start = Long.valueOf(splitRange[0]);
            Long end = Long.valueOf(splitRange[1]);

            if (start > (currentMin + 1)) {
                numUnblocked += start - currentMin - 1;
            }

            currentMin = Math.max(currentMin, end);
        }

        return numUnblocked;
    }
}
