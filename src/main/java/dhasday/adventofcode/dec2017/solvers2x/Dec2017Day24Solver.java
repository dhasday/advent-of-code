package dhasday.adventofcode.dec2017.solvers2x;

import java.util.HashSet;
import java.util.Set;

import com.google.common.collect.Sets;
import javafx.util.Pair;
import org.apache.commons.lang3.tuple.Triple;

import dhasday.adventofcode.dec2017.Dec2017DaySolver;

public class Dec2017Day24Solver extends Dec2017DaySolver<Integer> {

    private static final String INPUT_FILE = "src/main/resources/dec2017/24-input";

    @Override
    public int getDay() {
        return 24;
    }

    @Override
    protected Pair<Integer, Integer> solvePuzzles() {
        Set<Pair<Integer, Integer>> allPairs = loadAllPairs();

        Triple<Integer, Integer, Integer> strongestBridge = findStrongestBridge(allPairs, 0, Triple.of(0, 0, 0));

        return new Pair<>(strongestBridge.getLeft(), strongestBridge.getRight());
    }

    private Set<Pair<Integer, Integer>> loadAllPairs() {
        Set<Pair<Integer, Integer>> allPairs = new HashSet<>();

        for (String line : getAllFileLines(INPUT_FILE)) {
            String[] values = line.split("/");
            allPairs.add(new Pair<>(Integer.valueOf(values[0]), Integer.valueOf(values[1])));
        }

        return allPairs;
    }

    private Triple<Integer, Integer, Integer> findStrongestBridge(Set<Pair<Integer,Integer>> remainingConnectors,
                                                                  int previousConnection,
                                                                  Triple<Integer, Integer, Integer> curAnswer) {
        if (remainingConnectors.isEmpty()) {
            return curAnswer;
        }

        Triple<Integer, Integer, Integer> newAnswer = curAnswer;

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

            Triple<Integer, Integer, Integer> newStrongestBridge = Triple.of(
                    curAnswer.getLeft() + pair.getKey() + pair.getValue(),
                    curAnswer.getMiddle() + 1,
                    curAnswer.getRight() + pair.getKey() + pair.getValue()
            );

            Triple<Integer, Integer, Integer> possibleAnswer = findStrongestBridge(newRemainingConnectors, nextConnection, newStrongestBridge);

            int newLeft = Math.max(possibleAnswer.getLeft(), newAnswer.getLeft());

            if (possibleAnswer.getMiddle().equals(newAnswer.getMiddle())) {
                newAnswer = Triple.of(newLeft, newAnswer.getMiddle(), Math.max(possibleAnswer.getRight(), newAnswer.getRight()));
            } else if (possibleAnswer.getMiddle() > newAnswer.getMiddle()) {
                newAnswer = Triple.of(newLeft, possibleAnswer.getMiddle(), possibleAnswer.getRight());
            } else if (newLeft != newAnswer.getLeft()){
                newAnswer = Triple.of(newLeft, newAnswer.getMiddle(), newAnswer.getRight());
            }
        }

        return newAnswer;
    }
}
