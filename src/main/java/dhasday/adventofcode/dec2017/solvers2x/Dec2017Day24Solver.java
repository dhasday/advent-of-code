package dhasday.adventofcode.dec2017.solvers2x;

import java.util.Comparator;
import java.util.HashSet;
import java.util.Set;

import com.google.common.collect.Sets;
import javafx.util.Pair;

import dhasday.adventofcode.dec2017.Dec2017DaySolver;

public class Dec2017Day24Solver extends Dec2017DaySolver<Integer> {

    private static final String INPUT_FILE = "src/main/resources/dec2017/24-input";

    @Override
    public int getDay() {
        return 24;
    }

    @Override
    public Integer solvePuzzleOne() {
        Pair<Integer, Integer> strongestBridge = findStrongestBridge(
                loadAllPairs(),
                0,
                new Pair<>(0, 0),
                Comparator.comparingInt(Pair::getValue)
        );

        return strongestBridge.getValue();
    }

    @Override
    public Integer solvePuzzleTwo() {
        Pair<Integer, Integer> strongestBridge = findStrongestBridge(
                loadAllPairs(),
                0,
                new Pair<>(0, 0),
                (b1, b2) -> {
                    if (!b1.getKey().equals(b2.getKey())) {
                        return Integer.compare(b1.getKey(), b2.getKey());
                    }

                    return Integer.compare(b1.getValue(), b2.getValue());
                }
        );

        return strongestBridge.getValue();
    }

    private Set<Pair<Integer, Integer>> loadAllPairs() {
        Set<Pair<Integer, Integer>> allPairs = new HashSet<>();

        for (String line : getAllFileLines(INPUT_FILE)) {
            String[] values = line.split("/");
            allPairs.add(new Pair<>(Integer.valueOf(values[0]), Integer.valueOf(values[1])));
        }

        return allPairs;
    }

    private Pair<Integer, Integer> findStrongestBridge(Set<Pair<Integer,Integer>> remainingConnectors,
                                                       int previousConnection,
                                                       Pair<Integer, Integer> curSizeStrength,
                                                       Comparator<Pair<Integer, Integer>> bridgeComparator) {
        if (remainingConnectors.isEmpty()) {
            return curSizeStrength;
        }

        Pair<Integer, Integer> maxSizeStrength = curSizeStrength;

        for (Pair<Integer, Integer> pair : remainingConnectors) {
            Integer nextConnection;
            if (pair.getKey() == previousConnection) {
                nextConnection = pair.getValue();
            } else if (pair.getValue() == previousConnection) {
                nextConnection = pair.getKey();
            } else {
                continue;
            }

            Set<Pair<Integer, Integer>> newRemainingConnectors = Sets.newHashSet(remainingConnectors);
            newRemainingConnectors.remove(pair);

            Pair<Integer, Integer> newSizeStrength = new Pair<>(
                    curSizeStrength.getKey() + 1,
                    curSizeStrength.getValue() + pair.getKey() + pair.getValue()
            );

            Pair<Integer, Integer> possiblePair = findStrongestBridge(newRemainingConnectors, nextConnection, newSizeStrength, bridgeComparator);

            if (bridgeComparator.compare(maxSizeStrength, possiblePair) < 0) {
                maxSizeStrength = possiblePair;
            }
        }

        return maxSizeStrength;
    }
}
