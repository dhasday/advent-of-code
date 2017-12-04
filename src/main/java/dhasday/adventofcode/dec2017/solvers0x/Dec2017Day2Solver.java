package dhasday.adventofcode.dec2017.solvers0x;

import java.util.Arrays;
import java.util.List;
import java.util.stream.Collectors;

import dhasday.adventofcode.DaySolver;

public class Dec2017Day2Solver implements DaySolver<Integer> {

    private static final String INPUT_FILE = "src/main/resources/dec2017/2-input";

    @Override
    public int getDayNumber() {
        return 2;
    }

    @Override
    public Integer solvePuzzleOne() {
        List<String> input = getAllFileLines(INPUT_FILE);

        return input.stream()
                .map(this::parseTsvLine)
                .mapToInt(this::findMaxMinusMinChecksum)
                .sum();
    }

    @Override
    public Integer solvePuzzleTwo() {
        List<String> input = getAllFileLines(INPUT_FILE);

        return input.stream()
                .map(this::parseTsvLine)
                .mapToInt(this::findEvenlyDivisibleChecksum)
                .sum();
    }

    private List<Integer> parseTsvLine(String input) {
        return Arrays.stream(input.split("\t"))
                .map(Integer::valueOf)
                .collect(Collectors.toList());
    }

    private Integer findMaxMinusMinChecksum(List<Integer> values) {
        Integer max = values.get(0);
        Integer min = values.get(0);

        for (int i = 1; i < values.size(); i++) {
            max = Math.max(max, values.get(i));
            min = Math.min(min, values.get(i));
        }

        return max - min;
    }

    private Integer findEvenlyDivisibleChecksum(List<Integer> values) {
        for (int i = 0; i < values.size(); i++) {
            Integer valOne = values.get(i);

            for (int j = i + 1; j < values.size(); j++) {
                Integer valTwo = values.get(j);

                if (valOne % valTwo == 0) {
                    return valOne / valTwo;
                } else if (valTwo % valOne == 0) {
                    return valTwo / valOne;
                }
            }
        }

        throw new RuntimeException("Unable to find an evenly divisible pair");
    }
}
