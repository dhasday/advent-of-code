package dhasday.adventofcode.dec2017.solvers1x;

import java.util.ArrayList;
import java.util.List;

import dhasday.adventofcode.common.DaySolver;
import javafx.util.Pair;

public class Dec2017Day13Solver implements DaySolver<Integer> {

    private static final String INPUT_FILE = "src/main/resources/dec2017/13-input";

    @Override
    public int getDayNumber() {
        return 13;
    }

    @Override
    public Integer solvePuzzleOne() {
        List<Pair<Integer, Integer>> allScanners = loadAllScanners();

        int sum = 0;
        for (Pair<Integer, Integer> scanner : allScanners) {
            Integer depth = scanner.getKey();
            Integer range = scanner.getValue();

            if (isCaptured(depth, range, 0)) {
                sum += (depth * range);
            }
        }
        return sum;
    }

    @Override
    public Integer solvePuzzleTwo() {
        List<Pair<Integer, Integer>> allScanners = loadAllScanners();

        for (int i = 0; i < 10000000; i++) {
            if (!anyCaptured(allScanners, i)) {
                return i;
            }
        }

        return null;
    }

    private List<Pair<Integer, Integer>> loadAllScanners() {
        List<Pair<Integer, Integer>> allScanners = new ArrayList<>();

        for (String input : getAllFileLines(INPUT_FILE)) {
            String[] splitInput = input.split(": ");
            allScanners.add(new Pair<>(Integer.valueOf(splitInput[0]), Integer.valueOf(splitInput[1])));
        }

        return allScanners;
    }

    private boolean isCaptured(Integer depth, Integer range, int delay) {
        return (depth + delay) % (2 * (range - 1)) == 0;
    }

    private boolean anyCaptured(List<Pair<Integer, Integer>> allScanners, int delay) {
        for (Pair<Integer, Integer> entry : allScanners) {
            if (isCaptured(entry.getKey(), entry.getValue(), delay)) {
                return true;
            }
        }
        return false;
    }
}
