package dhasday.adventofcode.dec2016.solvers0x;

import java.util.HashSet;
import java.util.List;
import java.util.Set;
import java.util.regex.Matcher;
import java.util.regex.Pattern;
import java.util.stream.Collectors;

import dhasday.adventofcode.common.DaySolver;
import javafx.util.Pair;

public class Dec2016Day1Solver extends DaySolver<Integer> {

    private static final String INPUT_FILE = "src/main/resources/dec2016/1-input";

    private static final String INPUT_REGEX = "([RL])(\\d+)";

    private Pattern inputPattern = Pattern.compile(INPUT_REGEX);

    @Override
    public int getDayNumber() {
        return 1;
    }

    @Override
    public Integer solvePuzzleOne() {
        List<String> allFileLines = getAllFileLines(INPUT_FILE);

        List<Instruction> allInstructions = loadInstructions(allFileLines);

        Pair<Integer, Integer> finalPosition = findFinalLocation(allInstructions);

        return determineDistance(finalPosition);
    }

    @Override
    public Integer solvePuzzleTwo() {
        List<String> allFileLines = getAllFileLines(INPUT_FILE);

        List<Instruction> allInstructions = loadInstructions(allFileLines);

        Pair<Integer, Integer> finalPosition = findFirstIntersection(allInstructions);

        return determineDistance(finalPosition);
    }

    private List<Instruction> loadInstructions(List<String> allInputs) {
        return allInputs.stream()
                .map(this::processInstruction)
                .collect(Collectors.toList());
    }

    private Instruction processInstruction(String input) {
        Matcher matcher = inputPattern.matcher(input);

        if (!matcher.matches()) {
            throw new RuntimeException("That wasn't supposed to happen");
        }

        return new Instruction(
                "R".equals(matcher.group(1)) ? true : false,
                Integer.valueOf(matcher.group(2))
        );
    }

    private Integer determineDistance(Pair<Integer, Integer> position) {
        return Math.abs(position.getKey()) + Math.abs(position.getValue());
    }


    private Pair<Integer, Integer> findFinalLocation(List<Instruction> allInstructions) {
        Direction currentDirection = Direction.NORTH;
        Pair<Integer, Integer> currentPosition = new Pair<>(0, 0);

        for (Instruction instruction : allInstructions) {
            if (instruction.turnRight) {
                currentDirection = currentDirection.turnRight();
            } else {
                currentDirection = currentDirection.turnLeft();
            }

            currentPosition = currentDirection.move(currentPosition, instruction.numSteps);
        }

        return currentPosition;
    }

    private Pair<Integer, Integer> findFirstIntersection(List<Instruction> allInstructions) {
        Direction currentDirection = Direction.NORTH;
        Pair<Integer, Integer> currentPosition = new Pair<>(0, 0);

        Set<Pair<Integer, Integer>> visitedLocations = new HashSet<>();
        visitedLocations.add(currentPosition);

        for (Instruction instruction : allInstructions) {
            if (instruction.turnRight) {
                currentDirection = currentDirection.turnRight();
            } else {
                currentDirection = currentDirection.turnLeft();
            }

            for (int i = 0; i < instruction.numSteps; i++) {
                currentPosition = currentDirection.move(currentPosition, 1);
                if (visitedLocations.contains(currentPosition)) {
                    return currentPosition;
                }
                visitedLocations.add(currentPosition);
            }
        }

        return null;
    }

    private class Instruction {
        private boolean turnRight;
        private int numSteps;

        public Instruction(boolean turnRight, int numSteps) {
            this.turnRight = turnRight;
            this.numSteps = numSteps;
        }
    }

    private enum Direction {
        NORTH {
            @Override
            Direction turnLeft() {
                return WEST;
            }

            @Override
            Direction turnRight() {
                return EAST;
            }

            @Override
            Pair<Integer, Integer> move(Pair<Integer, Integer> currentPosition, int numSteps) {
                return new Pair<>(
                        currentPosition.getKey(),
                        currentPosition.getValue() + numSteps
                );
            }
        },
        SOUTH {
            @Override
            Direction turnLeft() {
                return EAST;
            }

            @Override
            Direction turnRight() {
                return WEST;
            }

            @Override
            Pair<Integer, Integer> move(Pair<Integer, Integer> currentPosition, int numSteps) {
                return new Pair<>(
                        currentPosition.getKey(),
                        currentPosition.getValue() - numSteps
                );
            }
        },
        EAST {
            @Override
            Direction turnLeft() {
                return NORTH;
            }

            @Override
            Direction turnRight() {
                return SOUTH;
            }

            @Override
            Pair<Integer, Integer> move(Pair<Integer, Integer> currentPosition, int numSteps) {
                return new Pair<>(
                        currentPosition.getKey() + numSteps,
                        currentPosition.getValue()
                );
            }
        },
        WEST {
            @Override
            Direction turnLeft() {
                return SOUTH;
            }

            @Override
            Direction turnRight() {
                return NORTH;
            }

            @Override
            Pair<Integer, Integer> move(Pair<Integer, Integer> currentPosition, int numSteps) {
                return new Pair<>(
                        currentPosition.getKey() - numSteps,
                        currentPosition.getValue()
                );
            }
        };

        abstract Direction turnLeft();
        abstract Direction turnRight();
        abstract Pair<Integer, Integer> move(Pair<Integer, Integer> currentPosition, int numSteps);
    }
}
