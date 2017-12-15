package dhasday.adventofcode.dec2015.solvers1x;

import java.util.Set;

import com.google.common.collect.Sets;
import dhasday.adventofcode.dec2015.Dec2015DaySolver;

public class Dec2015Day11Solver extends Dec2015DaySolver<String> {

    private static final String INPUT_FILE = "src/main/resources/dec2015/11-input";

    @Override
    public int getDay() {
        return 11;
    }

    @Override
    public String solvePuzzleOne() {
        String input = getOnlyFileLine(INPUT_FILE);

        return determinNextPassword(input);
    }

    @Override
    public String solvePuzzleTwo() {
        String input = getOnlyFileLine(INPUT_FILE);

        String currentPassword = determinNextPassword(input);

        return determinNextPassword(currentPassword);
    }

    String determinNextPassword(String input) {
        String currentPassword = input;

        do {
            currentPassword = calculateNextPassword(currentPassword);
        } while (!isValidPuzzleOnePassword(currentPassword));

        return currentPassword;
    }

    private String calculateNextPassword(String currentPassword) {
        StringBuilder newPassword = new StringBuilder(currentPassword);

        for (int i = (currentPassword.length() - 1); i >= 0; i--) {
            char rotatedChar = rotateCharacter(currentPassword.charAt(i));

            newPassword.setCharAt(i, rotatedChar);

            if (rotatedChar != 'a') {
                return newPassword.toString();
            }
        }

        return newPassword.toString();
    }

    private char rotateCharacter(char input) {
        if (input == 'z') {
            return 'a';
        } else {
            char result = input;
            result++;
            return result;
        }
    }

    private boolean isValidPuzzleOnePassword(String password) {
        Set<String> invalidLetters = Sets.newHashSet("i", "o", "l");

        if (invalidLetters.stream().anyMatch(password::contains)) {
            return false;
        }

        if (password.length() < 4) {
            return false;
        }

        boolean foundIncreasing = false;
        Character firstDuplicate = null;
        Character secondDuplicate = null;

        for (int i = 1; i < password.length(); i++) {
            char previousChar = password.charAt(i - 1);
            char currentChar = password.charAt(i);

            if (firstDuplicate == null) {
                if (previousChar == currentChar) {
                    firstDuplicate = previousChar;
                }
            } else if (secondDuplicate == null && currentChar != firstDuplicate) {
                if (previousChar == currentChar) {
                    secondDuplicate = previousChar;
                }
            }

            if (!foundIncreasing && i > 1) {
                char twoBackCharacter = password.charAt(i - 2);
                foundIncreasing = areSequentialCharacters(twoBackCharacter, previousChar, currentChar);
            }
        }

        return foundIncreasing
                && firstDuplicate != null
                && secondDuplicate != null;
    }

    private boolean areSequentialCharacters(char charOne, char charTwo, char charThree) {
        return (charOne + 1) == charTwo && (charTwo + 1) == charThree;
    }

}
