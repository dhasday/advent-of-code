package dhasday.adventofcode.dec2017.solvers2x;

import java.util.*;
import java.util.function.Function;

import javafx.util.Pair;

import dhasday.adventofcode.dec2017.Dec2017DaySolver;

public class Dec2017Day22Solver extends Dec2017DaySolver<Integer> {

    private static final String INPUT_FILE = "src/main/resources/dec2017/22-input";

    @Override
    public int getDay() {
        return 22;
    }

    @Override
    public Integer solvePuzzleOne() {
        Set<Pair<Integer, Integer>> infected = loadInitialInfectedNodes();

        Pair<Integer, Integer> curPos = new Pair<>(12, 12);
        Direction curDir = Direction.UP;

        int numTimesInfect = 0;

        for (int i = 0; i < 10000; i++) {
            if (infected.contains(curPos)) {
                curDir = curDir.turnRight();
                infected.remove(curPos);
            } else {
                curDir = curDir.turnLeft();
                infected.add(curPos);
                numTimesInfect++;
            }

            curPos = new Pair<>(curPos.getKey() + curDir.xOffset, curPos.getValue() + curDir.yOffset);
        }

        return numTimesInfect;
    }

    @Override
    public Integer solvePuzzleTwo() {
        Set<Pair<Integer, Integer>> infectedNodes = loadInitialInfectedNodes();
        Map<Pair<Integer, Integer>, NodeStatus> nodesStatus = initializeInfectedNodes(infectedNodes);

        Pair<Integer, Integer> curPos = new Pair<>(12, 12);
        Direction curDir = Direction.UP;

        int numTimesInfect = 0;

        for (int i = 0; i < 10000000; i++) {
            NodeStatus status = nodesStatus.getOrDefault(curPos, NodeStatus.CLEAN);

            curDir = status.nextDir.apply(curDir);

            status = status.nextState();
            switch (status) {
                case CLEAN:
                    nodesStatus.remove(curPos);
                    break;
                case INFECTED:
                    numTimesInfect++;
                default:
                    nodesStatus.put(curPos, status);
            }

            curPos = new Pair<>(curPos.getKey() + curDir.xOffset, curPos.getValue() + curDir.yOffset);
        }

        return numTimesInfect;
    }

    private Set<Pair<Integer, Integer>> loadInitialInfectedNodes() {
        List<String> allFileLines = getAllFileLines(INPUT_FILE);

        Set<Pair<Integer, Integer>> infectedNodes = new HashSet<>();

        for (int i = 0; i < allFileLines.size(); i++) {
            for (int j = 0; j < allFileLines.get(i).length(); j++) {
                if (allFileLines.get(i).charAt(j) == '#') {
                    infectedNodes.add(new Pair<>(j, i));
                }
            }
        }

        return infectedNodes;
    }

    private Map<Pair<Integer, Integer>, NodeStatus> initializeInfectedNodes(Set<Pair<Integer, Integer>> infectedNodes) {
        Map<Pair<Integer, Integer>, NodeStatus> nodeState = new HashMap<>();

        infectedNodes.forEach(n -> nodeState.put(n, NodeStatus.INFECTED));

        return nodeState;
    }

    private enum Direction {
        UP(0, -1) {
            @Override
            Direction turnLeft() {
                return LEFT;
            }

            @Override
            Direction turnRight() {
                return RIGHT;
            }

            @Override
            Direction reverse() {
                return DOWN;
            }
        },
        DOWN(0, 1) {
            @Override
            Direction turnLeft() {
                return RIGHT;
            }

            @Override
            Direction turnRight() {
                return LEFT;
            }

            @Override
            Direction reverse() {
                return UP;
            }
        },
        LEFT(-1, 0) {
            @Override
            Direction turnLeft() {
                return DOWN;
            }

            @Override
            Direction turnRight() {
                return UP;
            }

            @Override
            Direction reverse() {
                return RIGHT;
            }
        },
        RIGHT(1, 0) {
            @Override
            Direction turnLeft() {
                return UP;
            }

            @Override
            Direction turnRight() {
                return DOWN;
            }

            @Override
            Direction reverse() {
                return LEFT;
            }
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
        CLEAN(Direction::turnLeft) {
            @Override
            NodeStatus nextState() {
                return WEAKENED;
            }
        },
        WEAKENED(curDir -> curDir) {
            @Override
            NodeStatus nextState() {
                return INFECTED;
            }
        },
        INFECTED(Direction::turnRight) {
            @Override
            NodeStatus nextState() {
                return FLAGGED;
            }
        },
        FLAGGED(Direction::reverse) {
            @Override
            NodeStatus nextState() {
                return CLEAN;
            }
        };

        private Function<Direction, Direction> nextDir;

        abstract NodeStatus nextState();

        NodeStatus(Function<Direction, Direction> nextDir) {
            this.nextDir = nextDir;
        }
    }
}
