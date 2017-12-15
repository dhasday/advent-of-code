package dhasday.adventofcode.dec2015.solvers0x;

import java.util.ArrayList;
import java.util.HashSet;
import java.util.List;
import java.util.Set;

import dhasday.adventofcode.common.DaySolver;
import javafx.util.Pair;

public class Dec2015Day3Solver extends DaySolver<Integer> {

    private static final String INPUT_FILE = "src/main/resources/dec2015/3-input";

    private static final char CHAR_NORTH = '^';
    private static final char CHAR_SOUTH = 'v';
    private static final char CHAR_EAST = '>';
    private static final char CHAR_WEST = '<';

    @Override
    public int getDayNumber() {
        return 3;
    }

    @Override
    public Integer solvePuzzleOne() {
        String input = getOnlyFileLine(INPUT_FILE);
        return deliverPresents(input, 1);
    }

    @Override
    public Integer solvePuzzleTwo() {
        String input = getOnlyFileLine(INPUT_FILE);
        return deliverPresents(input, 2);
    }

    int deliverPresents(String input, int numDeliverers) {
        List<Pair<Integer, Integer>> currentLocations = new ArrayList<>();
        Pair<Integer, Integer> startingLocation = new Pair<>(0, 0);
        for (int i = 0; i < numDeliverers; i++) {
            currentLocations.add(startingLocation);
        }

        Set<Pair<Integer, Integer>> visitedHouses = new HashSet<>();
        visitedHouses.add(startingLocation);

        for (int i = 0; i < input.length(); i++) {
            int delivererIndex = i % numDeliverers;

            Pair<Integer, Integer> currentLocation = currentLocations.get(delivererIndex);

            currentLocation = getNextLocation(currentLocation, input.charAt(i));

            currentLocations.set(delivererIndex, currentLocation);

            visitedHouses.add(currentLocation);
        }

        return visitedHouses.size();
    }

    private Pair<Integer, Integer> getNextLocation(Pair<Integer, Integer> currentLocation, char movement) {
        int xAdjust = 0;
        int yAdjust = 0;

        switch (movement) {
            case CHAR_NORTH:
                yAdjust = 1;
                break;
            case CHAR_SOUTH:
                yAdjust = -1;
                break;
            case CHAR_EAST:
                xAdjust = -1;
                break;
            case CHAR_WEST:
                xAdjust = 1;
                break;
        }

        return new Pair<>(currentLocation.getKey() + xAdjust, currentLocation.getValue() + yAdjust);
    }
}
