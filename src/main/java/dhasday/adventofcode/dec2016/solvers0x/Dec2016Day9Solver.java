package dhasday.adventofcode.dec2016.solvers0x;

import java.util.regex.Matcher;
import java.util.regex.Pattern;

import dhasday.adventofcode.DaySolver;

public class Dec2016Day9Solver implements DaySolver<Long> {
    private static final String INPUT_FILE = "src/main/resources/dec2016/9-input";

    private Pattern pattern = Pattern.compile("(\\((\\d+)x(\\d+)\\))");

    @Override
    public int getDayNumber() {
        return 9;
    }

    @Override
    public Long solvePuzzleOne() {
        return decompress(getOnlyFileLine(INPUT_FILE), false);
    }

    @Override
    public Long solvePuzzleTwo() {
        return decompress(getOnlyFileLine(INPUT_FILE), true);
    }

    Long decompress(String input, boolean recursive) {
        Matcher matcher = pattern.matcher(input);

        long outputSize = 0;

        int currentIndex = 0;
        while(currentIndex < input.length() && matcher.find(currentIndex)) {
            outputSize += matcher.start() - currentIndex; // Add the characters we skipped over

            currentIndex = matcher.start() + matcher.group(1).length();

            int numChars = Integer.valueOf(matcher.group(2));
            int numTimes = Integer.valueOf(matcher.group(3));

            String repeatContents = input.substring(currentIndex, currentIndex + numChars);

            long groupSize = recursive ? decompress(repeatContents, true) : numChars;
            outputSize += (groupSize * numTimes);
            currentIndex += numChars;
        }

        // We we're done matching, add any remaining characters and return result
        outputSize += input.length() - currentIndex;
        return outputSize;
    }
}
