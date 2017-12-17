package dhasday.adventofcode.dec2015.solvers0x;

import dhasday.adventofcode.dec2015.Dec2015DaySolver;
import org.apache.commons.codec.digest.DigestUtils;
import org.apache.commons.lang3.StringUtils;

public class Dec2015Day4Solver extends Dec2015DaySolver<Integer> {

    private static final String INPUT = "ckczppom";

    @Override
    public int getDay() {
        return 4;
    }

    @Override
    public Integer solvePuzzleOne() {
        return getFirstLeadingMultizeroHash("00000");
    }

    @Override
    public Integer solvePuzzleTwo() {
        return getFirstLeadingMultizeroHash("000000");
    }

    private int getFirstLeadingMultizeroHash(String expectedPrefix) {
        int currentValue = 1; // Must be positive
        while(true) {
            String encodedPrefix = DigestUtils.md5Hex(INPUT + currentValue);

            if (encodedPrefix.startsWith(expectedPrefix)) {
                return currentValue;
            }

            currentValue++;
        }
    }
}
