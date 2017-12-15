package dhasday.adventofcode.dec2016.solvers1x;

import java.util.Arrays;

import dhasday.adventofcode.common.DaySolver;
import org.apache.commons.lang3.StringUtils;

public class Dec2016Day16Solver extends DaySolver<String> {

    private static final String INPUT = "00111101111101000";

    @Override
    public int getDayNumber() {
        return 16;
    }

    @Override
    public String solvePuzzleOne() {
        String fullInput = expandInput(INPUT, 272);
        return calculateChecksum(fullInput);
    }

    @Override
    public String solvePuzzleTwo() {
        String fullInput = expandInput(INPUT, 35651584);
        return calculateChecksum(fullInput);
    }

    private String expandInput(String input, int length) {
        String curValue = input;
        while (curValue.length() < length) {
            curValue = processExpand(curValue);
        }
        return curValue.substring(0, length);
    }

    private String processExpand(String input) {
        String inverted = StringUtils.replaceChars(input, "01", "10");
        return input + "0" + StringUtils.reverse(inverted);
    }

    private String calculateChecksum(String input) {
        if (input.length() % 2 == 1) {
            return input;
        }

        char[] newChecksum = new char[input.length() / 2];
        Arrays.fill(newChecksum, '0');

        int curIndex = 0;
        while (curIndex >= 0) {
            curIndex = replaceNextMatch(newChecksum, curIndex, input, "00");
        }

        curIndex = 0;
        while (curIndex >= 0) {
            curIndex = replaceNextMatch(newChecksum, curIndex, input, "11");
        }

        return calculateChecksum(String.valueOf(newChecksum));
    }

    private int replaceNextMatch(char[] checksum, int curIndex, String input, String match) {
        int nextIndex = input.indexOf(match, curIndex);

        if (nextIndex < 0 || nextIndex < curIndex) {
            return -1;
        }

        if (nextIndex % 2 == 0) {
            checksum[nextIndex / 2] = '1';
            return nextIndex + 2;
        } else {
            return nextIndex + 1;
        }
    }
}
