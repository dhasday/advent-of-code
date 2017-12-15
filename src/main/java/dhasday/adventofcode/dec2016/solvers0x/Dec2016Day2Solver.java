package dhasday.adventofcode.dec2016.solvers0x;

import java.util.List;

import dhasday.adventofcode.dec2016.Dec2016DaySolver;

public class Dec2016Day2Solver extends Dec2016DaySolver<String> {

    private static final String INPUT_FILE = "src/main/resources/dec2016/2-input";

    @Override
    public int getDay() {
        return 2;
    }

    @Override
    public String solvePuzzleOne() {
        List<String> allInstructions = getAllFileLines(INPUT_FILE);

        Character[][] numpad = new Character[][]{
                new Character[] {'1', '2', '3'},
                new Character[] {'4', '5', '6'},
                new Character[] {'7', '8', '9'}
        };

        return determineCode(numpad, allInstructions);
    }

    @Override
    public String solvePuzzleTwo() {
        List<String> allInstructions = getAllFileLines(INPUT_FILE);

        Character[][] numpad = new Character[][]{
                new Character[] {null,  null,   '1',    null,   null},
                new Character[] {null,  '2',    '3',    '4',    null},
                new Character[] {'5',   '6',    '7',    '8',    '9'},
                new Character[] {null,  'A',    'B',    'C',    null},
                new Character[] {null,  null,   'D',    null,   null}
        };

        return determineCode(numpad, allInstructions);
    }

    private String determineCode(Character[][] numpad, List<String> instructions) {
        Position currentPosition = new Position(1, 1);

        String result = "";

        for(String instruction : instructions) {
            currentPosition = processInstruction(numpad, currentPosition, instruction);
            result += numpad[currentPosition.x][currentPosition.y];
        }

        return result;
    }

    private Position processInstruction(Character[][] numpad, Position startPosition, String instruction) {
        int curX = startPosition.x;
        int curY = startPosition.y;

        for (int i = 0; i < instruction.length(); i++) {
            char curChar = instruction.charAt(i);

            switch (curChar) {
                case 'U':
                    int minusX = curX - 1;
                    if (isValid(numpad, minusX, curY)) {
                        curX = minusX;
                    }
                    break;
                case 'D':
                    int plusX = curX + 1;
                    if (isValid(numpad, plusX, curY)) {
                        curX = plusX;
                    }
                    break;
                case 'L':
                    int minusY = curY - 1;
                    if (isValid(numpad, curX, minusY)) {
                        curY = minusY;
                    }
                    break;
                case 'R':
                    int plusY = curY + 1;
                    if (isValid(numpad, curX, plusY)) {
                        curY = plusY;
                    }
                    break;
            }
        }

        return new Position(curX, curY);
    }

    private boolean isValid(Character[][] numpad, int x, int y) {
        try {
            return numpad[x][y] != null;
        } catch (IndexOutOfBoundsException ioobe) {
            return false;
        }
    }


    private class Position {
        private int x;
        private int y;

        Position(int x, int y) {
            this.x = x;
            this.y = y;
        }
    }
}
