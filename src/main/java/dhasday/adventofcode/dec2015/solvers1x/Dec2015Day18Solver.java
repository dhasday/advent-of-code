package dhasday.adventofcode.dec2015.solvers1x;

import java.util.List;

import dhasday.adventofcode.common.DaySolver;

public class Dec2015Day18Solver implements DaySolver<Integer> {

    private static final String INPUT_FILE = "src/main/resources/dec2015/18-input";

    @Override
    public int getDayNumber() {
        return 18;
    }

    @Override
    public Integer solvePuzzleOne() {
        List<String> allFileLines = getAllFileLines(INPUT_FILE);

        int sizeX = 100;
        int sizeY = 100;
        int numTransitions = 100;

        boolean[][] currentState = loadState(allFileLines, sizeX, sizeY);

        for (int i = 0; i < numTransitions; i++) {
            currentState = processStep(currentState, sizeX, sizeY, false);
        }

        return countOnLights(currentState);
    }

    @Override
    public Integer solvePuzzleTwo() {
        List<String> allFileLines = getAllFileLines(INPUT_FILE);

        int sizeX = 100;
        int sizeY = 100;
        int numTransitions = 100;

        boolean[][] currentState = loadState(allFileLines, sizeX, sizeY);

        for (int i = 0; i < numTransitions; i++) {
            currentState = processStep(currentState, sizeX, sizeY, true);
        }

        return countOnLights(currentState);
    }

    private boolean[][] loadState(List<String> inputLines, int sizeX, int sizeY) {
        boolean[][] state = new boolean[sizeX][sizeY];

        for (int x = 0; x < sizeY; x++) {
            String line = inputLines.get(x);

            for (int y = 0; y < sizeX; y++) {
                char curChar = line.charAt(y);

                if (curChar == '#') {
                    state[x][y] = true;
                } else if (curChar == '.') {
                    state[x][y] = false;
                } else {
                    throw new RuntimeException("Unable to determine light state for unknown character: " + curChar);
                }
            }
        }

        return state;
    }

    private boolean[][] processStep(boolean[][] currentState, int sizeX, int sizeY, boolean keepCornersLit) {
        boolean[][] newState = new boolean[sizeX][sizeY];

        for (int y = 0; y < sizeY; y++) {
            for (int x = 0; x < sizeX; x++) {
                int numNeighborsOn = getNumberNeighborsOn(currentState, sizeX, sizeY, x, y);

                newState[x][y] = (numNeighborsOn == 3) || (numNeighborsOn == 2 && currentState[x][y]);

                if (keepCornersLit && (x == 0 || x == sizeX - 1) && (y == 0 || y == sizeY - 1)) {
                    newState[x][y] = true;
                }
            }
        }

        return newState;
    }

    private int getNumberNeighborsOn(boolean[][] state, int sizeX, int sizeY, int x, int y) {
        int numOn = 0;

         for (int i = (x - 1); i <= (x + 1); i++) {
             if (i < 0 || i >= sizeX) {
                 continue;
             }

             for (int j = (y - 1); j <= (y + 1); j++) {
                 if (j < 0 || j >= sizeY) {
                     continue;
                 }

                 if ((i != x || j != y) && state[i][j]) {
                     numOn++;
                 }
             }
         }

         return numOn;
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

    private void printState(boolean[][] lightField) {
        System.out.println("");
        for (boolean[] lightRow : lightField) {
            String row = "";
            for (boolean light : lightRow) {
                if (light) {
                    row += "#";
                } else {
                    row += ".";
                }
            }
            System.out.println(row);
        }
        System.out.println("");
    }
}
