package dhasday.adventofcode.dec2017.solvers2x;

import java.util.HashSet;
import java.util.List;
import java.util.Set;

import javafx.util.Pair;

import dhasday.adventofcode.dec2017.Dec2017DaySolver;

public class Dec2017Day22Solver extends Dec2017DaySolver<Integer> {

    private static final String INPUT_FILE = "src/main/resources/dec2017/22-input";

    // Based on my inputs we go less than 250 in any direction, so these are way overkill, but it's
    // late and I don't want to figure out the exact sizing to fit. Plus doing so would potentially
    // not make this solution work for other inputs (even though it would just be changing these).
    private static final Integer GRID_SIZE = 1000;
    private static final Integer START_OFFSET = 500;

    @Override
    public int getDay() {
        return 22;
    }

    @Override
    public Integer solvePuzzleOne() {
        return solveForNumberOfInfections(12, 12, Direction.UP, 10000, false);
    }

    @Override
    public Integer solvePuzzleTwo() {
        return solveForNumberOfInfections(12, 12, Direction.UP, 10000000, true);
    }

    private int solveForNumberOfInfections(int startX,
                                           int startY,
                                           Direction startDir,
                                           int numCycles,
                                           boolean isAdvancedVirus) {
        NodeStatus[][] infectedNodes = loadInitialInfectedNodes(GRID_SIZE, START_OFFSET);

        int curX = startX + START_OFFSET;
        int curY = startY + START_OFFSET;
        Direction curDir = startDir;

        int numTimesInfect = 0;

        for (int i = 0; i < numCycles; i++) {
            NodeStatus currentStatus = infectedNodes[curX][curY];

            if (currentStatus == null) {
                currentStatus = NodeStatus.CLEAN;
            }

            switch (currentStatus) {
                case CLEAN:
                    curDir = curDir.turnLeft();
                    infectedNodes[curX][curY] = isAdvancedVirus ? NodeStatus.WEAKENED : NodeStatus.INFECTED;
                    numTimesInfect += isAdvancedVirus ? 0 : 1;
                    break;
                case WEAKENED:
                    infectedNodes[curX][curY] = NodeStatus.INFECTED;
                    numTimesInfect++;
                    break;
                case INFECTED:
                    curDir = curDir.turnRight();
                    infectedNodes[curX][curY] = isAdvancedVirus ? NodeStatus.FLAGGED : NodeStatus.CLEAN;
                    break;
                case FLAGGED:
                    curDir = curDir.reverse();
                    infectedNodes[curX][curY] = NodeStatus.CLEAN;
                    break;
                default:
                    throw new RuntimeException("There's *shouldn't* be any way to end up here since we've cased all values in the enum");
            }

            curX += curDir.xOffset;
            curY += curDir.yOffset;
        }

        return numTimesInfect;
    }

    private NodeStatus[][] loadInitialInfectedNodes(int gridSize, int offset) {
        List<String> allFileLines = getAllFileLines(INPUT_FILE);

        Set<Pair<Integer, Integer>> infectedNodes = new HashSet<>();

        for (int i = 0; i < allFileLines.size(); i++) {
            for (int j = 0; j < allFileLines.get(i).length(); j++) {
                if (allFileLines.get(i).charAt(j) == '#') {
                    infectedNodes.add(new Pair<>(j, i));
                }
            }
        }

        NodeStatus[][] nodeStatuses = new NodeStatus[gridSize][gridSize];

        infectedNodes.forEach(p -> nodeStatuses[p.getKey() + offset][p.getValue() + offset] = NodeStatus.INFECTED);

        return nodeStatuses;
    }

    // Enums work great until they don't. I really wanted to just set these values as fields, but
    // Java doesn't support forward referencing enum values (which doesn't make sense to me) so
    // I've collapsed these overrides onto a single line each since it seems just as readable and
    // a lot less verbose looking (same content, fewer line breaks and now it all lines up).
    private enum Direction {
        UP(0, -1) {
            @Override Direction turnLeft()  { return LEFT;  }
            @Override Direction turnRight() { return RIGHT; }
            @Override Direction reverse()   { return DOWN;  }
        },
        DOWN(0, 1) {
            @Override Direction turnLeft()  { return RIGHT; }
            @Override Direction turnRight() { return LEFT;  }
            @Override Direction reverse()   { return UP;    }
        },
        LEFT(-1, 0) {
            @Override Direction turnLeft()  { return DOWN;  }
            @Override Direction turnRight() { return UP;    }
            @Override Direction reverse()   { return RIGHT; }
        },
        RIGHT(1, 0) {
            @Override Direction turnLeft()  { return UP;    }
            @Override Direction turnRight() { return DOWN;  }
            @Override Direction reverse()   { return LEFT;  }
        };

        private final int xOffset;
        private final int yOffset;

        abstract Direction turnLeft();
        abstract Direction turnRight();
        abstract Direction reverse();

        Direction(int xOffset, int yOffset) {
            this.xOffset = xOffset;
            this.yOffset = yOffset;
        }
    }

    private enum NodeStatus {
        CLEAN,
        WEAKENED,
        INFECTED,
        FLAGGED
    }
}
