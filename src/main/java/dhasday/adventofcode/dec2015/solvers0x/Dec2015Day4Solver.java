package dhasday.adventofcode.dec2015.solvers0x;

import dhasday.adventofcode.dec2015.Dec2015DaySolver;
import org.apache.commons.codec.digest.DigestUtils;

public class Dec2015Day4Solver extends Dec2015DaySolver<Integer> {

    private static final String INPUT_FILE = "src/main/resources/dec2015/4-input";

    @Override
    public int getDay() {
        return 4;
    }

    @Override
    public Integer solvePuzzleOne() {
        String input = getOnlyFileLine(INPUT_FILE);
        return getFirstLeadingMultizeroHash(input, 5);
    }

    @Override
    public Integer solvePuzzleTwo() {
        String input = getOnlyFileLine(INPUT_FILE);
        return getFirstLeadingMultizeroHash(input, 6);
    }

    int getFirstLeadingMultizeroHash(String input, int numZeroes) {
        String expectedPrefix = buildPrefix('0', numZeroes);

        int currentValue = 1; // Must be positive

        while(true) {
            String toEncode = input + currentValue;
            String encoded = DigestUtils.md5Hex(toEncode);

            if (encoded.startsWith(expectedPrefix)) {
                return currentValue;
            }

            currentValue++;
        }
    }

    private String buildPrefix(char character, int num) {
        StringBuilder prefix = new StringBuilder();

        for (int i = 0; i < num; i++) {
            prefix.append(character);
        }

        return prefix.toString();
    }
}
