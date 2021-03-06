package dhasday.adventofcode.dec2016.solvers0x;

import java.util.Arrays;
import java.util.List;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

import dhasday.adventofcode.dec2016.Dec2016DaySolver;

public class Dec2016Day8Solver extends Dec2016DaySolver<String> {

    private static final String INPUT_FILE = "src/main/resources/dec2016/8-input";

    @Override
    public int getDay() {
        return 8;
    }

    @Override
    public String solvePuzzleOne() {
        List<String> allInstructions = getAllFileLines(INPUT_FILE);

        boolean[][] initialScreen = new boolean[6][50];

        boolean[][] finalScreen = processAllInstructions(allInstructions, initialScreen);

        return String.valueOf(countTrue(finalScreen));
    }

    @Override
    public String solvePuzzleTwo() {
        List<String> allInstructions = getAllFileLines(INPUT_FILE);

        boolean[][] initialScreen = new boolean[6][50];

        boolean[][] finalScreen = processAllInstructions(allInstructions, initialScreen);

        printScreen(finalScreen);

        return "Read Output ^";
    }

    private boolean[][] processAllInstructions(List<String> allInstructions, boolean[][] initialScreen) {
        boolean[][] currentScreen = initialScreen.clone();

        for (String instruction : allInstructions) {
            currentScreen = processInstruction(instruction, currentScreen);
        }

        return currentScreen;
    }

    private boolean[][] processInstruction(String instruction, boolean[][] screen) {
        Pattern rectPattern = Pattern.compile("rect (\\d+)x(\\d+)");
        Pattern rotatePattern = Pattern.compile("rotate (row|column) (x|y)=(\\d+) by (\\d+)");

        Matcher rectMatcher = rectPattern.matcher(instruction);
        if (rectMatcher.matches()) {
            int x = Integer.valueOf(rectMatcher.group(1));
            int y = Integer.valueOf(rectMatcher.group(2));

            boolean[][] nextScreen = copyArray(screen);
            for (int i = 0; i < y; i++) {
                for (int j = 0; j < x; j++) {
                    nextScreen[i][j] = true;
                }
            }
            return nextScreen;
        }

        Matcher rotateMatcher = rotatePattern.matcher(instruction);
        if (rotateMatcher.matches()) {
            String rotateType = rotateMatcher.group(2);
            int index = Integer.valueOf(rotateMatcher.group(3));
            int offset = Integer.valueOf(rotateMatcher.group(4));
            if ("x".equals(rotateType)) {
                boolean[][] nextScreen = copyArray(screen);
                int numRows = nextScreen.length;
                for (int x = 0; x < numRows; x++) {
                    nextScreen[x][index] = screen[(x - offset + numRows) % numRows][index];
                }
                return nextScreen;
            } else if ("y".equals(rotateType)) {
                boolean[][] nextScreen = copyArray(screen);
                int numCols = nextScreen[index].length;
                for (int y = 0; y < numCols; y++) {
                    nextScreen[index][y] = screen[index][(y - offset + numCols) % numCols];
                }
                return nextScreen;
            }
        }

        throw new RuntimeException("Fix your matchers");
    }

    private long countTrue(boolean[][] screen) {
        long trueCount = 0;

        for (boolean[] row : screen) {
            for (boolean cell : row) {
                if (cell) {
                    trueCount++;
                }
            }
        }

        return trueCount;
    }

    private boolean[][] copyArray(boolean[][] input) {
        boolean[][] output = new boolean[input.length][];

        for (int i = 0; i < input.length; i++) {
            output[i] = Arrays.copyOf(input[i], input[i].length);
        }

        return output;
    }

    private void printScreen(boolean[][] screen) {
        System.out.println("");
        for (int x = 0; x < screen.length; x++) {
            String row = "";
            for (int y = 0; y < screen[x].length; y++) {
                row += screen[x][y] ? "#" : " ";
            }
            System.out.println(row);
        }
        System.out.println("");
    }
}
