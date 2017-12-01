package dhasday.adventofcode.dec2015.solvers;

import java.util.List;
import java.util.Set;

import com.google.common.collect.ImmutableSet;
import dhasday.adventofcode.DaySolver;

public class Dec2015Day5Solver implements DaySolver {

    private static final String INPUT_FILE = "src/main/resources/dec2015/5-input";

    private static final Set<Character> VOWELS = ImmutableSet.of('a', 'e', 'i', 'o', 'u');
    private static final Set<String> BLACKLISTED_PAIRS = ImmutableSet.of("ab", "cd", "pq", "xy");

    @Override
    public int getDayNumber() {
        return 5;
    }

    @Override
    public Integer solvePuzzleOne() {
        List<String> input = getAllFileLines(INPUT_FILE);
        return (int) input.stream()
                .filter(this::isStringValidV1)
                .count();
    }

    @Override
    public Integer solvePuzzleTwo() {
        List<String> input = getAllFileLines(INPUT_FILE);
        return (int) input.stream()
                .filter(this::isStringValidV2)
                .count();
    }

    boolean isStringValidV1(String input) {
        int numVowels = 0;
        boolean containsDuplicate = false;

        for (int i = 0; i < input.length(); i++) {
            char currentChar = input.charAt(i);

            if (VOWELS.contains(currentChar)) {
                numVowels++;
            }

            if (i > 0) {
                char previousChar = input.charAt(i - 1);
                containsDuplicate = containsDuplicate || currentChar == previousChar;

                String pair = new String(new char[] {previousChar, currentChar});
                if (BLACKLISTED_PAIRS.contains(pair)) {
                    return false;
                }
            }
        }

        return containsDuplicate && numVowels >= 3;
    }

    boolean isStringValidV2(String input) {
        boolean foundDuplicatePair = false;
        boolean foundRepeatingLetter = false;

        for (int i = 0; i < input.length(); i++) {
            char currentChar = input.charAt(i);

            if (i > 0) {
                char previousChar = input.charAt(i - 1);
                String pair = new String(new char[] {previousChar, currentChar});

                if (input.length() > (i + 1)) {
                    foundDuplicatePair = foundDuplicatePair || input.substring(i + 1).contains(pair);
                }
            }

            if (i > 1) {
                char twoBackChar = input.charAt(i - 2);
                foundRepeatingLetter = foundRepeatingLetter || (twoBackChar == currentChar);
            }
        }

        return foundDuplicatePair && foundRepeatingLetter;
    }
}
