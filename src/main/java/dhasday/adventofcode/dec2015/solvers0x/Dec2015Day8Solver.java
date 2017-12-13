package dhasday.adventofcode.dec2015.solvers0x;

import java.util.List;

import dhasday.adventofcode.common.DaySolver;

public class Dec2015Day8Solver implements DaySolver<Integer> {

    private static final String INPUT_FILE = "src/main/resources/dec2015/8-input";

    @Override
    public int getDayNumber() {
        return 8;
    }

    @Override
    public Integer solvePuzzleOne() {
        List<String> allStrings = getAllFileLines(INPUT_FILE);

        return allStrings.stream()
                .mapToInt(value -> getCodeCharacterCount(value) - getStringCharacterCount(value))
                .sum();
    }

    @Override
    public Integer solvePuzzleTwo() {
        List<String> allStrings = getAllFileLines(INPUT_FILE);

        return allStrings.stream()
                .mapToInt(value -> getEscapedCharacterCount(value) - getCodeCharacterCount(value))
                .sum();
    }

    int getCodeCharacterCount(String value) {
        return value.length();
    }

    int getStringCharacterCount(String value) {
        String cleanedValue = value.replaceAll("(^\"|\"$)", "");
        cleanedValue = cleanedValue.replaceAll("\\\\(x[0-9a-f][0-9a-f]|\"|\\\\)", "-");
        return cleanedValue.length();
    }

    int getEscapedCharacterCount(String value) {
        String escapedValue = value.replaceAll("\\\\", "\\\\\\\\"); // Replace every \ with \\
        escapedValue = escapedValue.replaceAll("\"", "\\\\\\\"");   // Replace every " with \"
        escapedValue = "\"" + escapedValue + "\"";                  // Prefix and Suffix with "

        return escapedValue.length();
    }

}
