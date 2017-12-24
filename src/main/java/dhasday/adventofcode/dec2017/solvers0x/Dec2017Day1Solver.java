package dhasday.adventofcode.dec2017.solvers0x;

import dhasday.adventofcode.dec2017.Dec2017DaySolver;

public class Dec2017Day1Solver extends Dec2017DaySolver<Integer> {

    private static final String DAY_ONE_INPUT = "src/main/resources/dec2017/1-input";

    @Override
    public int getDay() {
        return 1;
    }

    @Override
    public Integer solvePuzzleOne() {
        String input = getOnlyFileLine(DAY_ONE_INPUT);
        return sumOfDuplicateDigits(input, 1);
    }

    @Override
    public Integer solvePuzzleTwo() {
        String input = getOnlyFileLine(DAY_ONE_INPUT);
        int offset = input.length() / 2;
        return sumOfDuplicateDigits(input, offset);
    }

    private int sumOfDuplicateDigits(String input, int offset) {
        int inputLength = input.length();

        int sum = 0;

        for (int i = 0; i < inputLength; i++) {
            int nextCharIndex = (i + offset) % inputLength;

            char currentChar = input.charAt(i);
            if (currentChar == input.charAt(nextCharIndex)) {
                sum += (currentChar - '0');
            }
        }

        return sum;
    }
}
