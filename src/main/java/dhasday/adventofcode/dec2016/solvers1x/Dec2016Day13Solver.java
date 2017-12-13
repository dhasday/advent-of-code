package dhasday.adventofcode.dec2016.solvers1x;

import java.util.HashSet;
import java.util.Set;

import com.google.common.collect.Sets;
import dhasday.adventofcode.common.DaySolver;
import javafx.util.Pair;

public class Dec2016Day13Solver implements DaySolver<Integer> {
    private static final int INPUT_VALUE = 1358;

    @Override
    public int getDayNumber() {
        return 13;
    }

    @Override
    public Integer solvePuzzleOne() {
        Pair<Integer, Integer> startLocation = new Pair<>(1, 1);
        Pair<Integer, Integer> targetLocation = new Pair<>(31, 39);

        return minStepsToLocation(startLocation, targetLocation, new HashSet<>(), 0, 100);
    }

    @Override
    public Integer solvePuzzleTwo() {
        Pair<Integer, Integer> startLocation = new Pair<>(1, 1);

        Set<Pair<Integer, Integer>> allPossibleLocations = getAllPossibleLocations(startLocation, new HashSet<>(), 50);
        return allPossibleLocations.size();
    }

    private Integer minStepsToLocation(Pair<Integer, Integer> curLoc,
                                       Pair<Integer, Integer> targetLoc,
                                       Set<Pair<Integer, Integer>> visitedStates,
                                       int curMoves,
                                       int remainingMoves) {
        if (curLoc.equals(targetLoc)) {
            return curMoves;
        }
        if (remainingMoves <= 0) {
            return null;
        }

        Set<Pair<Integer, Integer>> newVisitedStates = Sets.newHashSet(visitedStates);

        Integer minMoves = null;
        for (Direction direction : Direction.values()) {
            int nextX = curLoc.getKey() + direction.xOffset;
            int nextY = curLoc.getValue() + direction.yOffset;
            Pair<Integer, Integer> nextLoc = new Pair<>(nextX, nextY);

            if (visitedStates.contains(nextLoc) || isInvalid(nextLoc) || isWall(nextLoc)) {
                continue;
            }

            newVisitedStates.add(nextLoc);
            Integer newMin = minStepsToLocation(nextLoc, targetLoc, newVisitedStates, curMoves + 1, remainingMoves - 1);

            if (newMin != null) {
                if (minMoves == null) {
                    minMoves = newMin;
                } else {
                    minMoves = Math.min(minMoves, newMin);
                }
            }
        }

        return minMoves;
    }

    private Set<Pair<Integer, Integer>> getAllPossibleLocations(Pair<Integer, Integer> curLoc, Set<Pair<Integer, Integer>> accessibleLocations, int remainingMoves) {
        if (remainingMoves <= 0) {
            return accessibleLocations;
        }

        Set<Pair<Integer, Integer>> allAccessibleLocations = Sets.newHashSet(accessibleLocations);

        for (Direction direction : Direction.values()) {
            int nextX = curLoc.getKey() + direction.xOffset;
            int nextY = curLoc.getValue() + direction.yOffset;
            Pair<Integer, Integer> nextLoc = new Pair<>(nextX, nextY);

            if (accessibleLocations.contains(nextLoc) || isInvalid(nextLoc) || isWall(nextLoc)) {
                continue;
            }

            Set<Pair<Integer, Integer>> newAccessibleLocations = Sets.newHashSet(accessibleLocations);
            newAccessibleLocations.add(nextLoc);

            allAccessibleLocations.addAll(getAllPossibleLocations(nextLoc, newAccessibleLocations, remainingMoves - 1));
        }

        return allAccessibleLocations;
    }

    private boolean isInvalid(Pair<Integer, Integer> location) {
        return location.getKey() < 0 || location.getValue() < 0;
    }

    private boolean isWall(Pair<Integer, Integer> location) {
        int x = location.getKey();
        int y = location.getValue();

        int value = (x * x) + (3 * x) + (2 * x * y) + y + (y * y) + INPUT_VALUE;

        String binaryString = Integer.toBinaryString(value);

        boolean result = false;
        for (int i = 0; i < binaryString.length(); i++) {
            if (binaryString.charAt(i) == '1') {
                result = ! result;
            }
        }
        return result;
    }

    private enum Direction {
        NORTH(0, -1),
        SOUTH(0, 1),
        EAST(1, 0),
        WEST(-1, 0);

        final int xOffset;
        final int yOffset;

        Direction(int xOffset, int yOffset) {
            this.xOffset = xOffset;
            this.yOffset = yOffset;
        }
    }
}
