package dhasday.adventofcode.dec2015.solvers1x;

import dhasday.adventofcode.DaySolver;

public class Dec2015Day10Solver implements DaySolver<Integer> {

    private static final String INPUT_FILE = "src/main/resources/dec2015/10-input";

    @Override
    public int getDayNumber() {
        return 10;
    }

    @Override
    public Integer solvePuzzleOne() {
        String input = getOnlyFileLine(INPUT_FILE);

        return lookAndSayNTimes(input, 40).length();
    }

    @Override
    public Integer solvePuzzleTwo() {
        String input = getOnlyFileLine(INPUT_FILE);

        return lookAndSayNTimes(input, 50).length();
    }

    private String lookAndSayNTimes(String input, int numTimes) {
        String currentValue = input;

        for (int i = 0; i < numTimes; i++) {
            currentValue = lookAndSay(currentValue);
        }

        return currentValue;
    }

    private String lookAndSay(String input) {
        char character = input.charAt(0);
        int charCount = 1;

        StringBuilder result = new StringBuilder();

        for (int i = 1; i < input.length(); i++) {
            char currentChar = input.charAt(i);

            if (character == currentChar) {
                charCount++;
            } else {
                result.append(charCount);
                result.append(character);

                character = currentChar;
                charCount = 1;
            }
        }

        result.append(charCount);
        result.append(character);

        return result.toString();
    }
}
