package dhasday.adventofcode.dec2015.solvers0x;

import java.util.Arrays;
import java.util.List;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

import dhasday.adventofcode.common.DaySolver;

public class Dec2015Day6Solver extends DaySolver<Integer> {

    private static final String INPUT_FILE = "src/main/resources/dec2015/6-input";

    private static final String INSTRUCTION_REGEX = "(turn off|toggle|turn on) ([1-9][0-9]*),([1-9][0-9]*) through ([1-9][0-9]*),([1-9][0-9]*)";

    private Pattern pattern = Pattern.compile(INSTRUCTION_REGEX);

    @Override
    public int getDayNumber() {
        return 6;
    }

    @Override
    public Integer solvePuzzleOne() {
        List<String> allFileLines = getAllFileLines(INPUT_FILE);

        boolean[][] lightField = generateLightField(1000, 1000);

        for (String instruction : allFileLines) {
            processInstruction(lightField, instruction);
        }

        return countOnLights(lightField);
    }

    @Override
    public Integer solvePuzzleTwo() {
        List<String> allFileLines = getAllFileLines(INPUT_FILE);
        int[][] brightnessField = generateBrightnessField(1000, 1000);

        for (String instruction : allFileLines) {
            processInstruction(brightnessField, instruction);
        }

        return sumBrightnessOnLights(brightnessField);
    }

    private boolean[][] generateLightField(int sizeX, int sizeY) {
        return new boolean[sizeX][sizeY];
    }

    private int[][] generateBrightnessField(int sizeX, int sizeY) {
        return new int[sizeX][sizeY];
    }

    private void processInstruction(boolean[][] lightField, String instruction) {
        LightInstruction lightInstruction = parseInstruction(instruction);

        for (int x = lightInstruction.minX(); x <= lightInstruction.maxX(); x++) {
            for (int y = lightInstruction.minY(); y <= lightInstruction.maxY(); y++) {
                lightField[x][y] = lightInstruction.operation.operate(lightField[x][y]);
            }
        }
    }

    private void processInstruction(int[][] lightField, String instruction) {
        LightInstruction lightInstruction = parseInstruction(instruction);

        for (int x = lightInstruction.minX(); x <= lightInstruction.maxX(); x++) {
            for (int y = lightInstruction.minY(); y <= lightInstruction.maxY(); y++) {
                lightField[x][y] = lightInstruction.operation.operate(lightField[x][y]);
            }
        }
    }

    private LightInstruction parseInstruction(String input) {
        Matcher matcher = pattern.matcher(input);

        if (!matcher.matches()) {
            throw new RuntimeException("Didn't match RegEx");
        }

        return new LightInstruction(
                LightOp.fromInstruction(matcher.group(1)),
                Integer.valueOf(matcher.group(2)),
                Integer.valueOf(matcher.group(3)),
                Integer.valueOf(matcher.group(4)),
                Integer.valueOf(matcher.group(5))
        );
    }

    private int countOnLights(boolean[][] lightField) {
        int numLightsOn = 0;

        for (boolean[] lightRow : lightField) {
            for (boolean light : lightRow) {
                if (light) {
                    numLightsOn++;
                }
            }
        }

        return numLightsOn;
    }

    private int sumBrightnessOnLights(int[][] lightField) {
        int totalBightness = 0;

        for (int[] lightRow : lightField) {
            for (int light : lightRow) {
                totalBightness += light;
            }
        }

        return totalBightness;
    }

    private class LightInstruction {
        private LightOp operation;
        private int x1;
        private int y1;
        private int x2;
        private int y2;

        LightInstruction(LightOp operation, int x1, int y1, int x2, int y2) {
            this.operation = operation;
            this.x1 = x1;
            this.y1 = y1;
            this.x2 = x2;
            this.y2 = y2;
        }

        int minX() {
            return Math.min(x1, x2);
        }

        int maxX() {
            return Math.max(x1, x2);
        }

        int minY() {
            return Math.min(y1, y2);
        }

        int maxY() {
            return Math.max(y1, y2);
        }
    }

    private enum LightOp {
        TURN_ON("turn on") {
            @Override
            boolean operate(boolean currentState) {
                return true;
            }
            @Override
            int operate(int currentState) {
                return currentState + 1;
            }
        },
        TURN_OFF("turn off") {
            @Override
            boolean operate(boolean currentState) {
                return false;
            }
            @Override
            int operate(int currentState) {
                return Math.max(currentState - 1, 0);
            }
        },
        TOGGLE("toggle") {
            @Override
            boolean operate(boolean currentState) {
                return !currentState;
            }
            @Override
            int operate(int currentState) {
                return currentState + 2 ;
            }
        };

        abstract boolean operate(boolean currentState);
        abstract int operate(int currentState);
        private String instruction;

        LightOp(String instruction) {
            this.instruction = instruction;
        }

        private static LightOp fromInstruction(String instruction) {
            return Arrays.stream(values())
                    .filter(op -> op.instruction.equals(instruction))
                    .findFirst()
                    .orElseThrow(() -> new RuntimeException("Unknown instruction: " + instruction));
        }
    }
}
