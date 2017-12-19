package dhasday.adventofcode.dec2017.solvers1x;

import java.util.List;
import java.util.Set;

import com.google.common.collect.ImmutableSet;
import dhasday.adventofcode.dec2017.Dec2017DaySolver;
import javafx.util.Pair;

public class Dec2017Day19Solver extends Dec2017DaySolver<String> {

    private static final String INPUT_FILE = "src/main/resources/dec2017/19-input";

    @Override
    public int getDay() {
        return 19;
    }

    @Override
    public String solvePuzzleOne() {
        char[][] grid = loadGrid();

        return followLineForResults(grid).getKey();
    }

    @Override
    public String solvePuzzleTwo() {
        char[][] grid = loadGrid();

        return String.valueOf(followLineForResults(grid).getValue());
    }

    private char[][] loadGrid() {
        char[][] grid = new char[200][200];

        List<String> allFileLines = getAllFileLines(INPUT_FILE);

        for (int i = 0; i < allFileLines.size(); i++) {
            String line = allFileLines.get(i);
            for (int j = 0; j < line.length(); j++) {
                char character = line.charAt(j);

                if (character == ' ') {
                    grid[i][j] = 0;
                } else {
                    grid[i][j] = character;
                }
            }
        }

        return grid;
    }

    private Pair<String, Integer> followLineForResults(char[][] grid) {
        int curY = 0;
        int curX = findEntrypoint(grid[curY]);
        Direction curDirection = Direction.DOWN;

        int numSteps = 0;
        String seenLetters = "";

        while ((curX >= 0 && curX < 200) && (curY >= 0 && curY < 200) && grid[curY][curX] != 0) {
            char cur = grid[curY][curX];

            switch (cur) {
                case '+':
                    curDirection = findNextDirection(grid, curX, curY, curDirection);
                    break;
                case '|':
                case '-':
                    // Nothing to do for these characters, just continue
                    break;
                default:
                    // It's a letter so record it
                    seenLetters += cur;
            }

            curX += curDirection.xOffset;
            curY += curDirection.yOffset;
            numSteps++;
        }

        return new Pair<>(seenLetters, numSteps);
    }

    private int findEntrypoint(char[] row) {
        for (int i = 0; i < row.length; i++) {
            if (row[i] == '|') {
                return i;
            }
        }
        throw new RuntimeException("Start not found.");
    }

    private Direction findNextDirection(char[][] grid,
                                        int curX,
                                        int curY,
                                        Direction curDirection) {


        return curDirection.getTurnDirections()
                .stream()
                .filter(d -> {
                    int newX = curX + d.xOffset;
                    int newY = curY + d.yOffset;

                    if (newX < 0 || newX >= 200 || newY < 0 || newY >= 200) {
                        return false;
                    }

                    return grid[newY][newX] != 0;
                })
                .findFirst()
                .orElseThrow(() -> new RuntimeException("Zoolander-esque issues"));
    }


    private enum Direction {
        UP(0, -1) {
            @Override
            Set<Direction> getTurnDirections() {
                return ImmutableSet.of(RIGHT, LEFT);
            }
        },
        DOWN(0, 1) {
            @Override
            Set<Direction> getTurnDirections() {
                return ImmutableSet.of(RIGHT, LEFT);
            }
        },
        LEFT(-1, 0) {
            @Override
            Set<Direction> getTurnDirections() {
                return ImmutableSet.of(UP, DOWN);
            }
        },
        RIGHT(1, 0) {
            @Override
            Set<Direction> getTurnDirections() {
                return ImmutableSet.of(UP, DOWN);
            }
        };

        private final int xOffset;
        private final int yOffset;

        abstract Set<Direction> getTurnDirections();

        Direction(int xOffset, int yOffset) {
            this.xOffset = xOffset;
            this.yOffset = yOffset;
        }
    }
}
