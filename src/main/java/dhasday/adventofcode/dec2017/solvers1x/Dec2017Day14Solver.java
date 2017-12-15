package dhasday.adventofcode.dec2017.solvers1x;

import java.util.Arrays;
import java.util.Deque;
import java.util.HashSet;
import java.util.LinkedList;
import java.util.Set;
import java.util.function.Function;

import dhasday.adventofcode.common.DaySolver;
import dhasday.adventofcode.dec2017.common.KnotHash;
import javafx.util.Pair;
import org.apache.commons.lang3.StringUtils;

public class Dec2017Day14Solver extends DaySolver<Integer> {

    private static final String INPUT = "jxqlasbh";

    private static final int RESULT_LENGTH = 128;

    private KnotHash knotHash = new KnotHash();

    @Override
    public int getDayNumber() {
        return 14;
    }

    @Override
    public Integer solvePuzzleOne() {
        int usedCount = 0;

        for (int i = 0; i < RESULT_LENGTH; i++) {
            String binaryHash = knotHash.computeBinaryHash(INPUT + "-" + i);
            usedCount += StringUtils.countMatches(binaryHash, '1');
        }

        return usedCount;
    }

    @Override
    public Integer solvePuzzleTwo() {
        boolean[][] binaryResultMatrix = new boolean[RESULT_LENGTH][RESULT_LENGTH];

        for (int i = 0; i < RESULT_LENGTH; i++) {
            String binaryHash = knotHash.computeBinaryHash(INPUT + "-" + i);
            for (int j = 0; j < RESULT_LENGTH; j++) {
                binaryResultMatrix[i][j] = binaryHash.charAt(j) == '1';
            }
        }

        return countRegions(binaryResultMatrix);
    }

    private Integer countRegions(boolean[][] matrix) {
        int regionCount = 0;
        Set<Pair<Integer, Integer>> closedSet = new HashSet<>();

        for (int x = 0; x < RESULT_LENGTH; x++) {
            for (int y = 0; y < RESULT_LENGTH; y++) {
                Pair<Integer, Integer> curPair = new Pair<>(x, y);
                if (closedSet.contains(curPair)) {
                    continue;
                }

                if (matrix[x][y]) {
                    removeConnectedPairs(matrix, closedSet, x, y);
                    regionCount++;
                } else {
                    closedSet.add(curPair);
                }
            }
        }

        return regionCount;
    }

    private void removeConnectedPairs(boolean[][] matrix,
                                      Set<Pair<Integer, Integer>> closedSet,
                                      int x,
                                      int y) {
        Deque<Pair<Integer, Integer>> openSet = new LinkedList<>();
        openSet.add(new Pair<>(x, y));

        while (!openSet.isEmpty()) {
            Pair<Integer, Integer> curPair = openSet.removeFirst();
            closedSet.add(curPair);

            if (!matrix[curPair.getKey()][curPair.getValue()]) {
                continue;
            }

            Arrays.stream(Direction.values())
                    .filter(d -> d.isValid.apply(curPair))
                    .map(d -> new Pair<>(curPair.getKey() + d.xOffset, curPair.getValue() + d.yOffset))
                    .filter(p -> !closedSet.contains(p) && !openSet.contains(p))
                    .forEach(openSet::add);
        }
    }

    private enum Direction {
        UP(     0,  -1,  p -> p.getValue() > 0),
        DOWN(   0,   1,  p -> p.getValue() < RESULT_LENGTH - 1),
        LEFT(  -1,   0,  p -> p.getKey() > 0),
        RIGHT(  1,   0,  p -> p.getKey() < RESULT_LENGTH - 1);

        private final int xOffset;
        private final int yOffset;
        private final Function<Pair<Integer, Integer>, Boolean> isValid;

        Direction(int xOffset, int yOffset, Function<Pair<Integer, Integer>, Boolean> isValid) {
            this.xOffset = xOffset;
            this.yOffset = yOffset;
            this.isValid = isValid;
        }
    }
}