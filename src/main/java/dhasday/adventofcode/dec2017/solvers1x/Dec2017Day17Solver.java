package dhasday.adventofcode.dec2017.solvers1x;

import java.util.LinkedList;
import java.util.List;

import dhasday.adventofcode.dec2017.Dec2017DaySolver;

public class Dec2017Day17Solver extends Dec2017DaySolver<Integer> {

    private static final Integer INPUT = 376;

    @Override
    public int getDay() {
        return 17;
    }

    @Override
    public Integer solvePuzzleOne() {
        List<Integer> values = new LinkedList<>();
        values.add(0);

        int curPos = 0;
        for (int i = 1; i <= 2017; i++) {
            curPos = ((curPos + INPUT) % (values.size())) + 1;
            values.add(curPos, i);
        }

        return values.get((curPos + 1) % values.size());
    }

    @Override
    public Integer solvePuzzleTwo() {
        int valueAfterZero = 0;

        int curPos = 1;
        for (int i = 1; i <= 50000000; i++) {
            if (curPos == 1) {
                valueAfterZero = i;
            }
            curPos = ((curPos + INPUT) % (i + 1)) + 1;
        }

        return valueAfterZero;
    }
}
