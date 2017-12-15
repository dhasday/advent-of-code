package dhasday.adventofcode.dec2017.solvers1x;

import java.util.Arrays;
import java.util.List;
import java.util.stream.Collectors;

import dhasday.adventofcode.common.DaySolver;

public class Dec2017Day11Solver extends DaySolver<Integer> {

    private static final String INPUT_FILE = "src/main/resources/dec2017/11-input";

    @Override
    public int getDayNumber() {
        return 11;
    }

    @Override
    public Integer solvePuzzleOne() {
        List<HexMove> allMoves = loadMoves();

        int startX = 0;
        int startY = 0;

        int curX = startX;
        int curY = startY;

        for (HexMove hexMove : allMoves) {
            curX += hexMove.offsetX;
            curY += hexMove.offsetY;
        }

        return calculateDistance(startX, startY, curX, curY);
    }

    @Override
    public Integer solvePuzzleTwo() {
        List<HexMove> allMoves = loadMoves();

        int startX = 0;
        int startY = 0;

        int curX = startX;
        int curY = startY;
        int maxDistance = 0;

        for (HexMove hexMove : allMoves) {
            curX += hexMove.offsetX;
            curY += hexMove.offsetY;
            maxDistance = Math.max(maxDistance, calculateDistance(startX, startY, curX, curY));
        }

        return maxDistance;
    }

    private List<HexMove> loadMoves() {
        return Arrays.stream(getOnlyFileLine(INPUT_FILE).split(","))
                .map(HexMove::forSymbol)
                .collect(Collectors.toList());
    }

    private int calculateDistance(int xOne, int yOne, int xTwo, int yTwo) {
        int zOne = 0 - xOne - yOne;
        int zTwo = 0 - xTwo - yTwo;

        return Math.max(Math.abs(xTwo - xOne), Math.max(Math.abs(yTwo - yOne), Math.abs(zTwo - zOne)));
    }

    private enum HexMove {
        NORTH_WEST  ("nw", -1,  0),
        NORTH       ( "n", -1,  1),
        NORTH_EAST  ("ne",  0,  1),
        SOUTH_EAST  ("se",  1,  0),
        SOUTH       ( "s",  1, -1),
        SOUTH_WEST  ("sw",  0, -1);

        private final String symbol;
        private final int offsetX;
        private final int offsetY;

        HexMove(String symbol, int offsetX, int offsetY) {
            this.symbol = symbol;
            this.offsetX = offsetX;
            this.offsetY = offsetY;
        }

        private static HexMove forSymbol(String symbol) {
            return Arrays.stream(values())
                    .filter(m -> m.symbol.equals(symbol))
                    .findFirst()
                    .orElseThrow(() -> new RuntimeException("Unable to match symbol: " + symbol));
        }
    }
}
