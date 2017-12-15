package dhasday.adventofcode.dec2016.solvers0x;

import java.util.Arrays;
import java.util.Comparator;
import java.util.List;
import java.util.regex.Matcher;
import java.util.regex.Pattern;
import java.util.stream.Collectors;

import com.google.common.collect.Lists;
import dhasday.adventofcode.dec2016.Dec2016DaySolver;

public class Dec2016Day3Solver extends Dec2016DaySolver<Long> {

    private static final String INPUT_FILE = "src/main/resources/dec2016/3-input";

    private static final String INPUT_REGEX = "([^\\d]*)?(\\d+)([ ]+)(\\d+)([ ]+)(\\d+)";

    private Pattern inputPattern = Pattern.compile(INPUT_REGEX);

    @Override
    public int getDay() {
        return 3;
    }

    @Override
    public Long solvePuzzleOne() {
        List<String> allInputs = getAllFileLines(INPUT_FILE);

        return allInputs.stream()
                .filter(this::isValidHorizontalTriangle)
                .count();
    }

    @Override
    public Long solvePuzzleTwo() {
        List<String> allInputs = getAllFileLines(INPUT_FILE);

        if (allInputs.size() % 3 != 0) {
            throw new RuntimeException("Invalid input. Num rows must be divisible by 3.");
        }

        return countValidVerticalTriangles(allInputs);
    }

    private boolean isValidHorizontalTriangle(String input) {
        List<Integer> allSides = matchRow(input);

        return isValidTriangle(allSides);
    }

    private long countValidVerticalTriangles(List<String> allInputs) {
        long validTriangleCount = 0;

        for (int i = 0; i < allInputs.size(); i = i + 3) {
            List<Integer> rowOne = matchRow(allInputs.get(i));
            List<Integer> rowTwo = matchRow(allInputs.get(i + 1));
            List<Integer> rowThree = matchRow(allInputs.get(i + 2));

            for (int j = 0; j < 3; j++) {
                if (isValidTriangle(getIndexFromAllLists(j, rowOne, rowTwo, rowThree))) {
                    validTriangleCount++;
                }
            }
        }

        return validTriangleCount;
    }

    private List<Integer> matchRow(String row) {
        Matcher matcher = inputPattern.matcher(row);

        if (!matcher.matches()) {
            throw new RuntimeException("Unable to map input line: " + row);
        }

        return Lists.newArrayList(
                Integer.valueOf(matcher.group(2)),
                Integer.valueOf(matcher.group(4)),
                Integer.valueOf(matcher.group(6))
        );
    }

    private List<Integer> getIndexFromAllLists(int index, List<Integer>... lists) {
        return Arrays.stream(lists)
                .map(list -> list.get(index))
                .collect(Collectors.toList());
    }

    private boolean isValidTriangle(List<Integer> sides) {
        sides.sort(Comparator.naturalOrder());

        return (sides.get(0) + sides.get(1)) > sides.get(2);
    }
}
